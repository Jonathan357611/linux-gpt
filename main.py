import json
import requests
from colorama import Fore, Back, init
import re
import subprocess
import time
import os


def gpt_request(model, url, messages):
    """
    Make POST-request to desired API-endpoint
    """
    return requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={"model": model, "messages": messages},
    )


def gpt_request_handler(model, url, system_content, user_content):
    """
    Handle all possible errors when requesting, printing status and returning when successfull
    """
    while True:
        try:
            # Make request
            request = gpt_request(
                model=model,
                url=url,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content},
                ],
            )
            return request.json()["choices"][0]["message"]["content"] # return message
        except KeyError:
            # Retrying on chatgpt-error
            print(f"{Back.RED}TEMPORARY ISSUE, RETRYING IN 3s...")
            time.sleep(3)
        except Exception as e:
            print(f"{Back.RED}FATAL ERROR! EXITING...")
            print(e)
            exit(1)


def main(settings, info_command):
    query = input(f"{Back.YELLOW} [ {Back.GREEN} QUERY {Back.YELLOW} ] {Back.RESET} > ")
    print(f"{Back.YELLOW}THINKING...")

    # Make requests
    ## Get command
    command = gpt_request_handler(
        settings["model"],
        settings["url"],
        settings["system_messages"]["command"].replace(r"{info_command}", info_command),
        query,
    )
    ## Get commands explanation from independent API call
    explanation = gpt_request_handler(
        settings["model"],
        settings["url"],
        settings["system_messages"]["explanation"].replace(
            r"{info_command}", info_command
        ),
        command,
    )

    # Try to filter out codebrackets, as I could not get rid of them in the system-message
    if "```" in command:
        command = re.search(r"`bash(.*?)`", command, re.DOTALL).group(1).strip()

    print(f"{Back.GREEN}✨ Done! Your command is here!")

    print(f"{Back.CYAN}Press {Back.LIGHTBLUE_EX}ENTER{Back.CYAN} to run")
    print(f"{Back.CYAN}EXPLANATION:{Back.RESET} {explanation}")
    input(f"{Back.CYAN}COMMAND:{Back.RESET} \033[4m{command}\033[0m")

    subprocess.run(command, shell=True) # Execute proposed command

    print(f"{Back.GREEN}{Fore.WHITE}✨{Fore.RESET} Done! {Fore.WHITE}✨")

if __name__ == "__main__":
    init(autoreset=True) # Init colorama

    # Load settings file
    with open(os.path.join(os.path.expanduser("~"), ".config/linuxgpt/settings.json"), "r") as f:
        settings = json.loads(f.read())

    # Generate "info_command" for the AI, gives it information about your system
    info_command = ""
    for command in settings["info_commands"]:
        info_command += command["system_query"].replace(
            r"{command}",
            subprocess.check_output(command["command"], shell=True, text=True),
        )

    main(settings, info_command) # Run

pkgname=python-linuxgpt
pkgver=1.0
pkgrel=1
pkgdesc="Talk to your terminal like a human, thanks to chatgpt"
arch=("x86_64")
url="https://github.com/Jonathan357611/linux-gpt"
license=("MIT")
depends=("python" "python-requests" "python-colorama")
source=("https://github.com/Jonathan357611/linux-gpt/releases/download/1.0/python-linuxgpt-1.0.tar.gz")
sha256sums=("76effc98cfaf9c3f7adbef0b1cc52a070835bedc6549e777bd136fee54733e66")

prepare() {
    cd "$srcdir"
    mkdir -p linuxgpt
    tar xf python-linuxgpt-$pkgver.tar.gz -C linuxgpt --strip-components=1
    rm python-linuxgpt-$pkgver.tar.gz
}

build() {
    cd "linuxgpt"
    python3 -m venv venv
    source venv/bin/activate
    #python3 -m venv/bin/pip3 install -r requirements.txt
}

package() {
    cd "linuxgpt"
    install -D -m755 main.py "$pkgdir/usr/bin/linuxgpt"
    mkdir -p ~/.config/linuxgpt
    mv settings.json ~/.config/linuxgpt/
    install -D -m644 settings.json "$pkgdir/usr/share/$pkgname/settings.json"
}
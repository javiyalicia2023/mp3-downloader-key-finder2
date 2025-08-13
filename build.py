import PyInstaller.__main__
import sys


def build():
    target = sys.argv[1] if len(sys.argv) > 1 else 'gui'
    entry = 'gui.py' if target == 'gui' else 'main.py'
    name = 'mp3-tool-gui' if target == 'gui' else 'mp3-tool-cli'
    PyInstaller.__main__.run([
        entry,
        '--onefile',
        '--name', name,
    ])


if __name__ == '__main__':
    build()

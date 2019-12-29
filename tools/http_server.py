"""
pip install -r requirements.txt
pyinstaller -Fw http_server.py
"""
from os import getcwd
from threading import Thread
from functools import partial
from webbrowser import open as browser_open
from socket import socket, AF_INET, SOCK_DGRAM
from http.server import test, SimpleHTTPRequestHandler

from gooey import Gooey, GooeyParser


def get_host_ip():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def server(port=None, directory=None):
    if port is None:
        port = 8000
    if directory is None:
        directory = getcwd()
    HandlerClass = partial(SimpleHTTPRequestHandler, directory=directory)
    Thread(target=test, kwargs=dict(HandlerClass=HandlerClass, port=port)).start()
    Thread(target=browser_open, args=(f"http://localhost:{port}",)).start()


@Gooey(
    program_name=get_host_ip(),
    program_description="打开一个本地文件服务器",
    language="Chinese",
)
def main():
    parser = GooeyParser()
    parser.add_argument("port", default=8000, type=int, metavar="端口")
    parser.add_argument("directory", default=getcwd(), widget="DirChooser", metavar="选择目录")
    args = parser.parse_args()
    server(port=args.port, directory=args.directory)


if __name__ == "__main__":
    main()
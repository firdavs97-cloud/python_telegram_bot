import socket
from urllib.parse import urlparse
from requests import get, codes, exceptions


def ping_server(server: str, port: int = None, timeout=3):
    """ping server"""
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port if port is not None else 443))
    except OSError as error:
        return False
    else:
        s.close()
        return True


def request_get(url: str, headers: str = None, params: str = None, timeout=60):
    domain = urlparse(url)
    if ping_server(domain.netloc, domain.port):
        try:
            response = get(url, headers=headers, params=params, timeout=timeout)
            if response.status_code == codes.ok:
                return response.text
        except exceptions.Timeout:
            print("Сайт долго не отвечает")
    else:
        print("Сайт недоступен")

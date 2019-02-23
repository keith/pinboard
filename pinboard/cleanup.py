from .helpers import credentials
import requests
import webbrowser

API_URL = "https://api.pinboard.in/v1/"
DELETE_URL = API_URL + "posts/delete"
POSTS_URL = API_URL + "posts/all"
USER_AGENT = """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1
Safari/537.36""".replace("\n", " ")
HEADERS = {"User-agent": USER_AGENT}
_DEFAULT_PARAMS = {
    "auth_token": credentials.token(),
    "format": "json",
    "User-agent": USER_AGENT,
}


def ask(status, URL):
    answer = input("%d Delete %s y/N/o: " % (status, URL)).lower()
    if answer.startswith("o"):
        webbrowser.open_new_tab(URL)
        return ask(status, URL)
    else:
        return answer.startswith("y")


class Bookmark(object):
    def __init__(self, item):
        self.url = item["href"]

    def delete(self):
        requests.get(DELETE_URL, params={**_DEFAULT_PARAMS, "url": self.url})


def status_code(URL):
    response = requests.head(URL, allow_redirects=True, headers=HEADERS)
    if response.status_code < 400:
        return response.status_code

    response = requests.get(URL, headers=HEADERS)
    return response.status_code


def get_items():
    response = requests.get(POSTS_URL, params=_DEFAULT_PARAMS)
    return list(map(Bookmark, response.json()))


def main(_):
    items = get_items()
    for item in items:
        try:
            status = status_code(item.url)
        except requests.exceptions.ConnectionError:
            status = 500
        except requests.exceptions.TooManyRedirects:
            status = 500
        except requests.exceptions.Timeout:
            status = 500

        if status >= 400:
            delete = ask(status, item.url)
            if delete:
                item.delete()

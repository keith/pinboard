from .helpers import credentials
import requests
import webbrowser

API_URL = "https://api.pinboard.in/v1/"
DELETE_URL = API_URL + "posts/delete"
POSTS_URL = API_URL + "posts/all"
_DEFAULT_PARAMS = {"format": "json", "auth_token": credentials.token()}


class Bookmark(object):
    def __init__(self, item):
        self.url = item["href"]
        self.unread = item["toread"] == "yes"
        self.hastags = len(item["tags"]) != 0

    def delete(self):
        requests.get(DELETE_URL, params={**_DEFAULT_PARAMS, "url": self.url})


def get_items():
    response = requests.get(POSTS_URL, params=_DEFAULT_PARAMS)
    items = map(Bookmark, response.json())
    return [item for item in items if item.unread or not item.hastags]


def main(args):
    items = get_items()
    for i in range(args.count):
        if i >= len(items):
            break

        item = items[i]
        if webbrowser.open_new_tab(item.url):
            item.delete()

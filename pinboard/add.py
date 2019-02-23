from helpers import credentials
import requests
import sys

ADD_URL = "https://api.pinboard.in/v1/posts/add"


def request_params(params):
    return dict({"format": "json",
                 "auth_token": credentials.token()}.items() + params.items())


def usage(prg):
    print("Usage: %s URL" % prg)
    sys.exit(2)


def format_url(url):
    if url.find("://") == -1:
        return "https://%s" % url
    else:
        return url


def main(args):
    raw_url = args.url
    url = format_url(raw_url)
    params = request_params({"url": url, "description": url, "toread": "yes"})
    response = requests.post(ADD_URL, params=params)
    if response.status_code != 200:
        print(response.text)
        sys.exit(1)

    if "Pinboard is Down" in response.text:
        print(response.text)
        sys.exit(1)

    json = response.json()
    if json["result_code"] != "done":
        print(json)
        sys.exit(1)

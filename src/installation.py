import os
from getpass import getpass
import json

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    quit("Required Libraries aren't installed. Please restart installation.")

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".nalanda-cli","config.json")
SUBJECTS_FILE = os.path.join(os.path.expanduser("~"), ".nalanda-cli","subjects.json")
DATA_FILE = os.path.join(os.path.expanduser("~"), ".nalanda-cli","data.json")
LOGIN_LINK = "http://nalanda.bits-pilani.ac.in/login/index.php"
HOMEPAGE_LINK = "http://nalanda.bits-pilani.ac.in/my"

session = requests.session()

try:
    config = {}
    sub_name_url = {}
    URLS = {}

    while True:
        config["username"] = input("\nEnter BITS ID [Eg: f2016015]\n")
        config["username"] += "@pilani.bits-pilani.ac.in"

        config["password"] = getpass(prompt = "Enter nalanda password:")

        result = session.post(LOGIN_LINK, data = config)
        result = BeautifulSoup(result.text, "html.parser")

        if not result.find_all("a", {"id": "loginerrormessage"}):
            break
        print("Username or Password Incorrect. Please retry")
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

    result = session.get(HOMEPAGE_LINK)
    soup = BeautifulSoup(result.text, "html.parser")

    for x in soup.find_all("div", "column c1"):
        sub_name_url[x.contents[0].get("href")] = ((x.contents[0].contents[1]).split("/")[0]).split("\\")[0]
        URLS[x.contents[0].get("href")] = {
            "resource": [],
            "notice": [],
            "news":[]
        }

    json.dump(URLS, open(DATA_FILE, 'w'))
    json.dump(sub_name_url, open(SUBJECTS_FILE, "w"))


except KeyboardInterrupt:
    quit("Installation cancelled by user. Please retry.")
except requests.exceptions.ConnectionError:
    quit("No Internet Connection. Please retry.")
except IOError:
    quit("Unable to read from file. Please reinstall nalanda-cli.")

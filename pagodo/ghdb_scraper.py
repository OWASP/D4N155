#!/usr/bin/env python

# Standard Python libraries.
import json

# Third party Python libraries.
import requests
from bs4 import BeautifulSoup  # noqa

# Custom Python libraries.


def retrieve_google_dorks():
    """Retrieves all google dorks from https://www.exploit-db.com/google-hacking-database
    Writes then entire json reponse to a file in addition to just the dorks.
    """

    url = "https://www.exploit-db.com/google-hacking-database"

    header = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "deflate, gzip, br",
        "Accept-Language": "en-US",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = requests.get(url, headers=header, verify=True)

    if response.status_code != 200:
        print(f"[-] Error retrieving google dorks from: {url}")
        return

    # Extract json data.
    json_response = response.json()

    # Extract recordsTotal and data.
    total_records = json_response["recordsTotal"]
    json_dorks = json_response["data"]

    google_dork_file = f"pagodo/google_dorks.txt"
    with open(google_dork_file, "w") as fh:
        for dork in json_dorks:
            soup = BeautifulSoup(dork["url_title"], "html.parser")
            extracted_dork = soup.find("a").contents[0]
            fh.write(f"{extracted_dork}\n")

    print(f"[*] Total Google dorks retrieved: {total_records}")



if __name__ == "__main__":
    retrieve_google_dorks()
    print("[+] Done!")

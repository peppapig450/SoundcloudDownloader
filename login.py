import argparse
import os

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the login credentials
username = os.getenv("SOUNDCLOUD_USERNAME")
password = os.getenv("SOUNDCLOUD_PASSWORD")


# Function to login to SoundCloud
def login(username, password):
    # SoundCloud login URL
    login_url = "https://api-auth.soundcloud.com/sign-in?client_id=KhqBlYHkMDSGNC9DdLrcJHXqaLv5kOrh"

    # Request headers
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,ceb;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "424",
        "Content-Type": "application/json",
        "Cookie": "sc_anonymous_id=402662-908203-750258-293701; cookie_consent=1; ajs_anonymous_id=%221d3668d0-f98f-4866-95de-610e6e16290c%22; sc_session={%22id%22:%22D8EF8090-23A5-4627-811A-801BEABBC35B%22%2C%22lastBecameInactive%22:%222024-03-28T04:41:55.424Z%22}; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Mar+27+2024+21%3A41%3A55+GMT-0700+(Pacific+Daylight+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4cc37fb7-4ff0-4463-833b-bae6263bafea&interactionCount=0&landingPath=https%3A%2F%2Fsoundcloud.com%2Fsignin&groups=C0001%3A1%2CC0003%3A1%2CC0007%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1; _ga=GA1.2.692459250.1711600916; _gid=GA1.2.1329490610.1711600916; __qca=P0-294270673-1711600915849; _gat_gtag_UA_2519404_44=1; IR_gbd=soundcloud.com; IR_20541=1711600916446%7C0%7C1711600916446%7C%7C; _fbp=fb.1.1711600916533.707533732; datadome=nEex9_0QR4ioHAu626eTUt18NOUYUHcF8pNTe9LlWREYwLw7oOL6Mp2V4Bl9Xinkt~zrmqGWeW4niZ~67qhqERiMFMiLOB396U75Prtt5w2tB9fDeVvZynmbHWTZDtHb",
        "DNT": "1",
        "Host": "api-auth.soundcloud.com",
        "Origin": "https://secure.soundcloud.com",
        "Referer": "https://secure.soundcloud.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "X-Csrf-Token": "e7c332657c1c3f8f979df727c11f57a17063d99c3cd06174a8a05642dce16f6e",
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    # Construct the payload (request body)
    payload = {
        "credentials": {
            "kind": "password",
            "body": {"identifier": username, "password": password},
        },
        "vk": {
            "cp": "6Lf_t_wUAAAAACyAReaZlQzxI0fxbxhNCwrngjp6",
            "cr": None,
            "sg": "8:33-1-24237-579-2073600-1283-39-40:f32cf2:3",
            "dd": "402662-908203-750258-293701",
            "ag": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "cd": "KhqBlYHkMDSGNC9DdLrcJHXqaLv5kOrh",
        },
    }

    # Send the login request with both payload and headers
    response = requests.post(login_url, json=payload, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Login successful")
        return True
    else:
        print("Login failed")
        return False


# Function to scrape playlist and extract track URLs
def scrape_playlist(username, playlist_name):
    # Make the request to retrieve playlist information
    playlist_response = requests.get(
        f"https://api.soundcloud.com/resolve?url=https://soundcloud.com/{username}/{playlist_name}&client_id=KhqBlYHkMDSGNC9DdLrcJHXqaLv5kOrh"
    )

    # Check if the request was successful
    if playlist_response.status_code == 200:
        # Parse the JSON response
        playlist_data = playlist_response.json()

        # Extract URLs of tracks in the playlist
        track_urls = list(
            map(lambda track: track["permalink_url"], playlist_data["tracks"])
        )

        return track_urls
    else:
        print("Failed to retrieve playlist information")

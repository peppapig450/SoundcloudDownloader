import argparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from lxml import etree
from soupsieve import select


# Function to scrape playlist and extract the HTML
def get_html(playlist_url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(playlist_url)
    return driver.page_source


def scrape_playlist(playlist_html):
    song_urls = []

    # Parse the playlist HTML with BeautifulSoup
    parser = etree.HTMLParser()
    soup = BeautifulSoup(playlist_html, "lxml", parser=parser)

    # find all the song objects
    tracks = select(
        "a.trackItem__trackTitle.sc-link-dark.sc-link-primary.sc-font-light", soup
    )
    for track in tracks:
        href = track.get("href")
        if href:
            # get the song urls
            full_url = "https://soundcloud.com" + href.split("?")[0]
            song_urls.append(full_url)
        else:
            print("Warning: href attribute not found.")

    return song_urls


def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Scrape a SoundCloud playlist and download the songs."
    )

    parser.add_argument(
        "-p", "--playlist_url", help="URL of the playlist", required=True
    )
    args = parser.parse_args()

    return args


def main():
    # Get commmand line args
    args = parse_args()

    # Sget the HTML content of the playlist
    playlist_html = get_html(args.playlist_url)

    if playlist_html:
        # Scrape the playlsit to extract song URLS
        song_urls = scrape_playlist(playlist_html)

        for url in song_urls:
            print(url)
    else:
        print("Failed to retrieve playlist information")


if __name__ == "__main__":
    main()

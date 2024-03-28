import argparse

from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from soupsieve import select
from webdriver_manager.chrome import ChromeDriverManager


# Function to scrape playlist and extract the HTML
def get_html(playlist_url):
    options = Options()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(
        options=options, service=ChromeService(ChromeDriverManager().install())
    )
    driver.get(playlist_url)
    wait_until_class_count_exceeds(driver)
    return driver.page_source


def wait_until_class_count_exceeds(driver):
    accept_cookies(driver)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    try:
        WebDriverWait(driver, 10).until(
            lambda driver: len(
                driver.find_elements(
                    By.CSS_SELECTOR,
                    ".li.trackList__item.sc-border-light-bottom.sc-px-2x",
                )
            )
            > 35
        )
    except TimeoutException:
        print("All 35 tracks not found.")


def accept_cookies(driver):
    try:
        # Wait for the cookies button to be clickable
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )

        # Click the button
        button.click()
    except Exception as e:
        print(f"Error: {e}")


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


def scroll_to_bottom(driver):
    # Get the body element
    body = driver.find_element


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
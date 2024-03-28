import argparse

import requests
from bs4 import BeautifulSoup


# Function to scrape playlist and extract the HTML
def get_html(playlist_url):
    # Make the request to retrieve playlist information
    playlist_response = requests.get(f"{playlist_url}")

    # Check if the request was successful
    if playlist_response.status_code == 200:
        # Parse the JSON response
        playlist_data = playlist_response.text
        print(playlist_data)

        return playlist_data
    else:
        print("Failed to retrieve playlist information")


def scrape_playlist(playlist_html):
    song_urls = []

    # Parse the playlist HTML with BeautifulSoup
    soup = BeautifulSoup(playlist_html, "html.parser")

    # find all the song objects
    tracks = soup.select("a.trackItem__trackTitle")
    print("Number of tracks found:", len(tracks))

    for track in tracks:
        href = track.get("href")
        print("Extracted href:", href)
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

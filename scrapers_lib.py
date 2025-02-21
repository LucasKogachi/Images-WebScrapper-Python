import general_lib
import requests               # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
# pip install html5lib, BeatifulSoup needs it, but no need to import

def url_match(url: str, match_list: list[str]): # many sites
    for match in match_list:
        if url.find(match) != -1:
            return True
    return False

####################################################################################################
###########################################   Scrapers   ###########################################

def mangakakalot_scraper(url: str, dest_path: str):
    header = {}
    if url.find("chapmanganato") != -1:
        header = {"Referer": "https://chapmanganato.to/"}
    else:      # mangakakalot
        header = {"Referer": "https://mangakakalot.com/"}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html5lib")
    gallery = soup.find("div", {"class": "container-chapter-reader"})
    children = gallery.findChildren("img", recursive = False)
    count = 1
    for child in children:
        url = child.get("src")
        general_lib.download_img(url, count, dest_path, header)
        count += 1
    delay = general_lib.get_delay()
    general_lib.run_delay(count * delay[0], count * delay[1])

####################################################################################################
###########################################   Selector   ###########################################

def site_scrap(url: str, dest_path: str):
    if   url_match(url, ["chapmanganato", "mangakakalot"]):
        mangakakalot_scraper(url, dest_path)
    else:
        general_lib.error_log("No Scraper for " + url, dest_path)

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
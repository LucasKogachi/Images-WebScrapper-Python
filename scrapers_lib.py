import general_lib
from general_lib import FolderNumber # class
import requests                      # pip install requests
from bs4 import BeautifulSoup        # pip install beautifulsoup4
# pip install html5lib, BeatifulSoup needs it, but no need to import

def url_match(url: str, match_list: list[str]): # many sites
    for match in match_list:
        if url.find(match) != -1:
            return True
    return False

####################################################################################################
###########################################   Scrapers   ###########################################

def mangakakalot_scraper(url: str, download_folder_number: int):
    # entire manga
    if url.find("chapter") == -1:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html5lib")
        gallery = soup.find("ul", {"class": "row-content-chapter"})
        children = gallery.findChildren("a", recursive = True)
        chapters = []
        for child in children:
            chapter = child.get("href")
            chapters.append(chapter)
        chapters.reverse()
        if chapters:
            start = download_folder_number + 1
            for chapter in chapters[1:]:
                new_folder = general_lib.get_folder_path(start)
                general_lib.create_folder(new_folder)
                general_lib.add_lines_to_file([chapter], new_folder, general_lib.URL_FILE)
                start += 1
            url = chapters[0]

    # chapter
    dest_path = general_lib.get_folder_path(download_folder_number)
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

def site_scrap(url: str, download_folder_number: int):
    if   url_match(url, ["chapmanganato", "mangakakalot"]):
        mangakakalot_scraper(url, download_folder_number)
    else:
        general_lib.error_log("No Scraper for " + url)

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
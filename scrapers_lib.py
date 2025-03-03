import general_lib
import settings_lib
from fn import FolderNumber # class
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

def mangakakalot_headers(url: str):
    if   url.find("mangakakalot.com")  != -1:
        return {"Referer": "https://mangakakalot.com/"}
    elif url.find("chapmanganato.to")  != -1:
        return {"Referer": "https://chapmanganato.to/"}
    elif url.find("chapmanganelo.com") != -1:
        return {"Referer": "https://chapmanganelo.com/"}
    elif url.find("natomanga.com")     != -1:
        return {"Referer": "https://www.natomanga.com/"}
    elif url.find("mangakakalot.gg")   != -1:
        return {"Referer": "https://www.mangakakalot.gg/"}
    return {}

def mangakakalot_manga(url: str, folder_numbers: FolderNumber):
    general_lib.warning("ONGOING Planning, Don't use this function, until its finished")
    if url.find("chapter") != -1:
        return url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html5lib")
    if url.find("mangakakalot") != -1:
        gallery = soup.find("ul", {"class": "row-content-chapter"})
    else:
        gallery = soup.find("div", {"class": "chapter-list"})
    children = gallery.findChildren("a", recursive = True)
    chapters = []
    for child in children:
        chapter = child.get("href")
        chapters.append(chapter)
    chapters.reverse()
    if chapters:
        folder_numbers.planning += 1
        for chapter in chapters[1:]:
            new_folder = folder_numbers.get_planning_path()
            general_lib.create_folder(new_folder)
            general_lib.add_lines_to_file([chapter], new_folder, general_lib.URL_FILE)
            folder_numbers.planning += 1
        url = chapters[0]
    general_lib.warning("Planning FINISHED, You can use it again")
    return url

def mangakakalot_chapter(url: str, folder_numbers: FolderNumber):
    dest_path = folder_numbers.get_download_path()
    header = mangakakalot_headers(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html5lib")
    gallery = soup.find("div", {"class": "container-chapter-reader"})
    children = gallery.findChildren("img", recursive = False)
    count = 1
    for child in children:
        url = child.get("src")
        general_lib.download_img(url, count, dest_path, header)
        count += 1
    settings = settings_lib.get_settings()
    general_lib.run_delay(count * settings["min_delay"], count * settings["max_delay"])

def mangakakalot_scraper(url: str, folder_numbers: FolderNumber):
    url = mangakakalot_manga(url, folder_numbers)
    mangakakalot_chapter(url, folder_numbers)

####################################################################################################
###########################################   Selector   ###########################################

def site_scrap(url: str, folder_numbers: FolderNumber):
    mangakakalot_matches = ["mangakakalot", "manganato", "manganelo", "natomanga"]
    if   url_match(url, mangakakalot_matches):
        mangakakalot_scraper(url, folder_numbers)
    else:
        general_lib.error_log("No Scraper for " + url)

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
import general_lib
import settings_lib
from fn import FolderNumber # class
import requests                      # pip install requests
from bs4 import BeautifulSoup        # pip install beautifulsoup4
# pip install html5lib, BeatifulSoup needs it, but no need to import
import re

def url_match(url: str, match_list: list[str]): # many sites
    for match in match_list:
        if url.find(match) != -1:
            return True
    return False

####################################################################################################
###########################################   Scrapers   ###########################################

def natomanga_manga(url: str, folder_numbers: FolderNumber):
    if url.find("chapter") != -1:
        return url
    general_lib.warning("ONGOING Planning, Don't use this function, until its finished")
    for _ in range(3):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html5lib")
            gallery = soup.find("div", {"class": "chapter-list"})
            children = gallery.find_all("a", recursive = True)
            break
        except:
            general_lib.run_delay(3, 3)
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

def natomanga_chapter(url: str, folder_numbers: FolderNumber):
    dest_path = folder_numbers.get_download_path()
    header = {"Referer": "https://www.natomanga.com/"}
    for _ in range(3):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html5lib")
            gallery = soup.find("div", {"class": "container-chapter-reader"})
            children = gallery.find_all("img", recursive = False)
            break
        except:
            general_lib.run_delay(3, 3)
    count = 1
    for child in children:
        url = child.get("src")
        if url.find("virus") != -1: # found
            onerror = child.get("onerror")
            url = re.search(r"this.src='(.*?)'", onerror)
            if url:
                url = url.group(1)
            else:
                print(child)
        print(url)
        general_lib.download_img(url, count, dest_path, header)
        count += 1
    settings = settings_lib.get_settings()
    general_lib.run_delay(count * settings["min_delay"], count * settings["max_delay"])

def natomanga_scraper(url: str, folder_numbers: FolderNumber):
    url = natomanga_manga(url, folder_numbers)
    natomanga_chapter(url, folder_numbers)

####################################################################################################
###########################################   Selector   ###########################################

def site_scrap(url: str, folder_numbers: FolderNumber):
    if   url_match(url, ["natomanga"]):
        natomanga_scraper(url, folder_numbers)
    else:
        general_lib.error_log("No Scraper for " + url)

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
import images_lib
import requests
import time, random, os, shutil
from bs4 import BeautifulSoup # pip install beautifulsoup4
# pip install html5lib, BeatifulSoup needs it, but no need to import

DELAY_FILE = "delay.txt"
MIN_DELAY_TIME = 10.0 # seconds
MAX_DELAY_TIME = 15.0 # seconds

def url_match(url: str, match_list: list[str]): # many sites
    for match in match_list:
        if url.find(match) != -1:
            return True
    return False

def float_to_str(number: float, max_cases: int):
    number_str = str(number)
    x = number_str.rfind(".")
    if max_cases > 0 and x != -1:
        return number_str[:(x + 1 + max_cases)]
    return number_str

####################################################################################################
############################################   Delay   #############################################

def set_delay(min_delay: float, max_delay: float):
    f = open(DELAY_FILE, "w")
    f.write(str(min_delay) + "\n")
    f.write(str(max_delay) + "\n")
    f.close()

def get_delay():
    if os.path.isfile(DELAY_FILE):
        f = open(DELAY_FILE, "r")
        min_delay = float(f.readline().strip())
        max_delay = float(f.readline().strip())
        f.close()
        return [min_delay, max_delay]
    else:
        set_delay(MIN_DELAY_TIME, MAX_DELAY_TIME)
        return [MIN_DELAY_TIME, MAX_DELAY_TIME]

def run_delay(min_delay: float, max_delay: float):
    # Trying to avoid IP Block, by lots of requests
    delay = random.uniform(min_delay, max_delay)
    print("Delay(seconds): " + float_to_str(delay, 2))
    time.sleep(delay)

####################################################################################################
###########################################   Download   ###########################################

def download_img(url: str, img_number: int, dest_path: str, headers: dict = {}):
    img_name = images_lib.get_img_name(img_number)
    x = url.rfind(".")                                     # getting extension
    img_file = dest_path + img_name + url[x:].lower()
    r = requests.get(url, stream = True, headers=headers)  # stream, no interruptions
    if r.status_code == 200:
        with open(img_file, 'wb') as file:
            r.raw.decode_content = True               # force decompress, instead from request
            shutil.copyfileobj(r.raw, file)           # stream the data to a file object
        print(img_file + " Created Successfully")
        images_lib.verify_img_extension(img_file, dest_path)
    else:
        images_lib.error_log("Download " + img_file, dest_path)

####################################################################################################
###########################################   Scrapers   ###########################################

def mangakakalot_scraper(url: str, dest_path: str, min_delay: float, max_delay: float):
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
        download_img(url, count, dest_path, header)
        count += 1
    run_delay(count * min_delay, count * max_delay)

####################################################################################################
###########################################   Selector   ###########################################

def site_scrap(url: str, dest_path: str, min_delay: float, max_delay: float):
    if   url_match(url, ["chapmanganato", "mangakakalot"]):
        mangakakalot_scraper(url, dest_path, min_delay, max_delay)
    else:
        images_lib.error_log("No Scraper for " + url, dest_path)

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
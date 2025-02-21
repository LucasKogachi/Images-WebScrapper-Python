import os, random, time, shutil
from PIL import Image # pip install pillow
import requests       # pip install requests

####################################################################################################
############################################   Errors   ############################################

ERROR_FILE  = "errors.txt"

def error_log(msg: str, path: str = ""):
    error = "ERROR: " + msg
    f = open(path + ERROR_FILE, "a")
    f.write(error + "\n")
    f.close()
    print(error)

####################################################################################################
######################################   Folder Management   #######################################

def create_folder(path: str):
    if not os.path.exists(path):
        os.mkdir(path)

def remove_folder(path: str):
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except:
            error_log("Deleting Folder, Remaining Files in " + path)

####################################################################################################
###########################################   Strings   ############################################

def get_img_name(number: int, img_zfill: int = 3):
    return str(number).zfill(img_zfill)

def get_folder_path(number: int, dir_zfill: int = 4):
    return str(number).zfill(dir_zfill) + "/"

def float_to_str(number: float, max_cases: int): # trunc
    number_str = str(number)
    x = number_str.rfind(".")
    if max_cases > 0 and x != -1:
        return number_str[:(x + 1 + max_cases)]
    return number_str

####################################################################################################
#####################################   Text/File Management   #####################################
    
def add_lines_to_file(lines: list[str], path: str, file: str):
    if lines:
        f = open(path + file, "a")
        for line in lines:
            f.write(line + "\n")
        f.close()

def get_lines_from_file(path: str, file: str):
    lines = []
    if os.path.isfile(path + file):
        f = open(path + file, "r")
        line = f.readline().strip()
        while line:
            lines.append(line)
            line = f.readline().strip()
        f.close()
        os.remove(path + file)
    return lines

def remove_1x_line_from_file(path: str, file: str):
    line = ""
    lines = get_lines_from_file(path, file)
    if lines:
        line = lines[0]
        add_lines_to_file(lines[1:], path, file)
    return line

def reattach_line_to_file(line: str, path: str, file: str):
    lines = get_lines_from_file(path, file)
    lines = [line] + lines
    add_lines_to_file(lines, path, file)

####################################################################################################
############################################   Delay   #############################################

DELAY_FILE = "delay.txt"
MIN_DELAY_TIME = 4.0 # seconds
MAX_DELAY_TIME = 8.0 # seconds

def set_delay(min_delay: float, max_delay: float):
    f = open(DELAY_FILE, "w")
    f.write(str(min_delay) + "\n")
    f.write(str(max_delay) + "\n")
    f.close()

def get_delay():
    if os.path.isfile(DELAY_FILE):
        f = open(DELAY_FILE, "r")
        try:
            min_delay = float(f.readline().strip())
            max_delay = float(f.readline().strip())
        except:
            error_log("Reading Delay File")
            min_delay = MIN_DELAY_TIME
            max_delay = MAX_DELAY_TIME
        f.close()
        return [min_delay, max_delay]
    else:
        print("oi")
        set_delay(MIN_DELAY_TIME, MAX_DELAY_TIME)
        return [MIN_DELAY_TIME, MAX_DELAY_TIME]

def run_delay(min_delay: float, max_delay: float):
    # Trying to avoid IP Block, by lots of requests
    delay = random.uniform(min_delay, max_delay)
    print("Delay(seconds): " + float_to_str(delay, 2))
    time.sleep(delay)

####################################################################################################
###########################################   Download   ###########################################

def verify_img_extension(img_file: str, path: str):
    x = img_file.rfind(".")
    img_extension = img_file[(x+1):]
    try:
        with Image.open(img_file) as img:
            new_extension = img.format.lower()
            img.verify()
            if new_extension == "jpeg":
                new_extension = "jpg"
        if img_extension != new_extension:
            new_img_file_name = img_file[:(x+1)] + new_extension
            os.rename(img_file, new_img_file_name)
            print(new_img_file_name + " Extension Renamed")
    except:
        error_log("Image " + img_file, path)

def download_img(url: str, img_number: int, dest_path: str, headers: dict = {}):
    img_name = get_img_name(img_number)
    x = url.rfind(".")                                     # getting extension
    img_file = dest_path + img_name + url[x:].lower()
    r = requests.get(url, stream = True, headers=headers)  # stream, no interruptions
    if r.status_code == 200:
        with open(img_file, 'wb') as file:
            r.raw.decode_content = True           # force decompress, instead from request
            shutil.copyfileobj(r.raw, file)       # stream the data to a file object
        print(img_file + " Created Successfully")
        verify_img_extension(img_file, dest_path)
    else:
        error_log("Download " + img_file, dest_path)

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
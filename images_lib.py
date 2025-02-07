import os, shutil, glob
import requests
from PIL import Image # pip install pillow
import math
import fitz           # pip install pymupdf

#   Images
# 1 Named with 001, 002, 003 and so on ...
# 2 Easier to sort
# 3 See .zfill in get_img_name()

#   Steps
# 1 Download, Convert, Resize
# 2 Create PDF

TEMP_FOLDER = "Temp/"           # dont forget "/" at the end, if not empty
ERROR_FILE  = "errors.txt"
EXTENSIONS  = ["png", "webp"]   # to convert to jpg
MARGIN = 0.1                    # % safety margin, resize(bytes)
MAX_IMG_SIZE = 600000           # image size, bytes

def error_log(msg: str, path = ""):
    error = "ERROR: " + msg
    f = open(path + ERROR_FILE, "a")
    f.write(error + "\n")
    f.close()
    print(error)

def get_img_name(number: int):
    return str(number).zfill(3)

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

def download_img(url: str, img_number: int, dest_path: str):
    img_name = get_img_name(img_number)
    x = url.rfind(".")                                # getting extension
    img_file = dest_path + img_name + url[x:].lower()
    r = requests.get(url, stream = True)              # stream, no interruptions
    if r.status_code == 200:
        with open(img_file, 'wb') as file:
            r.raw.decode_content = True               # force decompress, instead from request
            shutil.copyfileobj(r.raw, file)           # stream the data to a file object
        print(img_file + " Created Successfully")
        verify_img_extension(img_file, dest_path)
    else:
        error_log("Download " + img_file, dest_path)

####################################################################################################
########################################   Convert Image   #########################################

def convert_all_to_jpg(path: str, extensions = EXTENSIONS):
    for extension in extensions:
        x = len(extension)
        for file in glob.glob(path + "*." + extension):
            try:
                with Image.open(file) as img:
                    img_rgb = img.convert('RGB')
                    img_rgb.save(file[:(-x)] + "jpg", optimize = True, quality = 95)
                os.remove(file)
            except:
                if os.path.isfile(file[:(-x)] + "jpg"):
                    os.remove(file[:(-x)] + "jpg")
                error_log("Conversion of " + file + " to jpg", path)

####################################################################################################
###################################   Image/Folder Management   ####################################

def create_folder(path: str):
    if not os.path.exists(path):
        os.mkdir(path)

def remove_folder(path: str):
    if os.path.isdir(path):
        try:
            os.rmdir(path)
        except:
            error_log("Deleting Folder, Remaining Files in " + path)

def remove_jpgs(path: str, jpgs_list = []):
    if jpgs_list: # not empty
        files = jpgs_list
    else:
        files = glob.glob(path + "*.jpg")
    for file in files:
        if os.path.isfile(file): # sometimes list something already deleted
            try:
                os.remove(file)
            except:
                error_log("Deleting" + file, path)

def move_jpgs(src_path: str, dest_path: str):
    x = len(src_path)
    for file in glob.glob(src_path + "*.jpg"):
        try:
            shutil.move(file, dest_path + file[x:])
        except:
            error_log("Moving " + file, dest_path)

def rename_jpgs(path: str, start = 1): # not using
    create_folder(path + TEMP_FOLDER)
    N = start
    for file in sorted(glob.glob(path + "*.jpg")):
        try:
            shutil.move(file, path + TEMP_FOLDER + get_img_name(N) + ".jpg")
            N += 1
        except:
            error_log("Renaming " + file, path)
    move_jpgs(path + TEMP_FOLDER, path)
    remove_folder(path + TEMP_FOLDER)

####################################################################################################
########################################   Resize Images   #########################################

def get_avg_img_size(path: str):
    somador = 0
    count = 0
    for file in glob.glob(path + "*.jpg"):
        somador += os.path.getsize(file)
        count += 1
    if count == 0:
        return 0
    return somador/count

def get_resize_coef(percentage: float, margin: float): # 0 < percentage < 1
    if percentage - margin > 0:
        return math.sqrt(percentage - margin)
    return math.sqrt(percentage)

def new_img_size(coefficient: float, img_size: list):
    width  = int(round(coefficient * img_size[0]))
    height = int(round(coefficient * img_size[1]))
    return [width, height]

def resize_x1(path: str, coefficient: float):
    x = len(path)
    for file in glob.glob(path + "*.jpg"):
        try:
            with Image.open(file) as img:
                img.thumbnail(new_img_size(coefficient, img.size), Image.ANTIALIAS)
                img.save(path + TEMP_FOLDER + file[x:], optimize = True, quality = 95)
        except:
            error_log("Resize of " + file, path)
    remove_jpgs(path)
    move_jpgs(path + TEMP_FOLDER, path)

def resize_jpgs(path: str, max_img_size = MAX_IMG_SIZE, margin = MARGIN):
    create_folder(path + TEMP_FOLDER)
    avg_img_size = get_avg_img_size(path)
    while avg_img_size > max_img_size:
        coefficient = get_resize_coef(max_img_size/avg_img_size, margin)
        resize_x1(path, coefficient)
        avg_img_size = get_avg_img_size(path)
    remove_folder(path + TEMP_FOLDER)

####################################################################################################
#############################################   PDF   ##############################################

def get_jpgs_list(path: str, start: int, end: int):
    jpgs = glob.glob(path + "*.jpg")
    if start < 0 or end < 0:
        return sorted(jpgs)
    files = []
    names_list = [path + get_img_name(x) + ".jpg" for x in range(start, end+1)]
    for name in names_list:
        if name in jpgs:
            files.append(name)
    return files

def convert_jpgs_to_pdf(path: str, pdf_name: str, start = -1, end = -1):
    files = get_jpgs_list(path, start, end)
    imgs = []
    for file in files:
        try:
            img = Image.open(file)
            imgs.append(img)
        except:
            error_log("PDF -> Opening Image " + file, path)
    if imgs: # not empty
        pdf_file = path + pdf_name + ".pdf"
        try:
            imgs[0].save(pdf_file, resolution = 100, save_all = True, append_images = imgs[1:])
            print(pdf_file + " Created Successfully")
        except:
            error_log("Creating PDF " + pdf_file, path)
        for img in imgs:
            img.close()
        remove_jpgs(path, files)

def merge_pdfs(path: str, pdf_name: str):
    pdf_file = path + pdf_name + ".pdf"
    try:
        pdf = fitz.open()
        for file in sorted(glob.glob(path + "*.pdf")):
            pdf.insert_file(file)
            os.remove(file)
        pdf.save(pdf_file)
        pdf.close()
        print(pdf_file + " Merged Successfully")
    except:
        error_log("Merging PDF " + pdf_file, path)

def split_pdf(path: str, pdf_name: str, split1: str, split2: str, split2_start_page: int):
    pdf_file  = path + pdf_name + ".pdf"
    pdf1_file = path + split1   + ".pdf"
    pdf2_file = path + split2   + ".pdf"
    if split2_start_page > 1:
        try:
            pdf1 = fitz.open()
            pdf2 = fitz.open()
            pdf1.insert_file(pdf_file, to_page   = split2_start_page-2)
            pdf2.insert_file(pdf_file, from_page = split2_start_page-1)
            os.remove(pdf_file)
            pdf1.save(pdf1_file)
            pdf2.save(pdf2_file)
            pdf1.close()
            pdf2.close()
            print(pdf_file + " Split Successful")
        except:
            error_log("Splitting PDF " + pdf_file, path)

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
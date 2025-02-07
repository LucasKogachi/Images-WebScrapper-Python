import images_lib
import archives_lib
import os

DEFAULT_FOLDER_NUMBER = 1 # starting folder number
URL_FILE    = "url.txt"
TITLES_FILE = "title.txt" # save titles for PDF

class FolderNumber:
    def __init__(self):
        self.planning = DEFAULT_FOLDER_NUMBER
        self.download = DEFAULT_FOLDER_NUMBER
        self.working  = DEFAULT_FOLDER_NUMBER

def get_input(msg: str):
    return input(msg).strip()

def get_folder_path(number: int):
    return str(number).zfill(2) + "/"

####################################################################################################
####################################   Text/Folder Management   ####################################

def create_folder(path: str):
    if not os.path.exists(path):
        os.mkdir(path)
    
def add_lines_to_file(lines: list, path: str, file: str):
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
########################################   Plan Download   #########################################

def plan_download_menu(folder_numbers: FolderNumber):
    while True:
        print("\nPress ENTER to exit/skip")
        print("Plan Download Folder Number: " + str(folder_numbers.planning))
        url = get_input("URL: ")
        if url == "":
            break
        plan_folder_path = get_folder_path(folder_numbers.planning)
        folder_numbers.planning += 1
        create_folder(plan_folder_path)
        add_lines_to_file([url], plan_folder_path, URL_FILE)
        msg = "Add New Folder in " + plan_folder_path + " (optional): "
        new_folder = get_input(msg)
        if new_folder: # != ""
            create_folder(plan_folder_path + new_folder + "/")
        print("Add PDF Titles (optional)")
        titles = []
        title_number = 1
        while True:
            title = get_input("Title (" + str(title_number) + "): ")
            if title:
                titles.append(title)
                title_number += 1
            else:
                add_lines_to_file(titles, plan_folder_path, TITLES_FILE)
                break

####################################################################################################
###########################################   Download   ###########################################



####################################################################################################
#############################################   PDF   ##############################################

def pdf_menu_options(folder_numbers: FolderNumber):
    print("\nPDF Menu, Working Folder: " + str(folder_numbers.working))
    print("1 - Convert ALL jpgs to PDF")
    print("2 - Convert PART of jpgs to PDF")
    print("3 - Next Working Folder")
    print("4 - Merge PDFs")
    print("5 - Split PDF")
    print("X - Exit")
    option = get_input("\nChosen Option: ")
    print()
    return option

def convert_all_jpgs_to_pdf(path: str):
    pdf_name = remove_1x_line_from_file(path, TITLES_FILE)
    if pdf_name:
        print("PDF Name (" + TITLES_FILE + "): " + pdf_name)
    else:
        pdf_name = get_input("PDF Name: ")
        if pdf_name == "":
            return
    images_lib.convert_jpgs_to_pdf(path, pdf_name)

def convert_part_jpgs_to_pdf(path: str):
    start = 0
    while True:
        pdf_name = remove_1x_line_from_file(path, TITLES_FILE)
        if pdf_name:
            print("\nPDF Name (" + TITLES_FILE + "): " + pdf_name)
        else:
            pdf_name = get_input("\nPDF Name: ")
            if pdf_name == "":
                break
        msg = "Start Page(" + images_lib.get_img_name(start) + "): "
        new_start = get_input(msg)
        try:
            new_start = int(new_start)
            if new_start > -1:
                start = new_start
        except:
            pass
        end = get_input("End Page: ")
        try:
            end = int(end)
            if end < start:
                reattach_line_to_file(pdf_name, path, TITLES_FILE)
                break
            images_lib.convert_jpgs_to_pdf(path, pdf_name, start, end)
            start = end + 1
        except:
            reattach_line_to_file(pdf_name, path, TITLES_FILE)
            break

def merge_pdfs(path: str):
    pdf_name = get_input("Merged PDF Name: ")
    if pdf_name:
        images_lib.merge_pdfs(path, pdf_name)

def split_pdf(path: str):
    pdf_name = get_input("PDF to Split: ")
    split1   = get_input("Split1 Name [1, N[: ")
    split2   = get_input("Split2 Name [N,  ]: ")
    N = get_input("N: ")
    try:
        N = int(N)
        if pdf_name and split1 and split2:
            images_lib.split_pdf(path, pdf_name, split1, split2, N)
    except:
        pass

def pdf_menu(folder_numbers: FolderNumber):
    while True:
        working_folder_path = get_folder_path(folder_numbers.working)
        option = pdf_menu_options(folder_numbers)
        if   option == "1": # convert all
            convert_all_jpgs_to_pdf(working_folder_path)
        elif option == "2": # convert part
            convert_part_jpgs_to_pdf(working_folder_path)
        elif option == "3": # next working folder
            folder_numbers.working += 1
        elif option == "4": # merge pdfs
            merge_pdfs(working_folder_path)
        elif option == "5": # split pdf
            split_pdf(working_folder_path)
        else:
            break

####################################################################################################
###########################################   Archives   ###########################################

def archives_menu_options(folder_numbers: FolderNumber):
    print("\nArchives Menu, Working Folder: " + str(folder_numbers.working))
    print("1 - Update Maps from Archive")
    print("2 - Update Map from Working Folder")
    print("3 - Create Archive")
    print("X - Exit")
    option = get_input("\nChosen Option: ")
    print()
    return option

def archives_menu(folder_numbers: FolderNumber):
    while True:
        working_folder_path = get_folder_path(folder_numbers.working)
        option = archives_menu_options(folder_numbers)
        if   option == "1": # update archive
            archives_lib.update_archive()
            print("Archive Maps Updated")
        elif option == "2": # update working folder
            archives_lib.update_map(working_folder_path)
            print("Working Folder Map Updated")
        elif option == "3": # create archive
            archives_lib.create_archive()
            print("Archive Created")
        else:
            break

####################################################################################################
######################################   Set Folder Number   #######################################

def folder_number_menu_options(folder_numbers: FolderNumber):
    print("\nFolder Number Menu")
    print("1 - Set PLANNING Folder Number (" + str(folder_numbers.planning) + ")")
    print("2 - Set DOWNLOAD Folder Number (" + str(folder_numbers.download) + ")")
    print("3 - Set WORKING Folder Number ("  + str(folder_numbers.working)  + ")")
    print("X - Exit")
    option = get_input("\nChosen Option: ")
    print()
    return option

def set_folder_number(previous_number: int):
    number = get_input("New Folder Number: ")
    try:
        number = int(number)
        if number < 0:
            number = previous_number
    except:
        number = previous_number
    return number

def folder_number_menu(folder_numbers: FolderNumber):
    while True:
        option = folder_number_menu_options(folder_numbers)
        if   option == "1": # set PLANNING folder
            print("PLANNING Folder Number: " + str(folder_numbers.planning))
            folder_numbers.planning = set_folder_number(folder_numbers.planning)
        elif option == "2": # set DOWNLOAD  folder
            print("DOWNLOAD Folder Number: " + str(folder_numbers.download))
            folder_numbers.download = set_folder_number(folder_numbers.download)
        elif option == "3": # set WORKING  folder
            print("WORKING Folder Number: "  + str(folder_numbers.working))
            folder_numbers.working  = set_folder_number(folder_numbers.working)
        else:
            break

####################################################################################################
#############################################   Main   #############################################

def main_menu_options():
    print("\nWeb Scraping")
    print("1 - Plan Download")                      # OK
    print("2 - Start Planned Download")
    print("3 - PDF")                                # OK
    print("4 - Archives")                           # OK
    print("5 - Set Folder Numbers")                 # OK
    print("X - Exit")                               # OK
    option = get_input("\nChosen option: ")
    print()
    return option

def main_menu():
    folder_numbers = FolderNumber()
    while True:
        option = main_menu_options()
        if   option == "1": # plan download
            plan_download_menu(folder_numbers)
        elif option == "2": # scrapers
            return
        elif option == "3": # pdf
            pdf_menu(folder_numbers)
        elif option == "4": # archives
            archives_menu(folder_numbers)
        elif option == "5": # set folder numbers
            folder_number_menu(folder_numbers)
        else:               # exit
            break

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
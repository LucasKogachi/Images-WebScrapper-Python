import os, re

ARCHIVE = "Archive/"
FOLDERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIAL = "0-9/"
MIXED   = "ZMixed/"
MAP     = "Map.txt"
TEMP1   = "Temp1.txt"
TEMP2   = "Temp2.txt"
PREFIX  = "    "

def create_archive():
    if not os.path.exists(ARCHIVE):
        os.mkdir(ARCHIVE)
    if not os.path.exists(ARCHIVE + SPECIAL):
        os.mkdir(ARCHIVE + SPECIAL)
    if not os.path.exists(ARCHIVE + MIXED):
        os.mkdir(ARCHIVE + MIXED)
    for X in FOLDERS:
        if not os.path.exists(ARCHIVE + X + "/"):
            os.mkdir(ARCHIVE + X + "/")
        if not os.path.exists(ARCHIVE + X + "/" + SPECIAL):
            os.mkdir(ARCHIVE + X + "/" + SPECIAL)
        for Y in FOLDERS:
            if not os.path.exists(ARCHIVE + X + "/" + Y + "/"):
                os.mkdir(ARCHIVE + X + "/" + Y + "/")

####################################################################################################
#############################################   Map   ##############################################

# Use update_map() or update_archive() in this section

def recursive_map(path: str, element: str, prefix = ""):    # element = folder name or pdf name
    if os.path.isdir(path + element): # folder
        i_map = [prefix + element]
        prefix += PREFIX
        for i in sorted(os.listdir(path + element)):
            j_map = recursive_map(path + element + "/", i, prefix)
            for j in j_map:
                i_map.append(j)
        return i_map
    else:                             # pdf file
        if re.search(r"pdf$", element):
            return [prefix + element]
        return []

def map_generator(path: str, map_name: str):
    f = open(path + map_name, "w")
    for i in sorted(os.listdir(path)):
        i_map = recursive_map(path, i)
        for j in i_map:
            f.write(j + "\n")
    f.close()

def update_map(path: str):
    if not os.path.isfile(path + MAP): # MAP doesnt exist
        map_generator(path, MAP)
        return
    os.rename(path + MAP, path + TEMP1)
    map_generator(path, TEMP2)
    f_map   = open(path + MAP  , "w")
    f_temp1 = open(path + TEMP1, "r")
    f_temp2 = open(path + TEMP2, "r")
    l_temp1 = f_temp1.readline()
    l_temp2 = f_temp2.readline()
    while l_temp1 and l_temp2:
        if l_temp1 < l_temp2:
            f_map.write(l_temp1)
            l_temp1 = f_temp1.readline()
        elif l_temp1 == l_temp2:
            f_map.write(l_temp1)
            l_temp1 = f_temp1.readline()
            l_temp2 = f_temp2.readline()
        else:
            f_map.write(l_temp2)
            l_temp2 = f_temp2.readline()
    while l_temp1:
        f_map.write(l_temp1)
        l_temp1 = f_temp1.readline()
    while l_temp2:
        f_map.write(l_temp2)
        l_temp2 = f_temp2.readline()
    f_map.close()
    f_temp1.close()
    f_temp2.close()
    os.remove(path + TEMP1)
    os.remove(path + TEMP2)

def update_archive(): # doesnt verify if archive exists
    for i in os.listdir(ARCHIVE + SPECIAL):
        if os.path.isdir(ARCHIVE + SPECIAL + i):
            update_map(ARCHIVE + SPECIAL + i + "/")
    for i in os.listdir(ARCHIVE + MIXED):
        if os.path.isdir(ARCHIVE + MIXED + i):
            update_map(ARCHIVE + MIXED + i + "/")
    for i in FOLDERS:
        for j in os.listdir(ARCHIVE + i + "/" + SPECIAL):
            if os.path.isdir(ARCHIVE + i + "/" + SPECIAL + j):
                update_map(ARCHIVE + i + "/" + SPECIAL + j + "/")
        for j in FOLDERS:
            for k in os.listdir(ARCHIVE + i + "/" + j):
                if os.path.isdir(ARCHIVE + i + "/" + j + "/" + k):
                    update_map(ARCHIVE + i + "/" + j + "/" + k + "/")

####################################################################################################
#############################################   Test   #############################################
# put "/" at the end if its not empty, only "/" is root and ("." or "./") is where youre working
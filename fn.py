import os

FN_FILE = "fn.txt"
DEFAULT_FOLDER_NUMBER = 1 # starting folder number
PLANNING = 0
DOWNLOAD = 1
WORKING  = 2

class FolderNumber:
    def __init__(self):
        if os.path.isfile(FN_FILE):
            values = get_fn_values()
            self.planning = values[PLANNING]
            self.download = values[DOWNLOAD]
            self.working  = values[WORKING]
        else:
            self.planning = DEFAULT_FOLDER_NUMBER
            self.download = DEFAULT_FOLDER_NUMBER
            self.working  = DEFAULT_FOLDER_NUMBER
    
    def get_planning_path(self):
        return get_folder_path(self.planning)
    
    def get_download_path(self):
        return get_folder_path(self.download)
    
    def get_working_path(self):
        return get_folder_path(self.working)

    def save(self):
        if os.path.isfile(FN_FILE):
            values = get_fn_values()
            save_fn_values(self, values)
        else:
            save_fn_values(self)
    
    def reset(self):
        self.planning = DEFAULT_FOLDER_NUMBER
        self.download = DEFAULT_FOLDER_NUMBER
        self.working  = DEFAULT_FOLDER_NUMBER
        save_fn_values(self)

def get_folder_path(number: int, dir_zfill: int = 4):
    return str(number).zfill(dir_zfill) + "/"

def get_fn_values():
    f = open(FN_FILE, "r")
    planning = int(f.readline().strip())
    download = int(f.readline().strip())
    working  = int(f.readline().strip())
    f.close()
    return [planning, download, working]

def save_fn_values(self: FolderNumber, values: list[int] = [0, 0, 0]):
    f = open(FN_FILE, "w")
    if self.planning > values[PLANNING]:
        f.write(str(self.planning) + "\n")
    else:
        f.write(str(values[PLANNING]) + "\n")
    if self.download > values[DOWNLOAD]:
        f.write(str(self.download) + "\n")
    else:
        f.write(str(values[DOWNLOAD]) + "\n")
    if self.working > values[WORKING]:
        f.write(str(self.working) + "\n")
    else:
        f.write(str(values[WORKING]) + "\n")
    f.close()
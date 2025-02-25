import general_lib
import os

SETTINGS_FILE = "settings.txt"
DEFAULT_SETTINGS = {
    "min_delay": 4.0, # seconds
    "max_delay": 8.0, # seconds
    "auto_convert_resize": True
}

def save_settings(settings: dict = DEFAULT_SETTINGS):
    f = open(SETTINGS_FILE, "w")
    f.write(str(settings["min_delay"]) + "\n")
    f.write(str(settings["max_delay"]) + "\n")
    if settings["auto_convert_resize"]:
        f.write(str(1) + "\n")
    else:
        f.write(str(0) + "\n")
    f.close()

def get_settings():
    if os.path.isfile(SETTINGS_FILE):
        settings = {}
        f = open(SETTINGS_FILE, "r")
        try:
            settings["min_delay"] = float(f.readline().strip())
            settings["max_delay"] = float(f.readline().strip())
            auto_convert_resize = int(f.readline().strip())
            settings["auto_convert_resize"] = True if auto_convert_resize else False
        except:
            general_lib.error_log("Reading " + SETTINGS_FILE)
            settings = DEFAULT_SETTINGS
        f.close()
        return settings
    else:
        save_settings()
        return DEFAULT_SETTINGS

####################################################################################################
#############################################   Test   #############################################
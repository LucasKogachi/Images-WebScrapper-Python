# Image Web Scrapper Python

## Overview

Simple Image Web Scrapper made in Python, for now it only works on the site natomanga(old mangakakalot), which is a quite popular manga website.

## How it Works

The whole program process is divided in 3 steps:
+ Planning (optional)
+ Download
+ Working (optional)

To avoid IP Block, there is a simple delay time function (does nothing for a period of a time) and while you wait, you can work on what you already downloaded. What is meant to say is that you can run the same program in 2 different terminals. One terminal for Download/wait delay and another to plan future downloads and work on what you already downloaded. You can also just use one terminal for everything.

### Planning (Optional)

It saves one url on a txt file for use later. And it can also save title(s) on another txt file if you choose to convert the images to pdf later.

### Download

If there's a specific txt file with an url created in the Planning Step it automatically uses it to start downloading, otherwise it asks for an url.

### Working (Optional)

Allows you to convert images to pdf, split pdfs and merge pdfs. When converting images from a specific folder to pdf, if title txt file was created in the Planning Step, it automatically uses that title, you can also convert part of imgs to pdf instead of all, that's why you can add multiple titles to the titles txt file.

### Example

Url of One Piece Chapter 1 ```https://www.natomanga.com/manga/one-piece/chapter-1```

Or

Url of One Piece entire Manga ```https://www.natomanga.com/manga/one-piece```

## Getting Started

1. Install Python 3\
    Visit https://www.python.org/downloads/
    
2. Install pip to install dependencies\
    Visit https://pip.pypa.io/en/stable/installation/. pip is a package installler for Python, which makes it easier to install additional libraries and dependencies (you don't need to reinvent the wheel)

3. Install dependencies with pip (terminal)\
    ```pip install requests``` # download imgs\
    ```pip install pillow``` # manipulate imgs\
    ```pip install pymupdf``` # pdf\
    ```pip install beautifulsoup4``` # scrapers\
    ```pip install html5lib``` # support beautifulsoup4
    ```pip install natsort``` # sort files like os

4. (Optional) Install VSCode or other Code Editor of your preference\
    Visit https://code.visualstudio.com/Download

5. Run main.py with the other scripts(.py) in the same folder

6. Enjoy it

## Known Issues

+ No Cookies, the requests function have a way to use cookies, but the sites i'm visiting are not using it yet, so that's why...
+ Cloudflare
# Image Web Scrapper Python

## Overview

Simple Image Web Scrapper made in Python, for now it only works on the site mangakakalot, which is a quite popular manga website.

## How it Works

Let's use an example, you have the url of One Piece Chapter 1 ```https://chapmanganato.to/manga-aa951409/chapter-1``` and Chapter 2 ```https://chapmanganato.to/manga-aa951409/chapter-2```

The whole program process is divided in 3 steps:
    + Planning (optional)
    + Download
    + Working (optional)

To avoid IP Block there is a simple delay time function (does nothing for a period of a time) and while you wait you can work on what you already downloaded. What i meant to say is that you can run the same program in 2 different terminals. One terminal for Download/wait delay and another to plan future downloads and work on what you already downloaded. You can also just use one terminal for everything.

### Planning

It saves one url on a txt file for use later.

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

4. (Optional) Install VSCode or other Code Editor of your preference\
    Visit https://code.visualstudio.com/Download

5. Run main.py with images_lib.py, archives_lib.py, scrapers_lib.py and interface.py in the same folder
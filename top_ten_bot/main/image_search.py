#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.processing.list_processing import clean_list
from dvk_archive.main.processing.string_processing import get_extension
from dvk_archive.main.web.bs_connect import get_direct_response
from dvk_archive.main.web.bs_connect import json_connect
from os.path import exists, join
from PIL import Image
from random import randint
from time import sleep
from typing import List

def get_images(search:str=None,
                directory:str=None,
                num_images:int=10) -> List[Dvk]:
    """
    Returns list of Dvks with images related to the search query.
    Images are sourced from DuckDuckGo.

    :param search: Query for searching for images, defaults to None
    :type search: str, optional
    :param directory: Directory in which to save media, defaults to None
    :type directory: str, optional
    :param num_images: Number of images to download, defaults to 10
    :type num_images: int, optional
    :return: List of Dvks linked to relevent images
    :rtype: list[str]
    """
    if search is None or directory is None:
        return []
    try:
        print("Searching for images...")
        # Send POST request to DuckDuckGo
        data = {"q":search}
        response = get_direct_response("https://duckduckgo.com/", data=data)
        html = response.text
        # Get DuckDuckGo token
        start = html.find("vqd='") + 5
        end = html.find("'", start)
        if start == -1:
            start = html.find("vqd=\"") + 5
            end = html.find("\"", start)
        token = html[start:end]
        # Get base search
        url = "https://duckduckgo.com/i.js?l-us-en&o=json&q="
        url = url + search
        url = url + "&vqd="
        url = url + token
        url = url + "&f=,size:Medium,,,layout:Wide,&p="
        # Get images
        images = []
        page_num = 1
        size = int(num_images*1.5)
        pages = int(num_images/3) + 3
        while page_num < pages and len(images) < size:
            sleep(5)
            json = json_connect(url + str(page_num))
            results = json["results"]
            for result in results:
                images.append(result["image"])
            clean_list(images)
            page_num+=1
        # Download images
        print("Downloading images...")
        dvks = []
        num_downloaded = 0
        while len(images) > 0 and num_downloaded < num_images:
            # Get random link from list of images
            link_num = randint(0, len(images)-1)
            # Set up Dvk for downloading image
            dvk = Dvk()
            filename = str(num_downloaded + 1)
            dvk.set_dvk_file(join(directory, filename + ".dvk"))
            dvk.set_title(filename)
            dvk.set_dvk_id("filename")
            dvk.set_artist("artist")
            dvk.set_page_url("/url/")
            dvk.set_direct_url(images[link_num])
            dvk.set_media_file(filename + get_extension(images[link_num]))
            dvk.write_media()
            # Check if files were actually downloaded
            if exists(dvk.get_media_file()):
                try:
                    # Check image isn't corrupted.
                    image = Image.open(dvk.get_media_file())
                    w = image.size[0]
                    h = image.size[1]
                    if w > 100 and h > 100:
                        dvks.append(dvk)
                        num_downloaded += 1
                except:
                    dvk = None
            del images[link_num]
            sleep(2)
        return dvks
    except:
        return []

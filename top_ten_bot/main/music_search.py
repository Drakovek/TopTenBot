#!/usr/bin/env python3

from dvk_archive.main.web.bs_connect import bs_connect
from json import loads
from moviepy.editor import AudioFileClip
from os import listdir, mkdir
from os.path import abspath, basename, exists, isdir, join
from random import randint
from shutil import move, rmtree
from tempfile import gettempdir
from time import sleep
from traceback import print_exc
from typing import List
from youtubesearchpython import VideosSearch
import youtube_dl

hot_100_links = ["https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2009",
            "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2010",
            "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2011",
            "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2012",
            "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2013",
            "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2014",
            "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2015"]

def get_temp_directory(directory_name:str="dvk_top_ten") -> str:
    """
    Creates and returns a temporary directory for storing media.

    :param directory_name: Name of the temporary direcrory, defaults to "dvk_top_ten"
    :type directory_name: str
    :return: Path to the temporary directory
    :rtype: str
    """
    # Return None if directory name is invalid
    if directory_name is None or directory_name == "":
        return None
    # Get temporary directory
    temp_dir = abspath(join(abspath(gettempdir()), directory_name))
    # Delete directory if it already exists
    if(exists(temp_dir)):
        rmtree(temp_dir)
    # Create directory
    mkdir(temp_dir)
    return temp_dir

def get_top_40(url:str=None) -> List[List[str]]:
    """
    Returns a list of the top 40 songs from a wikipedia article of a year's hot 100 singles.

    :param url: URL of a Year End Billboard 100 from Wikipedia, defaults to None
    :type url: str, optional
    :return: List of songs, each entry is a list of [song, artist]
    :rtype: list[list[str]]
    """
    try:
        # Get a list of all rows in a table on the page
        bs = bs_connect(url)
        sleep(2)
        rows = bs.find_all("tr")
        # Run through rows
        pairs = []
        for row in rows:
            # Check if a chart reference, and in the top 40
            columns = row.find_all("td")
            try:
                if len(columns) == 3 and int(columns[0].get_text()) < 41:
                    # Get song title
                    title = columns[1].find("a").get_text()
                    # Get song artist
                    artist = columns[2].find("a").get_text()
                    # Add song+artist pair to list
                    pairs.append([title, artist])
            except:
                first_column = None
        # Return list of song+artist pairs
        return pairs
    except:
        return []

def find_song_video(song_title:str=None, artist:str=None) -> str:
    """
    Finds YouTube video URL for a given song.

    :param song_title: Title of the song to search for, defaults to None
    :type song_title: str, optional
    :param artist: Artist of the song to search for, defaults to None
    :type artist: str, optional
    :return: YouTube URL for the given song
    :rtype: str
    """
    # Return None if parameters are invalid
    if song_title is None or song_title == "" or artist is None or artist == "":
        return None
    # Get list of search results
    search = song_title + " " + artist + " lyrics"
    video_search = VideosSearch(search, limit = 2)
    results = video_search.result()["result"]
    sleep(2)
    # Get link that matches the search query
    for result in results:
        title = result["title"].lower()
        if ("lyrics" in title
                    and song_title.lower() in title
                    and artist.lower() in title):
            return "https://www.youtube.com/watch?v=" + result["id"]
    return None

def download_music(url:str=None, filename:str=None, directory:str=None) -> str:
    """
    Downloads an audio file from a given youtube link.

    :param url: URL of video to download from, defaults to None
    :type url: str, optional
    :param filename: What to name the audio file (without extesion), defaults to None
    :type filename: str, optional
    :param directory: Directory in which to save audio file, defaults to None
    :type directory: str, optional
    :return: File path for the downloaded audio file
    :rtype: str
    """
    # Return None if directory is invalid
    if directory is None or not exists(directory) or not isdir(directory):
        return None
    # Return None if parameters are invalid
    if url is None or url == "" or filename is None or filename == "":
        return None
    try:
        # Get file path for the music being downloaded
        temp_dir = get_temp_directory("dvk_audio")
        file = abspath(join(temp_dir, filename + "."))
        # Download audio file to temp directory
        ydl_opts = {"format": "worstaudio", "outtmpl": (str(file) + "%(ext)s")}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Get path of downloaded file
        paths = listdir(temp_dir)
        assert len(paths) == 1
        file = abspath(join(temp_dir, paths[0]))
        # Move file to the given directory
        filename = basename(file)
        new_file = abspath(join(directory, filename))
        move(file, new_file)
        # Return the file path
        return new_file
    except:
        return None

def get_songs(directory:str=None, duration:int=0) -> List[str]:
    """
    Downloads a list of pop songs long enough to fill a given amount of time.

    :param directory: Directory to save music to, defaults to None
    :type directory: str, optional
    :param duration: length of time to fill in seconds, defaults to 0
    :type duration: int, optional
    :return: List of audio files
    :rtype: list[str]
    """
    # Return empty list if directory is invalid
    if directory is None or not exists(directory) or not isdir(directory):
        return []
    try:
        # Get list of indexes relating to Hot 100 links
        link_nums = []
        for i in range(0, len(hot_100_links)):
            link_nums.append(i)
        # Run loop until needed duration is met
        songs = []
        return_songs = []
        song_num = 1
        cur_duration = 0
        while len(link_nums) > 0 and cur_duration < duration:
            # Get list of top 40 songs, if needed
            if songs == []:
                index = randint(0, len(link_nums)-1)
                songs = get_top_40(hot_100_links[link_nums[index]])
                del link_nums[index]
            # Get YouTube link for a random song
            index = randint(0, len(songs)-1)
            url = find_song_video(songs[index][0], songs[index][1])
            del songs[index]
            # Download song
            file = download_music(url, str(song_num), directory)
            if file is not None:
                # Add to list of songs, and add song duration
                return_songs.append(file)
                clip = AudioFileClip(file)
                cur_duration += clip.duration
                song_num += 1
        return return_songs
    except:
        print_exc()
        return []
    

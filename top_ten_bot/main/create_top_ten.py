#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.processing.string_processing import get_filename
from os import getcwd, mkdir
from os.path import abspath, basename, exists, isdir, join
from tempfile import gettempdir
from top_ten_bot.main.image_search import get_images
from top_ten_bot.main.encode_video import create_list_video, write_video
from shutil import move, rmtree

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

def create_video(search:str=None,
            title:str=None,
            items:str="10",
            directory:str=None) -> str:
    """
    Creates a top # video given a search string and title.

    :param search: Text used to search for images, defaults to None
    :type search: str, optional
    :param title: Title of the video, defaults to None
    :type title: str, optional
    :param items: Number of items to show in the video as a str, defaults to "10" 
    :type items: str, optional
    :param directory: Directory to save video into, defaults to None
    :type directory: str, optional
    :return: Path to the rendered video
    :rtype: str
    """
    # Return None it title or search strings are none or empty
    if title is None or title == "" or search is None or search == "":
        return None
    # Return None if directory is invalid
    if (directory is None
                or not exists(abspath(directory))
                or not isdir(abspath(directory))):
        print("Directory is invalid.")
        return None
    # Get temporary directory for saving images into
    temp_dir = get_temp_directory()
    # Get list of files from the search query
    try:
        num_images = int(items)
        dvks = get_images(search, temp_dir, num_images)
    except(TypeError, ValueError):
        print("Number used for the number of items is invalid")
        return None
    # Get video visuals
    video = create_list_video(title, dvks)
    # Write the video to file
    filename = get_filename(title)
    video_file = join(abspath(directory), filename + ".webm")
    write_video(video, video_file)
    # Create image folder
    image_folder = abspath(join(abspath(directory), filename))
    if not exists(image_folder):
        mkdir(image_folder)
    # Move files to image folder
    for dvk in dvks:
        filename = basename(dvk.get_media_file())
        moved = abspath(join(image_folder, filename))
        move(dvk.get_media_file(), moved)
    # Delete temporary folder
    rmtree(temp_dir)
    # Return video file
    return video_file

def main():
    """
    Sets up creating a top 10 video.
    """
    parser = ArgumentParser()
    parser.add_argument(
        "search",
        help="String used to search for images",
        type=str)
    parser.add_argument(
        "title",
        help="Title of the video",
        type=str)
    parser.add_argument(
        "-i",
        "--items",
        metavar="#",
        help="Number of items to include in the video",
        type=str,
        default="10")
    parser.add_argument(
        "-d",
        "--directory",
        metavar="DIR",
        help="Directory in which to save the video",
        type=str,
        default=str(getcwd()))
    args = parser.parse_args()
    create_video(args.search, args.title, args.items, args.directory)

if __name__ == "__main__":
    main()

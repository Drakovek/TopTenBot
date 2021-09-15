#!/usr/bin/env python3

from argparse import ArgumentParser
from dvk_archive.main.processing.string_processing import get_filename
from os import getcwd, mkdir
from os.path import abspath, basename, exists, isdir, join
from top_ten_bot.main.image_search import get_images
from top_ten_bot.main.encode_video import add_audio_to_video
from top_ten_bot.main.encode_video import create_list_video
from top_ten_bot.main.encode_video import write_video
from top_ten_bot.main.music_search import get_songs
from top_ten_bot.main.music_search import get_temp_directory
from shutil import move, rmtree

def create_video(search:str=None,
            title:str=None,
            items:str="10",
            width:str="240",
            directory:str=None) -> str:
    """
    Creates a top # video given a search string and title.

    :param search: Text used to search for images, defaults to None
    :type search: str, optional
    :param title: Title of the video, defaults to None
    :type title: str, optional
    :param items: Number of items to show in the video as a str, defaults to "10" 
    :type items: str, optional
    :param items: Width of the video as a str, defaults to "240" 
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
    temp_dir = get_temp_directory("dvk_video")
    # Get with to use for rendering video
    try:
        int_width = int(width)
    except(TypeError, ValueError):
        print("Number used for video width is invalid")
        return None
    # Get list of files from the search query
    try:
        num_images = int(items)
    except(TypeError, ValueError):
        print("Number used for the number of items is invalid")
        return None
    dvks = get_images(search, temp_dir, num_images)
    # Get video visuals
    video = create_list_video(title, dvks, int_width)
    # Add songs to video
    print("Searching for songs...")
    songs = get_songs(temp_dir, int(video.duration))
    print(songs)
    with_audio = add_audio_to_video(video, songs)
    # Write the video to file
    filename = get_filename(title)
    video_file = join(abspath(directory), filename + ".mp4")
    write_video(with_audio, video_file)
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
        "-w",
        "--width",
        metavar="#",
        help="Width of the rendered video in pixels",
        type=str,
        default="240")
    parser.add_argument(
        "-d",
        "--directory",
        metavar="DIR",
        help="Directory in which to save the video",
        type=str,
        default=str(getcwd()))
    args = parser.parse_args()
    create_video(args.search, args.title, args.items, args.width, args.directory)

if __name__ == "__main__":
    main()

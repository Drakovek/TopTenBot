#!/usr/bin/env python3

from argparse import ArgumentParser
from traceback import print_exc
from top_ten_bot.test.test_create_top_ten import all_tests as create_top_ten
from top_ten_bot.test.test_encode_video import all_tests as encode_video
from top_ten_bot.test.test_image_search import all_tests as image_search
from top_ten_bot.test.test_music_search import all_tests as music_search

def test_all():
    """
    Runs all unit tests for the top_ten_bot program.
    """
    try:
        image_search()
        music_search()
        encode_video()
        create_top_ten()
        print("\033[32mAll TopTenBot tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()

def test_encode_video():
    """
    Runs tests related to encoding images into a video.
    """
    try:
        encode_video()
        print("\033[32mAll image searching tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()

def test_image_search():
    """
    Runs tests related to searching for images.
    """
    try:
        image_search()
        print("\033[32mAll image searching tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()

def test_music_search():
    """
    Runs tests related to searching for pop music.
    """
    try:
        music_search()
        print("\033[32mAll music searching tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()

def test_create_top_ten():
    """
    Runs tests related to creating a full top 10 video.
    """
    try:
        create_top_ten()
        print("\033[32mAll CreateTopTen tests passed.\033[0m")
    except AssertionError:
        print("\033[31mCheck failed:\033[0m")
        print_exc()


def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-c",
        "--createtop",
        help="Runs tests for creating a full top 10 video.",
        action="store_true")
    group.add_argument(
        "-e",
        "--encode",
        help="Runs tests for the encoding video.",
        action="store_true")
    group.add_argument(
        "-i",
        "--imagesearch",
        help="Runs tests for the image searching functions.",
        action="store_true")
    group.add_argument(
        "-m",
        "--musicsearch",
        help="Runs tests for the music searching functions.",
        action="store_true")
    args = parser.parse_args()
    if args.imagesearch:
        test_image_search()
    elif args.musicsearch:
        test_music_search() 
    elif args.encode:
        test_encode_video()
    elif args.createtop:
        test_create_top_ten()
    else:
        test_all()

if __name__ == "__main__":
    main()


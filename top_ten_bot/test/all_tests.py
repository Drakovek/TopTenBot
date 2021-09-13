#!/usr/bin/env python3

from argparse import ArgumentParser
from traceback import print_exc
from top_ten_bot.test.test_image_search import all_tests as image_search


def test_all():
    """
    Runs all unit tests for the top_ten_bot program.
    """
    try:
        image_search()
        print("\033[32mAll TopTenBot tests passed.\033[0m")
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

def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--imagesearch",
        help="Runs tests for the image searching functions.",
        action="store_true")
    args = parser.parse_args()
    if args.imagesearch:
        test_image_search()
    else:
        test_all()

if __name__ == "__main__":
    main()


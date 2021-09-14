#!/usr/bin/env python3

from dvk_archive.test.temp_dir import get_test_dir
from moviepy.editor import VideoFileClip
from os import listdir
from os.path import abspath, basename, exists, isdir, join
from top_ten_bot.main.create_top_ten import create_video
from top_ten_bot.main.create_top_ten import get_temp_directory

def test_get_temp_directory():
    """
    Tests the get_temp_directory function.
    """
    # Test getting temporary directory.
    temp_dir = get_temp_directory()
    assert exists(temp_dir)
    assert basename(temp_dir) == "dvk_top_ten"
    # Test deleting contents of temporary directory
    file = abspath(join(temp_dir, "file.txt"))
    with open(file, "w") as out_file:
        out_file.write("TEST")
    assert exists(file)
    temp_dir = get_temp_directory()
    assert exists(temp_dir)
    assert not exists(file)

def test_create_video():
    # Test creating a video
    test_dir = get_test_dir()
    file = create_video("taco", "top 2 tacos!", "2", test_dir)
    assert file == abspath(join(test_dir, "top 2 tacos.webm"))
    assert exists(file)
    clip = VideoFileClip(file)
    assert clip.duration == 20
    # Test that image files were moved to image folder
    sub = abspath(join(test_dir, "top 2 tacos"))
    assert exists(sub)
    assert isdir(sub)
    assert len(listdir(sub)) == 2
    # Test using invalid parameters
    create_video(None, "top 2 tacos!", "2", test_dir) == None
    create_video("", "top 2 tacos!", "2", test_dir) == None
    create_video("taco", None, "2", test_dir) == None
    create_video("taco", "", "2", test_dir) == None
    create_video("taco", "top 2 tacos!", None, test_dir) == None
    create_video("taco", "top 2 tacos!", "blah", test_dir) == None
    create_video("taco", "top 2 tacos!", "2", None) == None
    create_video("taco", "top 2 tacos!", "2", "/non/existant/dir/") == None

def all_tests():
    """
    Runs all tests for the create_top_ten.py module.
    """
    test_get_temp_directory()
    test_create_video()

#!/usr/bin/env python3

from dvk_archive.test.temp_dir import get_test_dir
from moviepy.editor import VideoFileClip
from os import listdir
from os.path import abspath, basename, exists, isdir, join
from top_ten_bot.main.create_top_ten import create_video

def test_create_video():
    """
    Tests the create_video function.
    """
    # Test creating a video
    test_dir = get_test_dir()
    file = create_video("taco", "top 2 tacos!", "2", "240", test_dir)
    assert file == abspath(join(test_dir, "top 2 tacos.mp4"))
    assert exists(file)
    clip = VideoFileClip(file)
    assert int(clip.duration) == 20
    # Test that image files were moved to image folder
    sub = abspath(join(test_dir, "top 2 tacos"))
    assert exists(sub)
    assert isdir(sub)
    assert len(listdir(sub)) == 2
    # Test using invalid parameters
    create_video(None, "top 2 tacos!", "2", "240", test_dir) == None
    create_video("", "top 2 tacos!", "2", "240", test_dir) == None
    create_video("taco", None, "2", "240", test_dir) == None
    create_video("taco", "", "2", "240", test_dir) == None
    create_video("taco", "top 2 tacos!", None, "240", test_dir) == None
    create_video("taco", "top 2 tacos!", "blah", "240", test_dir) == None
    create_video("taco", "top 2 tacos!", "2", None, test_dir) == None
    create_video("taco", "top 2 tacos!", "2", "notNumber", test_dir) == None
    create_video("taco", "top 2 tacos!", "2", "240", None) == None
    create_video("taco", "top 2 tacos!", "2", "240", "/non/existant/dir/") == None

def all_tests():
    """
    Runs all tests for the create_top_ten.py module.
    """
    test_create_video()

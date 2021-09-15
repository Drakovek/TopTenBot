#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.web.bs_connect import download
from dvk_archive.test.temp_dir import get_test_dir
from moviepy.editor import VideoFileClip
from top_ten_bot.main.encode_video import add_audio_to_video
from top_ten_bot.main.encode_video import create_list_video
from top_ten_bot.main.encode_video import get_image_clip
from top_ten_bot.main.encode_video import get_text_clip
from top_ten_bot.main.encode_video import write_video
from top_ten_bot.main.image_search import get_images
from top_ten_bot.main.music_search import download_music
from os.path import abspath, exists, join

def test_get_text_clip():
    """
    Tests the get_text_clip function.
    """
    # Test video is the correct duration
    video = get_text_clip("uniportant text")
    assert video is not None
    assert video.duration == 4
    # Test using invalid parameters
    video = get_text_clip(None)
    assert video is None

def test_get_image_clip():
    """
    Tests the get_image_clip function.
    """
    # Download test image
    test_dir = get_test_dir()
    file = abspath(join(test_dir, "image.jpg"))
    url = "http://www.pythonscraping.com/img/gifts/img6.jpg"
    download(url, file)
    assert exists(file)
    # Test video is the correct definition.
    video = get_image_clip(file)
    assert video is not None
    assert video.duration == 4
    # Test resized image exists
    file = abspath(join(test_dir, "image-rs.png"))
    assert exists(file)
    # Test using invalid parameters
    assert get_image_clip("/non/existant/file") is None
    assert get_image_clip(None) is None

def test_create_list_video():
    """
    Tests the create_list function.
    """
    # Get test Dvks with images attatched
    test_dir = get_test_dir()
    dvks = get_images("banana", test_dir, 2)
    assert len(dvks) == 2
    # Test video is the correct duration
    video = create_list_video("top 2 bananas", dvks)
    assert video is not None
    assert video.duration == 20
    # Test using empty list
    video = create_list_video("title", [])
    assert video is not None
    assert video.duration == 4
    # Test using invalid parameters
    assert create_list_video(None, dvks) == None
    assert create_list_video("title", None) == None
    assert create_list_video("title", [Dvk()]) == None

def test_write_video():
    """
    Tests the write_video function.
    """
    # Test that video was written to file.
    test_dir = get_test_dir()
    video = get_text_clip("test text")
    file = join(test_dir, "test.webm")
    write_video(video, file)
    assert exists(file)
    clip = VideoFileClip(file)
    assert clip.duration == 4
    # Test writing video with invalid parameters
    file = join(test_dir, "other.webm")
    assert not exists(file)
    write_video(None, file)
    assert not exists(file)
    file = "/non/existant/directory/file.webm"
    write_video(video, file)
    assert not exists(file)
    write_video(video, None)

def test_add_audio_to_video():
    """
    Tests the add_audio_to_video function.
    """
    # Get test audio file
    test_dir = get_test_dir()
    file = download_music("https://www.youtube.com/watch?v=mUJIALZU5_M", "1", test_dir)
    assert exists(file)
    # Get test text file
    video = get_text_clip("test text")
    # Test adding audio to video clip
    mixed = add_audio_to_video(video, [file])
    assert mixed is not None
    assert mixed.duration == 4
    # Test using invalid parameters
    mixed = add_audio_to_video(video, []) is None
    add_audio_to_video(video, [""]) is None
    add_audio_to_video(video, [None]) is None
    add_audio_to_video(None, [file]) is None

def all_tests():
    """
    Runs all tests for the encode_video.py module.
    """
    test_add_audio_to_video()
    test_get_text_clip()
    test_get_image_clip()
    test_write_video()
    test_create_list_video()

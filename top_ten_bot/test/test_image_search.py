#!/usr/bin/env python3

from dvk_archive.test.temp_dir import get_test_dir
from os.path import exists
from top_ten_bot.main.image_search import get_images

def test_get_images():
    """
    Tests the get_images function.
    """
    # Test getting images
    test_dir = get_test_dir()
    dvks = get_images("moose", test_dir, 3)
    assert len(dvks) == 3
    assert exists(dvks[0].get_media_file())
    assert exists(dvks[1].get_media_file())
    assert exists(dvks[2].get_media_file())
    # Test getting no images
    assert get_images("cat", test_dir, 0) == []
    # Test with invalid parameters
    assert get_images(None, test_dir, 10) == []
    assert get_images("dog", None, 5) == []
 
def all_tests():
    """
    Runs all tests for the image_search.py module.
    """
    test_get_images()

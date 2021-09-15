#!/usr/bin/env python3

from dvk_archive.test.temp_dir import get_test_dir
from os.path import abspath, basename, exists, join
from moviepy.editor import AudioFileClip
from top_ten_bot.main.music_search import download_music
from top_ten_bot.main.music_search import find_song_video
from top_ten_bot.main.music_search import get_songs
from top_ten_bot.main.music_search import get_temp_directory
from top_ten_bot.main.music_search import get_top_40

def test_get_temp_directory():
    """
    Tests the get_temp_directory function.
    """
    # Test getting temporary directory.
    temp_dir = get_temp_directory()
    assert exists(temp_dir)
    assert basename(temp_dir) == "dvk_top_ten"
    temp_dir = get_temp_directory("dvk_other")
    assert exists(temp_dir)
    assert basename(temp_dir) == "dvk_other"
    # Test deleting contents of temporary directory
    file = abspath(join(temp_dir, "file.txt"))
    with open(file, "w") as out_file:
        out_file.write("TEST")
    assert exists(file)
    temp_dir = get_temp_directory("dvk_other")
    assert exists(temp_dir)
    assert not exists(file)
    # Test getting directory with invalid parameters
    assert get_temp_directory(None) == None
    assert get_temp_directory("") == None

def test_get_top_40():
    """
    Tests the get_top_40 function.
    """
    # Test getting songs from the top 40
    base_url = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_"
    top_40 = get_top_40(base_url + "2010")
    assert len(top_40) == 40
    assert top_40[0] == ["Tik Tok", "Kesha"]
    assert top_40[39] == ["Club Can't Handle Me", "Flo Rida"]
    top_40 = get_top_40(base_url + "2012")
    assert len(top_40) == 40
    assert top_40[0] == ["Somebody That I Used to Know", "Gotye"]
    assert top_40[1] == ["Call Me Maybe", "Carly Rae Jepsen"]
    # Test getting songs from invalid urls
    assert get_top_40("https://en.wikipedia.org/wiki/Toothpaste") == []
    assert get_top_40("") == []
    assert get_top_40(None) == []

def test_find_song_video():
    """
    Tests the find_song_video function.
    """
    # Test finding a youtube video for a song
    url = find_song_video("Party Rock Anthem", "LMFAO")
    assert url == "https://www.youtube.com/watch?v=Coq-OlEdZQ8"
    # Test finding song when video doesn't exist
    url = find_song_video("This is not a real song", "absolutely nobody")
    assert url == None
    # Test finding song with invalid parameters
    assert find_song_video("", "LMFAO") is None
    assert find_song_video(None, "LMFAO") is None
    assert find_song_video("Party Rock Anthem", "") is None
    assert find_song_video("Party Rock Anthem", None) is None

def test_download_music():
    """
    Tests the download_music function.
    """
    # Test downloading audio from youtube video
    test_dir = get_test_dir()
    file = download_music("https://www.youtube.com/watch?v=mUJIALZU5_M", "1", test_dir)
    assert file == abspath(join(test_dir, "1.webm"))
    assert exists(file)
    clip = AudioFileClip(file)
    assert clip.duration == 143.04
    # Test downloading invalid parameters
    assert download_music("ashtdarwa", "1", test_dir) is None
    assert download_music("", "1", test_dir) is None
    assert download_music(None, "1", test_dir) is None
    assert download_music("https://www.youtube.com/watch?v=mUJIALZU5_M", None, test_dir) is None
    assert download_music("https://www.youtube.com/watch?v=mUJIALZU5_M", "", test_dir) is None
    assert download_music("https://www.youtube.com/watch?v=mUJIALZU5_M", "1", None) is None
    assert download_music("https://www.youtube.com/watch?v=mUJIALZU5_M", "1", "/non/existant/dir/") is None

def test_get_songs():
    """
    Tests the get_songs function.
    """
    # Test getting songs
    test_dir = get_test_dir()
    files = get_songs(test_dir, 400)
    assert len(files) > 1
    duration = 0
    for file in files:
        assert exists(file)
        clip = AudioFileClip(file)
        duration += clip.duration
    assert duration > 400
    # Test getting songs with invalid parameters
    assert get_songs(None, 400) == []
    assert get_songs("/non/existant/dir/", 400) == []
    assert get_songs(test_dir, 0) == []
    assert get_songs(test_dir) == []

def all_tests():
    """
    Runs all tests for the music_search.py module.
    """
    test_get_temp_directory()
    test_get_top_40()
    test_find_song_video()
    test_download_music()
    test_get_songs()

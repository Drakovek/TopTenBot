# TopTenBot

Utility for creating terrible, low quality Top 10 Videos.

# WARNING!!!

This program pulls images and audio from the internet at random based on a search query, and thus some of the media used *might* be innappropriate or NSFW. Always check the resulting video before posting somewhere!

# Installation

This program requires [ImageMagick](https://imagemagick.org/index.php) to be installed on your system.
ImageMagick is used by moviepy to generate text, and should be detected automatically on MacOS and Unix-based systems.

ImageMagick will not be detected on Windows and some versions of Ubuntu. Follow the instructions on the [moviepy website](https://zulko.github.io/moviepy/install.html) if ImageMagick isn't working correctly.

TopTenBot can be intalled from its [PyPI package](https://pypi.org/project/TopTenBot/) using pip:

    pip install TopTenBot

If you are installing from source, the following python packages are required:
* [dvk_archive](https://pypi.org/project/dvk-archive/)
* [moviepy](https://pypi.org/project/moviepy/)
* [Pillow](https://pypi.org/project/Pillow/)
* [youtube-dl](https://pypi.org/project/youtube_dl/)
* [youtube-search-python](https://pypi.org/project/youtube-search-python/)

# Running Program

Simply use the "top10bot" command in your terminal:

    top10bot search title [-i items] [-d directory] [-h for help]

For example, the following command would create a video titled "top 25 lizards"

    top10bot lizard "top 25 lizards" -i 25

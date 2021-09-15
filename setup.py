#!/usr/bin/env python3

"""Setuptools setup file."""

import setuptools

console_scripts = [
    "top10test = top_ten_bot.test.all_tests:main",
    "top10bot = top_ten_bot.main.create_top_ten:main"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TopTenBot",
    version="0.1.1",
    author="Drakovek",
    author_email="DrakovekMail@gmail.com",
    description=long_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drakovek/dvk_manga",
    packages=setuptools.find_packages(),
    install_requires=["dvk-archive", "moviepy", "pillow", "youtube-dl", "youtube-search-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.0',
    entry_points={"console_scripts": console_scripts}
)

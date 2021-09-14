#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.processing.string_processing import get_extension
from moviepy.editor import concatenate_videoclips
from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip, TextClip, VideoClip
from os import pardir
from os.path import abspath, basename, join
from PIL import Image
from typing import List

def get_text_clip(text:str=None, fadein:bool=True, fadeout:bool=True) -> VideoClip:
    """
    Returns a VideoClip showing given text in Comic Sans on a blue background.

    :param text: Text to use in the video clip, defaults to None
    :type text: str, optional
    :param fadein: Whether to fade clip in from black, defaults to True
    :type fadein: boolean, optional
    :param fadeout: Whether to fade clip out to black, defaults to True
    :type fadeout: boolean, optional
    :return: Video clip of your glorious Comic Sans text
    :rtype: VideoClip
    """
    try:
        # Set text clip
        text_clip = TextClip(text, method="caption", size=(400, None),
                    fontsize=48, font="Comic-Sans-MS", color="white")
        text_clip = text_clip.set_pos("center").set_duration(4)
        # Set color background
        color_clip = ColorClip(size=(480,360), color=[45,152,255])
        color_clip = color_clip.set_duration(4)
        # Get black fadein
        start = ColorClip(size=(480, 360), color=[0,0,0])
        start = start.set_duration(1)
        start = start.crossfadeout(1)
        # Get black fadeout
        end = ColorClip(size=(480, 360), color=[0,0,0])
        end = end.set_duration(1).set_start(3)
        end = end.crossfadein(1)
        # Composite clips together
        video = CompositeVideoClip([color_clip, text_clip])
        if fadein:
            video = CompositeVideoClip([video, start])
        if fadeout:
            video = CompositeVideoClip([video, end])
        # Return composite video
        return video
    except:
        return None

def get_image_clip(image:str=None, fadein:bool=True, fadeout:bool=True) -> VideoClip:
    """
    Returns a VideoClip showing a given image, resized if necessary.

    :param image: Path to an image file, defaults to None
    :type image: str, optional
    :param fadein: Whether to fade clip in from black, defaults to True
    :type fadein: boolean, optional
    :param fadeout: Whether to fade clip out to black, defaults to True
    :type fadeout: boolean, optional
    :return: Video clip of given image.
    :rtype: VideoClip
    """
    try:
        # Resize Image
        original = Image.open(image)
        width = original.size[0]
        height = original.size[1]
        new_width = 480
        new_height = 360
        if width < height:
            ratio = height/width
            new_height = int(ratio * 480)
        else:
            ratio = width/height
            new_width = int(ratio * 360)
        resized = original.resize((new_width, new_height))
        # Crop Image
        x = int((new_width - 480)/2)
        y = int((new_height - 360)/2)
        resized = resized.crop((x,y, x+480, y+360))
        # Save resized image
        parent = abspath(join(image, pardir))
        extension = get_extension(image)
        file = basename(image)
        file = file[0:len(file) - len(extension)]
        file = abspath(join(parent, file + "-rs" + ".png"))
        resized.save(file)
        # Set white background
        color_clip = ColorClip(size=(480,360), color=[255,255,255])
        color_clip = color_clip.set_duration(4)
        # Get image clip
        image_clip = ImageClip(file)
        image_clip = image_clip.set_duration(4)
        # Get black fadein
        start = ColorClip(size=(480, 360), color=[0,0,0])
        start = start.set_duration(1)
        start = start.crossfadeout(1)
        # Get black fadeout
        end = ColorClip(size=(480, 360), color=[0,0,0])
        end = end.set_duration(1).set_start(3)
        end = end.crossfadein(1)
        # Composite clips together
        video = CompositeVideoClip([color_clip, image_clip])
        if fadein:
            video = CompositeVideoClip([video, start])
        if fadeout:
            video = CompositeVideoClip([video, end])
        # return composited video
        return video
    except:
        return None

def create_list_video(title:str=None, dvks:List[Dvk]=None) -> VideoClip:
    """
    Creates a top # video with a numbered label for each of a given set of images.

    :param title: Title text to use for the intro title card, defaults to None
    :type title: str, optional
    :param dvks: List of dvks with connected image files, defaults to None
    :type dvks: list[Dvk], optional
    :return: Top # video
    :rtype: VideoClip
    """
    try:
        # Get title clip
        clips = [get_text_clip(title, False, True)]
        # Get list of text clips showing numbers
        size = len(dvks)
        number_clips = []
        for i in range(0, size):
            number_clips.append(get_text_clip("number " + str(size-i)))
        # Get list of image clips
        image_clips = []
        for i in range(0, size):
            image = dvks[i].get_media_file()
            image_clips.append(get_image_clip(image, True, i<size-1))
        # Combine lists of clips
        for i in range(0, size):
            clips.append(number_clips[i])
            clips.append(image_clips[i])
        # Concatenate and return video
        video = concatenate_videoclips(clips)
        return video
    except:
        return None

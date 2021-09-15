#!/usr/bin/env python3

from dvk_archive.main.file.dvk import Dvk
from dvk_archive.main.processing.string_processing import get_extension
from moviepy.editor import AudioFileClip
from moviepy.editor import concatenate_videoclips, concatenate_audioclips
from moviepy.editor import ColorClip, CompositeVideoClip, ImageClip, TextClip, VideoClip
from os import pardir
from os.path import abspath, basename, isdir, join
from PIL import Image
from typing import List

def get_text_clip(text:str=None, fadein:bool=True, fadeout:bool=True, width:int=240) -> VideoClip:
    """
    Returns a VideoClip showing given text in Comic Sans on a blue background.

    :param text: Text to use in the video clip, defaults to None
    :type text: str, optional
    :param fadein: Whether to fade clip in from black, defaults to True
    :type fadein: boolean, optional
    :param fadeout: Whether to fade clip out to black, defaults to True
    :type fadeout: boolean, optional
    :param width: Height of the video in pixels, defaults to 180
    :type width: int, optional
    :return: Video clip of your glorious Comic Sans text
    :rtype: VideoClip
    """
    try:
        # Set text clip
        fontsize = int(width/10)
        text_clip = TextClip(text, method="caption", size=(400, None),
                    fontsize=fontsize, font="Comic-Sans-MS", color="white")
        text_clip = text_clip.set_position("center").set_duration(4)
        # Set color background
        height = int(width*0.75)
        color_clip = ColorClip(size=(width,height), color=[45,152,255])
        color_clip = color_clip.set_duration(4)
        # Get black fadein
        start = ColorClip(size=(width,height), color=[0,0,0])
        start = start.set_duration(1)
        start = start.crossfadeout(1)
        # Get black fadeout
        end = ColorClip(size=(width,height), color=[0,0,0])
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

def get_image_clip(image:str=None, fadein:bool=True, fadeout:bool=True, width:int=240) -> VideoClip:
    """
    Returns a VideoClip showing a given image, resized if necessary.

    :param image: Path to an image file, defaults to None
    :type image: str, optional
    :param fadein: Whether to fade clip in from black, defaults to True
    :type fadein: boolean, optional
    :param fadeout: Whether to fade clip out to black, defaults to True
    :type fadeout: boolean, optional
    :param width: Height of the video in pixels, defaults to 180
    :type width: int, optional
    :return: Video clip of given image.
    :rtype: VideoClip
    """
    try:
        # Resize Image
        original = Image.open(image)
        owidth = original.size[0]
        oheight = original.size[1]
        height = int(width * 0.75)
        nwidth = width
        nheight = height
        if owidth < oheight:
            ratio = oheight/owidth
            nheight = int(ratio * width)
        else:
            ratio = owidth/oheight
            new_width = int(ratio * height)
        resized = original.resize((nwidth, nheight))
        # Crop Image
        x = int((nwidth - width)/2)
        y = int((nheight - height)/2)
        resized = resized.crop((x,y, x+width, y+height))
        # Save resized image
        parent = abspath(join(image, pardir))
        extension = get_extension(image)
        file = basename(image)
        file = file[0:len(file) - len(extension)]
        file = abspath(join(parent, file + "-rs" + ".png"))
        resized.save(file)
        # Set white background
        color_clip = ColorClip(size=(width,height), color=[255,255,255])
        color_clip = color_clip.set_duration(4)
        # Get image clip
        image_clip = ImageClip(file)
        image_clip = image_clip.set_duration(4)
        # Get black fadein
        start = ColorClip(size=(width, height), color=[0,0,0])
        start = start.set_duration(1)
        start = start.crossfadeout(1)
        # Get black fadeout
        end = ColorClip(size=(width, height), color=[0,0,0])
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

def create_list_video(title:str=None, dvks:List[Dvk]=None, width:int=240) -> VideoClip:
    """
    Creates a top # video with a numbered label for each of a given set of images.

    :param title: Title text to use for the intro title card, defaults to None
    :type title: str, optional
    :param dvks: List of dvks with connected image files, defaults to None
    :type dvks: list[Dvk], optional
    :param width: Height of the video in pixels, defaults to 180
    :type width: int, optional
    :return: Top # video
    :rtype: VideoClip
    """
    try:
        # Get title clip
        clips = [get_text_clip(title, False, True, width)]
        # Get list of text clips showing numbers
        size = len(dvks)
        number_clips = []
        for i in range(0, size):
            number_clips.append(get_text_clip("number " + str(size-i), True, True, width))
        # Get list of image clips
        image_clips = []
        for i in range(0, size):
            image = dvks[i].get_media_file()
            image_clips.append(get_image_clip(image, True, i<size-1, width))
        # Combine lists of clips
        for i in range(0, size):
            clips.append(number_clips[i])
            clips.append(image_clips[i])
        # Concatenate and return video
        video = concatenate_videoclips(clips)
        return video
    except:
        return None

def add_audio_to_video(video:VideoClip=None, audio:List[str]=None) -> VideoClip:
    """
    Adds audio from a list of audio files to a given video file.

    :param video: Video to add audio to, defaults to None
    :type video: VideoClip, optional
    :param audio: List of audio files to add to video, defaults to None
    :type audio: list[str], optional
    :return: VideoClip with added audio
    :rtype: VideoClip
    """
    try:
        # Concatenate audio files
        audio_clips = []
        for file in audio:
            clip = AudioFileClip(file)
            audio_clips.append(clip)
        full_audio = concatenate_audioclips(audio_clips)
        # Set video audio to concatenated audio
        full_audio = full_audio.set_duration(video.duration)
        video.audio = full_audio
        return video
    except:
        return None
    
def write_video(video:VideoClip=None, file:str=None):
    """
    Writes a given VideoClip to a file.

    :param video: VideoClip to save to file, defaults to None
    :type video: VideoClip, optional
    :param file: Path of file video will be saved to, defaults to None
    :type file: str, optional
    """
    # Check if parameters are valid
    if (video is not None
            and file is not None
            and isdir(abspath(join(file, pardir)))):
        # Write video to file
        video.write_videofile(abspath(file), fps=12, audio_bitrate="30k")

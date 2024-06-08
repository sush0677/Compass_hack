import streamlit as st
from moviepy.editor import TextClip, CompositeVideoClip

st.title("AI Video Generation")

def generate_video(text):
    # This function generates a simple video with text overlay using MoviePy
    clip = TextClip(text, fontsize=70, color='white', size=(640, 480))
    clip = clip.set_duration(10)  # 10 seconds duration
    video = CompositeVideoClip([clip])
    video.write_videofile("output.mp4", fps=24)
    return "output.mp4"

st.header("Generate Video")
user_input = st.text_input("Enter text to generate video")
if st.button("Generate"):
    if user_input:
        video_file = generate_video(user_input)
        st.video(video_file)
    else:
        st.error("Please enter some text to generate video")

import streamlit as st
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS

st.title("AI Content Creation Studio for myco.io")

def generate_video(text):
    # Generate a simple video with text overlay
    clip = TextClip(text, fontsize=70, color='white', size=(640, 480))
    clip = clip.set_duration(10)  # 10 seconds duration
    video = CompositeVideoClip([clip])
    video.write_videofile("output.mp4", fps=24)
    return "output.mp4"

def generate_audio(text):
    tts = gTTS(text)
    audio_file = "audio.mp3"
    tts.save(audio_file)
    return audio_file

def add_audio_to_video(video_file, audio_file):
    video = CompositeVideoClip([video_file])
    audio = AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    final_video.write_videofile("final_output.mp4", fps=24)
    return "final_output.mp4"

st.header("Generate Video")
user_input = st.text_input("Enter text to generate video with audio")
if st.button("Generate"):
    if user_input:
        video_file = generate_video(user_input)
        audio_file = generate_audio(user_input)
        final_video_file = add_audio_to_video(video_file, audio_file)
        st.video(final_video_file)
    else:
        st.error("Please enter some text to generate video")

import streamlit as st
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip


st.title("AI Content Creation Studio for myco.io")

def generate_video(text):
    clip = TextClip(text, fontsize=70, color='white', size=(640, 480))
    clip = clip.set_duration(10)  # 10 seconds duration
    video = CompositeVideoClip([clip])
    video.write_videofile("output.mp4", fps=24)
    return "output.mp4"

def generate_audio(text):
    tts = gTTS(text)
    audio_file = "audio.mp3"
    tts.save(audio_file)
    return audio_file

def add_audio_to_video(video_file, audio_file):
    video = CompositeVideoClip([video_file])
    audio = AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    final_video.write_videofile("final_output.mp4", fps=24)
    return "final_output.mp4"

def generate_captions(text):
    captions = f"Captions: {text}"
    return captions

st.header("Generate Video")
user_input = st.text_input("Enter text to generate video with audio and captions")
if st.button("Generate"):
    if user_input:
        video_file = generate_video(user_input)
        audio_file = generate_audio(user_input)
        final_video_file = add_audio_to_video(video_file, audio_file)
        captions = generate_captions(user_input)
        st.video(final_video_file)
        st.subheader("Captions")
        st.write(captions)
    else:
        st.error("Please enter some text to generate video")

from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip

st.set_page_config(page_title="AI Content Creation Studio", layout="wide")

def generate_video(text):
    clip = TextClip(text, fontsize=70, color='white', size=(640, 480))
    clip = clip.set_duration(10)  # 10 seconds duration
    video = CompositeVideoClip([clip])
    video.write_videofile("output.mp4", fps=24)
    return "output.mp4"

def generate_audio(text):
    tts = gTTS(text)
    audio_file = "audio.mp3"
    tts.save(audio_file)
    return audio_file

def add_audio_to_video(video_file, audio_file):
    video = CompositeVideoClip([video_file])
    audio = AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    final_video.write_videofile("final_output.mp4", fps=24)
    return "final_output.mp4"

def generate_captions(text):
    captions = f"Captions: {text}"
    return captions

st.title("AI Content Creation Studio for myco.io")
st.sidebar.header("Settings")
st.sidebar.write("Configure your video generation settings")

user_input = st.sidebar.text_input("Enter text to generate video with audio and captions")
if st.sidebar.button("Generate"):
    if user_input:
        with st.spinner("Generating video..."):
            video_file = generate_video(user_input)
            audio_file = generate_audio(user_input)
            final_video_file = add_audio_to_video(video_file, audio_file)
            captions = generate_captions(user_input)
        st.video(final_video_file)
        st.subheader("Captions")
        st.write(captions)
    else:
        st.error("Please enter some text to generate video")

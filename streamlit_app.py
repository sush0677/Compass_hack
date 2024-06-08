import streamlit as st
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS
import os

# Streamlit page configuration
st.set_page_config(page_title="AI Content Creation Studio", layout="wide")

# Function to generate a video with text overlay
def generate_video(text):
    try:
        clip = TextClip(text, fontsize=70, color='white', size=(640, 480))
        clip = clip.set_duration(10)  # 10 seconds duration
        video = CompositeVideoClip([clip])
        video.write_videofile("output.mp4", fps=24)
        return "output.mp4"
    except Exception as e:
        st.error(f"Error generating video: {e}")
        return None

# Function to generate audio from text
def generate_audio(text):
    try:
        tts = gTTS(text)
        audio_file = "audio.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# Function to add audio to the video
def add_audio_to_video(video_file, audio_file):
    try:
        video = CompositeVideoClip([video_file])
        audio = AudioFileClip(audio_file)
        final_video = video.set_audio(audio)
        final_video.write_videofile("final_output.mp4", fps=24)
        return "final_output.mp4"
    except Exception as e:
        st.error(f"Error adding audio to video: {e}")
        return None

# Function to generate captions
def generate_captions(text):
    captions = f"Captions: {text}"
    return captions

# Streamlit UI setup
st.title("AI Content Creation Studio for myco.io")
st.sidebar.header("Settings")
st.sidebar.write("Configure your video generation settings")

# User input for text to generate video with audio and captions
user_input = st.sidebar.text_input("Enter text to generate video with audio and captions")

if st.sidebar.button("Generate"):
    if user_input:
        with st.spinner("Generating video..."):
            video_file = generate_video(user_input)
            if video_file:
                audio_file = generate_audio(user_input)
                if audio_file:
                    final_video_file = add_audio_to_video(video_file, audio_file)
                    if final_video_file:
                        captions = generate_captions(user_input)
                        st.video(final_video_file)
                        st.subheader("Captions")
                        st.write(captions)
    else:
        st.error("Please enter some text to generate video")

# Ensure to delete the generated files after displaying
if os.path.exists("output.mp4"):
    os.remove("output.mp4")
if os.path.exists("audio.mp3"):
    os.remove("audio.mp3")
if os.path.exists("final_output.mp4"):
    os.remove("final_output.mp4")

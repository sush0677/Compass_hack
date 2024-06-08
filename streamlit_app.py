import streamlit as st
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, VideoFileClip
from transformers import pipeline
from moviepy.video.fx.all import resize
import cv2
import numpy as np

st.set_page_config(page_title="AI Content Creation Studio", layout="wide")

def generate_video(text, duration=10):
    # Create a video with dynamic background and text overlay
    width, height = 640, 480
    background = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    video_file = "background.mp4"
    out = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

    for _ in range(duration * 24):
        out.write(background)
    out.release()

    # Add text overlay
    clip = VideoFileClip(video_file)
    txt_clip = (TextClip(text, fontsize=70, color='white', size=(width, height), method='caption')
                .set_duration(duration)
                .set_position('center'))

    video = CompositeVideoClip([clip, txt_clip])
    final_video_file = "output_video.mp4"
    video.write_videofile(final_video_file, fps=24)
    return final_video_file

def generate_audio(text):
    # Use Hugging Face's TTS model
    tts_pipeline = pipeline("text-to-speech", model="tts_model")
    audio = tts_pipeline(text)[0]["generated_audio"]
    audio_file = "audio.mp3"
    with open(audio_file, "wb") as f:
        f.write(audio)
    return audio_file

def add_audio_to_video(video_file, audio_file):
    # Combine video and audio
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    final_video_file = "final_output.mp4"
    final_video.write_videofile(final_video_file, fps=24)
    return final_video_file

def generate_captions(text):
    # Generate captions using AI-based summarization or other NLP techniques
    captions = f"Captions: {text}"
    return captions

st.title("AI Content Creation Studio for myco.io")
st.sidebar.header("Settings")
st.sidebar.write("Configure your video generation settings")

user_input = st.sidebar.text_area("Enter text to generate video with audio and captions")
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

# Adding footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed for the Compass Hackathon")

import streamlit as st
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS
import random
import spacy
from transformers import pipeline

# Initialize NLP model
nlp = spacy.load("en_core_web_sm")
sentiment_analysis = pipeline("sentiment-analysis")

st.set_page_config(page_title="AI Content Creation Studio", layout="wide")

def generate_video(text):
    # Generate a simple video with text overlay
    clip = TextClip(text, fontsize=70, color='white', size=(640, 480))
    clip = clip.set_duration(10)  # 10 seconds duration
    video = CompositeVideoClip([clip])
    video_file = "output.mp4"
    video.write_videofile(video_file, fps=24)
    return video_file

def generate_audio(text):
    # Generate audio using gTTS
    tts = gTTS(text)
    audio_file = "audio.mp3"
    tts.save(audio_file)
    return audio_file

def add_audio_to_video(video_file, audio_file):
    # Combine video and audio
    video = CompositeVideoClip([video_file])
    audio = AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    final_video_file = "final_output.mp4"
    final_video.write_videofile(final_video_file, fps=24)
    return final_video_file

def generate_captions(text):
    # Generate simple captions
    captions = f"Captions: {text}"
    return captions

def analyze_text(text):
    doc = nlp(text)
    sentiment = sentiment_analysis(text)
    keywords = [token.lemma_ for token in doc if token.is_stop is False and token.is_alpha]
    return sentiment, keywords

st.title("AI Content Creation Studio for myco.io")
st.sidebar.header("Settings")
st.sidebar.write("Configure your video generation settings")

user_input = st.sidebar.text_area("Enter text to generate video with audio and captions")
if st.sidebar.button("Generate"):
    if user_input:
        with st.spinner("Generating video..."):
            sentiment, keywords = analyze_text(user_input)
            video_file = generate_video(user_input)
            audio_file = generate_audio(user_input)
            final_video_file = add_audio_to_video(video_file, audio_file)
            captions = generate_captions(user_input)

        st.video(final_video_file)
        st.subheader("Captions")
        st.write(captions)
        
        st.subheader("Sentiment Analysis")
        st.write(f"Sentiment: {sentiment[0]['label']} (Score: {sentiment[0]['score']:.2f})")
        
        st.subheader("Keywords")
        st.write(", ".join(keywords))
    else:
        st.error("Please enter some text to generate video")

# Adding footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed for the Compass Hackathon")

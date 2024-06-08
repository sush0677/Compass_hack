# import streamlit as st
# from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
# from gtts import gTTS
# import random

# st.set_page_config(page_title="AI Content Creation Studio", layout="wide")

# def generate_video(text):
#     # Generate a simple video with text overlay
#     clip = clip.set_duration(10)  # 10 seconds duration
#     video = CompositeVideoClip([clip])
#     video_file = "output.mp4"
#     video.write_videofile(video_file, fps=24)
#     return video_file

# def generate_audio(text):
#     # Generate audio using gTTS
#     tts = gTTS(text)
#     audio_file = "audio.mp3"
#     tts.save(audio_file)
#     return audio_file

# def add_audio_to_video(video_file, audio_file):
#     # Combine video and audio
#     video = CompositeVideoClip([video_file])
#     audio = AudioFileClip(audio_file)
#     final_video = video.set_audio(audio)
#     final_video_file = "final_output.mp4"
#     final_video.write_videofile(final_video_file, fps=24)
#     return final_video_file

# def generate_captions(text):
#     # Generate simple captions
#     captions = f"Captions: {text}"
#     return captions

# st.title("AI Content Creation Studio for myco.io")
# st.sidebar.header("Settings")
# st.sidebar.write("Configure your video generation settings")

# user_input = st.sidebar.text_input("Enter text to generate video with audio and captions")
# if st.sidebar.button("Generate"):
#     if user_input:
#         with st.spinner("Generating video..."):
#             video_file = generate_video(user_input)
#             audio_file = generate_audio(user_input)
#             final_video_file = add_audio_to_video(video_file, audio_file)
#             captions = generate_captions(user_input)
        
#         st.video(final_video_file)
#         st.subheader("Captions")
#         st.write(captions)
#     else:
#         st.error("Please enter some text to generate video")

# # Adding footer
# st.sidebar.markdown("---")
# st.sidebar.markdown("Developed for the Compass Hackathon")
import streamlit as st
import moviepy.editor as mp
import cv2
from google.cloud import speech

# Function to create video
def create_video(frames, output_file):
    height, width, layers = frames[0].shape
    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))

    for frame in frames:
        video.write(frame)

    video.release()

# Function to add audio
def add_audio_to_video(video_file, audio_file, output_file):
    video = mp.VideoFileClip(video_file)
    audio = mp.AudioFileClip(audio_file)
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_file)

# Function to transcribe audio
def transcribe_audio(audio_path):
    client = speech.SpeechClient()
    with open(audio_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    captions = [result.alternatives[0].transcript for result in response.results]
    return captions

# Streamlit UI
st.title("AI Video Generator")

uploaded_video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
uploaded_audio = st.file_uploader("Upload Audio", type=["mp3", "wav"])
generate_captions = st.checkbox("Generate Captions")

if st.button("Generate Video"):
    if uploaded_video and uploaded_audio:
        video_path = f"uploaded_{uploaded_video.name}"
        audio_path = f"uploaded_{uploaded_audio.name}"

        # Save uploaded files
        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())

        # Create video with audio
        output_video_path = "output_video_with_audio.mp4"
        add_audio_to_video(video_path, audio_path, output_video_path)
        
        st.video(output_video_path)

        # Generate captions if selected
        if generate_captions:
            captions = transcribe_audio(audio_path)
            st.write("Captions: ", captions)

# Run Streamlit app
if __name__ == "__main__":
    st.run()

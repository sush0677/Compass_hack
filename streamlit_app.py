import streamlit as st
import whisper
from transformers import pipeline

# Function to extract video description
def extract_video_description(video_path):
    # Load the pre-trained Whisper model
    model = whisper.load_model("base")
    
    # Transcribe the video
    result = model.transcribe(video_path)
    transcript = result['text']
    
    return transcript

# Function to translate text
def translate_text(text, target_language):
    # Load the translation pipeline with a specific model
    if target_language == "arabic":
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")
    else:
        raise ValueError("Target language not supported.")
    
    # Split text into chunks to avoid exceeding model limits
    max_length = 512  # Model-specific token limit
    text_chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    # Translate each chunk
    translated_text = ""
    for chunk in text_chunks:
        translation = translator(chunk)
        translated_text += translation[0]['translation_text'] + " "
    
    return translated_text.strip()

# Streamlit app
def main():
    st.title("Video Transcription and Translation App")

    # Upload video file
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mkv", "avi", "mov"])

    if uploaded_file is not None:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_file.read())

        st.write("Extracting transcript...")
        transcript = extract_video_description("temp_video.mp4")
        st.write("Transcript:")
        st.write(transcript)

        target_language = st.selectbox("Select target language for translation", ["arabic"])

        if st.button("Translate Transcript"):
            st.write("Translating transcript...")
            translated_text = translate_text(transcript, target_language)
            st.write("Translated Text:")
            st.write(translated_text)

if __name__ == "__main__":
    main()

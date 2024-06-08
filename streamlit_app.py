import streamlit as st
import whisper
from transformers import pipeline

def extract_video_description(video_path):
    # Load the pre-trained Whisper model
    model = whisper.load_model("base")
    
    # Transcribe the video
    result = model.transcribe(video_path)
    transcript = result['text']
    
    return transcript

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

def main():
    st.title("Video Description Extractor and Translator")
    
    # File uploader
    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])
    
    # Language selector
    target_language = st.selectbox("Select target language", ["arabic"])
    
    if st.button("Extract and Translate"):
        if video_file is not None:
            with st.spinner("Extracting transcript..."):
                transcript = extract_video_description(video_file)
                st.write("Video Transcript:", transcript)
            
            with st.spinner("Translating text..."):
                translated_text = translate_text(transcript, target_language)
                st.write("Translated Text:", translated_text)
        else:
            st.error("Please upload a video file.")

if __name__ == "__main__":
    main()

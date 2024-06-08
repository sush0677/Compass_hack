import streamlit as st
import whisper
from transformers import pipeline
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.effects import normalize

# Function to extract audio from video
def extract_audio_from_video(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

# Function to enhance audio
def enhance_audio(input_audio_path, output_audio_path):
    audio = AudioSegment.from_file(input_audio_path)
    normalized_audio = normalize(audio)
    normalized_audio.export(output_audio_path, format="wav")

# Function to extract video description with timestamps
def extract_video_description_with_timestamps(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result['segments']

# Function to format captions
def format_captions(segments):
    captions = []
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        captions.append({
            'start': start_time,
            'end': end_time,
            'text': text
        })
    return captions

# Function to translate text
def translate_text(text, target_language):
    if target_language == "arabic":
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ar")
    else:
        raise ValueError("Target language not supported.")
    
    max_length = 512
    text_chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    translated_text = ""
    for chunk in text_chunks:
        translation = translator(chunk)
        translated_text += translation[0]['translation_text'] + " "
    
    return translated_text.strip()

# Streamlit app
st.title("Video Transcription and Translation App")

video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

if video_file is not None:
    video_path = f"/tmp/{video_file.name}"
    with open(video_path, "wb") as f:
        f.write(video_file.getbuffer())
    
    st.video(video_file)

    # Extract audio
    audio_path = "/tmp/extracted_audio.wav"
    extract_audio_from_video(video_path, audio_path)
    st.success("Audio extracted successfully!")

    # Enhance audio
    enhanced_audio_path = "/tmp/enhanced_audio.wav"
    enhance_audio(audio_path, enhanced_audio_path)
    st.success("Audio enhanced successfully!")

    # Transcribe video
    segments = extract_video_description_with_timestamps(enhanced_audio_path)
    captions = format_captions(segments)

    # Display transcript
    transcript = " ".join([caption['text'] for caption in captions])
    st.subheader("Video Transcript")
    st.write(transcript)

    # Translate transcript
    target_language = st.selectbox("Select target language", ["arabic"])
    if st.button("Translate"):
        translated_text = translate_text(transcript, target_language)
        st.subheader("Translated Text")
        st.write(translated_text)

    # Save captions to SRT
    srt_path = "/tmp/captions.srt"
    with open(srt_path, 'w') as f:
        for i, caption in enumerate(captions, start=1):
            start = caption['start']
            end = caption['end']
            text = caption['text']
            start_h, start_m, start_s = int(start // 3600), int((start % 3600) // 60), start % 60
            end_h, end_m, end_s = int(end // 3600), int((end % 3600) // 60), end % 60
            f.write(f"{i}\n")
            f.write(f"{start_h:02}:{start_m:02}:{start_s:06.3f} --> {end_h:02}:{end_m:02}:{end_s:06.3f}\n")
            f.write(f"{text}\n\n")
    
    with open(srt_path, "rb") as file:
        st.download_button("Download Captions (SRT)", file, file_name="captions.srt")

st.caption("Developed by [Your Name]")

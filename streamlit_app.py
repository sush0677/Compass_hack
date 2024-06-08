import streamlit as st
import whisper
from transformers import pipeline
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.effects import normalize

def extract_audio_from_video(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def enhance_audio(input_audio_path, output_audio_path):
    audio = AudioSegment.from_file(input_audio_path)
    normalized_audio = normalize(audio)
    normalized_audio.export(output_audio_path, format="wav")

def extract_video_description_with_timestamps(video_path):
    # Load the pre-trained Whisper model
    model = whisper.load_model("base")

    # Transcribe the video with timestamps
    result = model.transcribe(video_path)
    segments = result['segments']

    return segments

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
    st.title("Video Description Extractor and Translator")
    
    # Upload video file
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])
    
    if uploaded_file is not None:
        video_path = "uploaded_video.mp4"
        audio_path = "extracted_audio.wav"
        enhanced_audio_path = "enhanced_audio.wav"

        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success("Video file uploaded successfully.")
        
        # Extract and enhance audio
        with st.spinner("Extracting and enhancing audio..."):
            extract_audio_from_video(video_path, audio_path)
            enhance_audio(audio_path, enhanced_audio_path)
        
        # Extract transcript with timestamps
        with st.spinner("Extracting transcript with timestamps..."):
            segments = extract_video_description_with_timestamps(enhanced_audio_path)
            captions = format_captions(segments)
        
        st.subheader("Video Captions")
        for caption in captions:
            start = caption['start']
            end = caption['end']
            text = caption['text']
            st.write(f"[{start:.2f} - {end:.2f}] {text}")

        # Optionally, save captions to a file (e.g., SRT format)
        with open('captions.srt', 'w') as f:
            for i, caption in enumerate(captions, start=1):
                start = caption['start']
                end = caption['end']
                text = caption['text']
                start_h, start_m, start_s = int(start // 3600), int((start % 3600) // 60), start % 60
                end_h, end_m, end_s = int(end // 3600), int((end % 3600) // 60), end % 60
                f.write(f"{i}\n")
                f.write(f"{start_h:02}:{start_m:02}:{start_s:06.3f} --> {end_h:02}:{end_m:02}:{end_s:06.3f}\n")
                f.write(f"{text}\n\n")

        st.success("Captions saved to captions.srt")

        # Translate text
        transcript = " ".join([caption['text'] for caption in captions])
        target_language = st.selectbox("Select target language for translation", ["arabic"])
        
        if st.button("Translate"):
            with st.spinner("Translating text..."):
                translated_text = translate_text(transcript, target_language)
            st.subheader("Translated Text")
            st.write(translated_text)

if __name__ == "__main__":
    main()

import streamlit as st
import cv2
import numpy as np
from sklearn.decomposition import PCA

# Function to read video and extract frames
def extract_frames(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames
    except Exception as e:
        st.error(f"Error in extracting frames: {e}")

# Function to optimize features using PCA
def optimize_features(frames, n_components=50):
    try:
        flattened_frames = [frame.flatten() for frame in frames]
        pca = PCA(n_components=n_components)
        pca_frames = pca.fit_transform(flattened_frames)
        return pca, pca_frames
    except Exception as e:
        st.error(f"Error in optimizing features: {e}")

# Streamlit app
st.title('Video Feature Optimization Tool')

# File uploader
video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if video_file is not None:
    try:
        video_path = 'temp_video.mp4'
        with open(video_path, 'wb') as f:
            f.write(video_file.getbuffer())

        # Extract frames
        frames = extract_frames(video_path)
        st.write(f"Total frames extracted: {len(frames)}")

        # Display a few frames
        st.write("Sample Frames:")
        for i in range(0, len(frames), max(1, len(frames)//10)):
            st.image(cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB), caption=f"Frame {i}")

        # Optimize features
        st.write("Optimizing features...")
        pca, pca_frames = optimize_features(frames)
        st.write(f"Features reduced to {pca.n_components_} components.")

        # Display PCA components
        st.write("PCA Components (Sample):")
        st.write(pca_frames[:10])

    except Exception as e:
        st.error(f"An error occurred: {e}")

st.write("Developed by [Your Name]")

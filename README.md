### AI Video Optimization Tool for Myco.io - Compass Hackathon

## Project Description

During the **Compass Hackathon** in Abu Dhabi, my teammate and I developed an AI-powered tool for **Myco.io** aimed at optimizing video content. The objective was to create an innovative solution that could automatically enhance videos using artificial intelligence, tailored specifically for content creators and platforms requiring optimized media.

We utilized OpenAI's **Whisper** model for audio transcription and processing, and built an interactive user interface using **Streamlit**. The project also incorporated libraries like **moviepy**, **pydub**, and **transformers** to handle various video and audio processing tasks effectively.

## Key Contributions:

- **Audio Transcription with Whisper**: Employed OpenAI's **Whisper** model to transcribe audio from video files, enabling features like automated subtitles and audio analysis.
  
- **Video and Audio Processing**: Utilized **moviepy** and **pydub** libraries to edit and enhance video and audio tracks, including normalization and noise reduction.
  
- **Interactive UI with Streamlit**: Developed a user-friendly interface using **Streamlit**, allowing users to upload videos and receive optimized outputs seamlessly.
  
- **NLP Enhancements with Transformers**: Integrated the **transformers** library from Hugging Face to perform advanced NLP tasks, enhancing the AI capabilities of the tool.
  
- **Team Collaboration and Rapid Development**: Overcame challenges of team member withdrawals and successfully built a functional prototype within 24 hours as a 2-member team.

## Technologies Used

- **Python** for programming.
- **OpenAI Whisper** for speech recognition and transcription.
- **Streamlit** for building the web application interface.
- **moviepy** (`import moviepy.editor as mp`) for video editing and processing.
- **pydub** and **pydub.effects** for audio manipulation and normalization.
- **Transformers** library for natural language processing tasks.

## Code Snippets

Here's an overview of some key code components used in the project:

```python
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.effects import normalize
import whisper
from transformers import pipeline
```

- **Video to Audio Conversion**: Extracted audio from video files using `moviepy`.
- **Audio Normalization**: Used `pydub` to normalize audio levels for better transcription accuracy.
- **Speech Recognition**: Applied `whisper` for transcribing audio content.
- **NLP Tasks**: Leveraged `transformers` for tasks like summarization and sentiment analysis.

## Hackathon Highlights

- **Event**: Compass Hackathon (Abu Dhabi)
- **Duration**: 24 hours
- **Team Size**: 2 members (Myself and Vivek)
- **Project**: AI-powered video optimization tool for Myco.io
- **Outcome**: Developed a functional AI tool that enhances video content, providing value to the Myco.io platform and its users.

## Project Overview

- **Team Members**: Sushant, Vivek
- **Objective**: To create an AI-driven tool that automates video optimization processes, including transcription, enhancement, and content analysis for Myco.io.
- **Challenges Overcome**:
  - Adjusted to a smaller team due to member withdrawals.
  - Managed time constraints to deliver a working prototype within 24 hours.
  - Integrated multiple technologies to achieve seamless functionality.

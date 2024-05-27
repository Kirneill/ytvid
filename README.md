Certainly! Below is a formatted README.md that you can directly copy and paste. This README provides an overview of your project, prerequisites, setup instructions, and how to run the script.

```markdown
# Video to Text Transcription

This project includes a Python script that automates the transcription of video files into text using the OpenAI API and `ffmpeg`. It processes video files within a specified directory, converts them into audio format, splits the audio into manageable chunks, transcribes the chunks, and saves the transcription to text files.

## Prerequisites

Before running this script, ensure you have the following installed:

- **Python 3.6+**
- **ffmpeg**: This is required for converting video files into audio files.
- **pydub**: A Python library used for manipulating audio.
- **openai**: The OpenAI Python client library.

You will also need an API key from OpenAI.

## Setup

1. **Install Required Python Libraries**:
   ```bash
   pip install pydub openai
   ```

2. **Install ffmpeg**:
   - For Windows, download and set up ffmpeg from [FFmpeg.org](https://ffmpeg.org/download.html).
   - For MacOS, you can install ffmpeg using Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - For Linux:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

3. **Set up Environment Variables**:
   Ensure that your OpenAI API key is available as an environment variable:
   ```bash
   export OPENAI_API_KEY='your_api_key_here'
   ```

## Usage

Place your video files (.mp4) in a directory and specify this directory when running the script. The script will process all mp4 files in the directory, transcribe them, and save the transcripts as .txt files named after the original video files.

To run the script, use:
```bash
python path_to_script.py
```

Replace `path_to_script.py` with the actual path to the script if not running from the script's directory.

## What the Script Does

1. **Converts Video to Audio**: Uses `ffmpeg` to convert video files to audio (mp3 format).
2. **Splits Audio into Chunks**: Breaks down the audio file into 30-second chunks for easier processing.
3. **Transcribes Audio**: Each audio chunk is sent to the OpenAI API, which returns the transcribed text.
4. **Saves Transcriptions**: The transcriptions are saved in text files corresponding to each video file.

## Notes

- Ensure that the `ffmpeg` command is accessible from your terminal/command prompt.
- Check the `OPENAI_API_KEY` environment variable if there are issues with accessing the OpenAI services.

```

This README.md file provides a comprehensive guide for setting up and running your video to text transcription project. It includes clear instructions on prerequisites, installation, and usage, making it easy for users to get started with the script.
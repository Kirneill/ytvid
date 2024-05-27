import os
from openai import OpenAI
from pydub import AudioSegment

def initialize_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables. Please set 'OPENAI_API_KEY'.")
    return OpenAI(api_key=api_key)

def convert_video_to_audio(video_path):
    audio_file_path = video_path.replace('.mp4', '.mp3')
    ffmpeg_command = f"ffmpeg -i {video_path} -q:a 0 -map a {audio_file_path}"
    os.system(ffmpeg_command)
    return audio_file_path


def transcribe_audio(client, audio_file_path):
    """
    Transcribes the audio file into text using the specified client.

    Args:
        client (object): The client object used for transcribing the audio.
        audio_file_path (str): The path to the audio file.

    Returns:
        str: The full transcript of the audio file.

    Raises:
        Exception: If an error occurs during the transcription process.
    """
    audio = AudioSegment.from_mp3(audio_file_path)
    chunk_length_ms = 30000  # 30 seconds
    chunks = make_chunks(audio, chunk_length_ms)

    full_transcript = ""
    for i, chunk in enumerate(chunks):
        chunk_file = f"{audio_file_path[:-4]}_chunk{i}.mp3"
        chunk.export(chunk_file, format="mp3")
        try:
            with open(chunk_file, "rb") as audio_file:
                # Assuming the API directly returns the transcribed text
                transcript_text = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                if transcript_text.strip():  # Checking if the transcription text is not empty
                    print(f"Response for chunk {i}: {transcript_text}")
                    full_transcript += transcript_text + " "
                else:
                    print(f"Failed to transcribe chunk {i}: Received empty transcription.")
        except Exception as e:
            print(f"An error occurred while transcribing chunk {i}: {e}")
        finally:
            os.remove(chunk_file)  # Cleanup

    return full_transcript


def make_chunks(audio_segment, chunk_length_ms):
    """
    Breaks an AudioSegment into chunks of a specific length.

    Parameters:
    audio_segment (AudioSegment): The audio segment to be broken into chunks.
    chunk_length_ms (int): The length of each chunk in milliseconds.

    Returns:
    list: A list of AudioSegments, each representing a chunk of the original audio segment.
    """
    length_ms = len(audio_segment)  # Length of the audio in milliseconds
    return [audio_segment[i:i + chunk_length_ms] for i in range(0, length_ms, chunk_length_ms)]

def main(folder_path):
    """
    Transcribes audio from video files in a given folder.

    Args:
        folder_path (str): The path to the folder containing the video files.

    Returns:
        None
    """
    client = initialize_client()
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            video_path = os.path.join(folder_path, filename)
            audio_file_path = convert_video_to_audio(video_path)
            transcript = transcribe_audio(client, audio_file_path)

            if transcript.strip():  # Checking if transcript contains non-space characters
                txt_filename = audio_file_path.replace('.mp3', '.txt')  # Name the text file after the audio file
                with open(txt_filename, 'w') as txt_file:
                    txt_file.write(transcript)
            else:
                print(f"Failed to transcribe video: {video_path}")

if __name__ == "__main__":
    main('F:/ytvid')  # Set your folder path here


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
    audio = AudioSegment.from_mp3(audio_file_path)
    chunk_length_ms = 30000  # 30 seconds
    chunks_filename = audio_file_path.replace('.mp3', '_chunks.txt')

    # Check if the chunks file already exists
    if os.path.exists(chunks_filename):
        print(f"Chunks file '{chunks_filename}' already exists. Skipping transcription.")
        # Optionally, you could read and return the existing content here
        with open(chunks_filename, 'r') as file:
            return file.read()

    # If the file does not exist, proceed with creating chunks and transcribing them
    chunks = make_chunks(audio, chunk_length_ms)
    full_transcript = ""

    with open(chunks_filename, 'w') as file:
        for i, chunk in enumerate(chunks):
            chunk_file = f"{audio_file_path[:-4]}_chunk{i}.mp3"
            chunk.export(chunk_file, format="mp3")
            try:
                with open(chunk_file, "rb") as audio_file:
                    transcript_text = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )
                    if transcript_text.strip():  # Checking if the transcription text is not empty
                        print(f"Response for chunk {i}: {transcript_text}")
                        file.write(f"Chunk {i}:\n{transcript_text}\n\n")
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


def gpt4_api_request(client, prompt, system_message):
    """
    Sends a request to the GPT-4 API for generating a response based on the given prompt and system message.

    Args:
        prompt (str): The user's input prompt.
        system_message (str): The system message to provide context for the prompt.

    Returns:
        str: The generated response from the GPT-4 model.
    """
    client = initialize_client()
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4",
        temperature=0.7,
        max_tokens=1500,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content.strip()

def generate_youtube_content(client, transcript):
    titles_prompt = f"Generate 5 novel attention-grabbing titles for the following transcript:\n{transcript}"
    titles = gpt4_api_request(client, titles_prompt, "You are a master class content creator.").split('\n')

    description_prompt = f"Provide a description related to what users usually search for based on the following transcript:\n{transcript}"
    description = gpt4_api_request(client, description_prompt, "You are a master class content creator.")

    tags_prompt = f"Provide tags that users usually search for and are related to the following transcript:\n{transcript}"
    tags = gpt4_api_request(client, tags_prompt, "You are a master class content creator.").split(',')

    timestamps_prompt = f"Provide timestamps and short interesting and attention-grabbing titles in a format that YouTube uses for the following transcript:\n{transcript}"
    timestamps_titles = gpt4_api_request(client, timestamps_prompt, "You are a master class content creator.")

    return {
        'titles': titles,
        'description': description,
        'tags': tags,
        'timestamps_titles': timestamps_titles
    }

def main(folder_path):
    client = initialize_client()
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            video_path = os.path.join(folder_path, filename)
            audio_file_path = convert_video_to_audio(video_path)
            transcript = transcribe_audio(client, audio_file_path)

            # Save the transcript to a file named after the video
            transcript_filename = filename.replace('.mp4', '.txt')
            with open(os.path.join(folder_path, transcript_filename), 'w') as transcript_file:
                transcript_file.write(transcript)

            if transcript.strip():
                youtube_content = generate_youtube_content(client, transcript)
                details_filename = filename.replace('.mp4', '_youtubedetails.txt')
                with open(os.path.join(folder_path, details_filename), 'w') as content_file:
                    content_file.write("Titles:\n" + "\n".join(youtube_content['titles']) + "\n\n")
                    content_file.write("Description:\n" + youtube_content['description'] + "\n\n")
                    content_file.write("Tags:\n" + ",".join(youtube_content['tags']) + "\n\n")
                    content_file.write("Timestamps and Titles:\n" + youtube_content['timestamps_titles'] + "\n")
            else:
                print(f"Failed to transcribe video: {video_path}")


if __name__ == "__main__":
    main('F:/ytvid')  # Set your folder path here
 
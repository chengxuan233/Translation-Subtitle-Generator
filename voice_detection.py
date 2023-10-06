import os
import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment
from pydub.silence import split_on_silence


# Extract audio from video
def extract_audio_from_video(video_file, audio_file):
    video = VideoFileClip(video_file)
    video.audio.write_audiofile(audio_file)


# Convert audio to text with timestamps
def audio_to_text(audio_file):
    r = sr.Recognizer()

    # Use pydub to split the audio file into chunks on silence
    audio_chunks = split_on_silence(
        AudioSegment.from_wav(audio_file),
        min_silence_len=500,
        silence_thresh=-40
    )

    results = []

    for i, chunk in enumerate(audio_chunks):
        chunk_filename = f"chunk{i}.wav"
        chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.listen(source)

            try:
                # Recognize the chunk
                text = r.recognize_google(audio_listened, show_all=True)

                # Calculate start and end times
                start_time = sum([c.duration_seconds for c in audio_chunks[:i]])
                end_time = start_time + chunk.duration_seconds

                # Append to results
                results.append({
                    'text': text,
                    'start_time': start_time,
                    'end_time': end_time
                })

            except sr.UnknownValueError:
                print(f"Chunk {i} could not be recognized")
            except sr.RequestError:
                print("API unavailable")

    return results


if __name__ == "__main__":
    output_txt_path = 'recognized_text.txt'  # Define the path for the output text file
    video_path = 'peppa pig.mp4'
    audio_path = 'extracted_audio.wav'

    extract_audio_from_video(video_path, audio_path)
    text_results = audio_to_text(audio_path)

    with open(output_txt_path, 'w') as file:  # Open the txt file in write mode
        for result in text_results:
            line = f"{result['start_time']}s to {result['end_time']}s: {result['text']}\n"
            file.write(line)  # Write each line to the txt file

    print(f"Recognized text has been written to {output_txt_path}")

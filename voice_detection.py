# import whisper

# model = whisper.load_model("base")
# result = model.transcribe("peppa pig.mp4")
# print(result["text"])
import whisper


def estimate_timestamps(text, total_duration):
    sentences = text.split('. ')
    duration_per_sentence = total_duration / len(sentences)
    timestamps = [(i * duration_per_sentence, (i + 1) * duration_per_sentence) for i in range(len(sentences))]
    return [
        {"sentence": sentence.strip() + ".", "timestamp_start": start, "timestamp_end": end}
        for sentence, (start, end) in zip(sentences, timestamps)
    ]


try:
    # Load model and transcribe video
    model = whisper.load_model("base")
    result = model.transcribe("peppa pig.mp4")

    # Total duration of the video in seconds
    total_duration = 300  # example duration - you should retrieve the actual duration

    # Get the estimated timestamps
    transcript = estimate_timestamps(result['text'], total_duration)

    # Save to a file
    with open("transcription.txt", "w") as file:
        for item in transcript:
            sentence = item["sentence"]
            start_time, end_time = item["timestamp_start"], item["timestamp_end"]
            file.write(f"{start_time}s to {end_time}s: {sentence}\n")

except FileNotFoundError:
    print("The specified file could not be found.")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")


import openai
import whisper

openai.api_key = ' your api key'


def translate_text(input_text, source_language, target_language):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": f"Translate the following {source_language} text to {target_language}: '{input_text}'"},
        ],
        max_tokens=150
    )

    translated_text = response['choices'][0]['message']['content'].strip()

    return translated_text


def translate_transcript(source_language, target_language):
    with open("transcription.txt", "r") as f:
        lines = f.readlines()

    translated_transcript = []

    for line in lines:
        # Split each line into timestamp and text parts
        parts = line.strip().split(': ')
        if len(parts) == 2:
            timestamp, text = parts[0], parts[1]
            # Translate only the text part
            translated_text = translate_text(text, source_language, target_language)
            # Reconstruct the line with the translated text and the preserved timestamp
            translated_line = f"{timestamp}: {translated_text}"
            translated_transcript.append(translated_line)
        else:
            # If the line doesn't contain a timestamp, add it as is
            translated_transcript.append(line.strip())

    return '\n'.join(translated_transcript)


source_lang = "English"
target_lang = "Chinese"

# Translate the entire transcript while preserving timestamps
translated_result = translate_transcript(source_lang, target_lang)
print(translated_result)

import openai

openai.api_key = 'your own api key'


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


# Example usage
source_lang = "English"
target_lang = "Chinese"
text_to_translate = "one two three "

translated_result = translate_text(text_to_translate, source_lang, target_lang)
print(translated_result)

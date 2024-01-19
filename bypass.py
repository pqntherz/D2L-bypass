import clipboard, keyboard, openai, pyttsx3, time
from termcolor import colored as tf

# Account key
openai.api_key = 'ADD_YOUR_API_KEY_HERE'

def get_ai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Provide the correct answer."},
                {"role": "user", "content": f"Question: {question}"},
            ]
        )

        ai_response = response['choices'][0]['message']['content']
        return ai_response

    except Exception as e:
        print(f'Error during AI request: {e}')
        return None

def announce_answer_on_audio(answer):
    tts = pyttsx3.init() # shouldn't keep reinitializing this, but it's fine for now.
    tts.setProperty('rate', 125)
    tts.setProperty('voice', tts.getProperty('voices')[1].id)
    tts.say(answer)
    tts.runAndWait()
    print(answer)

def handle_clipboard():
    try:
        copied_text = clipboard.paste().strip()

        if copied_text:
            answer = get_ai_response(copied_text)
            if answer:
                announce_answer_on_audio(answer)
        else:
            print(tf('Clipboard is empty or does not contain text.', 'white', 'on_red'))

    except Exception as e:
        print(tf(f'Error during clipboard handling: {e}', 'white', 'on_red'))

def on_press(e):
    if e.event_type == keyboard.KEY_DOWN:
        handle_clipboard()

keyboard.on_press_key('q', on_press, suppress=True)

if __name__ == "__main__":
    while True:
        time.sleep(0.1)

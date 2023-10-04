import openai
import playsound
import time
import threading
import speech_recognition as sr
import logging
import traceback
from gtts import gTTS
from initialize import init_openai



logging.basicConfig(level=logging.ERROR)  # Configures logging to show errors
lang = "en"

init_openai()

# Flag to signal when the text is currently being spoken
is_speaking = threading.Event()


def speak(text: str):
    """
    Speak the given text using gTTS (Google Text-to-Speech).

    Args:
    - text (str): The text to be spoken.

    Returns:
    - None
    """
    is_speaking.set()  # Signal that the program is speaking
    speech = gTTS(text=text, lang=lang, slow=False, tld="ie")
    speech.save("output.mp3")
    playsound.playsound("output.mp3")  # Play the audio
    time.sleep(len(text) * 0.06)  # Rough estimation to ensure the event clears after the text is spoken
    is_speaking.clear()  # Reset the speaking flag


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        try:
            audio = r.listen(source)
        except sr.UnknownValueError:
            logging.error("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

        said = ""
        try:
            said = r.recognize_google(audio).lower()
            print("You said", said)

            if "" in said:
                speak("Yes Adam?")
                messages = [
                    {"role": "system", "content": "You are a sassy assistant"},
                    {"role": "user", "content": said}
                ]
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=messages
                )
                print(completion)
                speak(completion.choices[0].message.content)

            if "stop" in said:
                speak("Okay.")
                return "stop"

        except sr.UnknownValueError:
            logging.error("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logging.error("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            logging.error("An unexpected error occurred: {0}".format(repr(e)))
            logging.error(traceback.format_exc())  # This will print the entire stack trace

    return said

while True:
    result = get_audio()
    if result == "stop":
        break


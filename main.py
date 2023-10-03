from dotenv import load_dotenv
import openai
import os


def init_openai():
    load_dotenv()
    openai.api_key = os.getenv("API_KEY")
    print("Key loaded.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init_openai()

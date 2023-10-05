import openai
from secret import api_key


def init_openai():
    openai.api_key = api_key
    print("Key loaded.")
    print("OpenAI API version: " + openai.__version__)
    print(openai.Engine.list())


if __name__ == '__main__':
    init_openai()

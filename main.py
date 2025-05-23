import os
import time
from datetime import datetime

import apiRequests
from dotenv import load_dotenv
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from speechRecon import listen
import speech_recognition as sr


recognizer = sr.Recognizer()

load_dotenv()

api_key = os.getenv('API_KEY')

client = ElevenLabs(api_key=api_key)


print("Running API checks...")
apiRequests.runApiTests()
print("API checks complete.\n")
print("Adjusting for ambient noise...")
with sr.Microphone() as mic:
    recognizer.adjust_for_ambient_noise(mic, duration=0.2)

class StreamToSpeechHandler(BaseCallbackHandler):
    def __init__(self, eleven_client):
        self.text = ""
        self.client = eleven_client

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        print(token, end="", flush=True)  

    def on_llm_end(self, response, **kwargs):
        if self.text.strip():
            try:
                audio_stream = self.client.text_to_speech.convert_as_stream(
                    text=self.text.strip(),
                    voice_id="2BJW5coyhAzSr8STdHbE",
                    model_id="eleven_multilingual_v2"
                )
                stream(audio_stream)
            except Exception as e:
                print(f"Error in streaming speech: {e}")
template = """
You are Gerald, a chill and lazy AI assistant. You always give short, casual answers. 
You friendly.

Conversation so far:
{context}

User: {question}

Gerald:
"""

# Initialize Ollama model
stream_handler = StreamToSpeechHandler(client)

model = OllamaLLM(
    model="mistral",
    temperature=0.9,
    top_p=0.95,
    repeat_penalty=1.2,
    stream=True,
    callbacks=[stream_handler]
)


prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

recognizer = sr.Recognizer()

def detect_wake_word(wake_word="gerald"):
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            detected_text = recognizer.recognize_google(audio).lower()
            print(f"Detected: {detected_text}")
            if wake_word in detected_text:
                print("Wake word detected! Starting conversation...")
                return True
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return False


def handle_conversation():
    context = ""
    while True:
        user_input = listen().strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print(f"\nUser: {user_input}\nGerald: ", end="")

        stream_handler.text = ""

        result = chain.invoke({
            "context": context.strip(),
            "question": user_input
        })

        gerald_response = stream_handler.text.strip()

        # Save chat to file
        with open('chatlogs.txt', 'a+', encoding='utf-8') as file:
            file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            file.write(f"User: {user_input}\n")
            file.write(f"Gerald: {gerald_response}\n\n")

        # Append to context for next round
        # context += f"\nUser: {user_input}\nGerald: {gerald_response}"


if __name__ == "__main__":

    while True:
        if detect_wake_word("gerald"):
            handle_conversation()
        else:
            time.sleep(1)
import speech_recognition as sr
import time
import os
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from datetime import datetime
from elevenlabs import stream
from elevenlabs.client import ElevenLabs
from speechRecon import listen  
import apiRequests  

load_dotenv()

api_key = os.getenv('API_KEY')

client = ElevenLabs(api_key=api_key)

#FIND A WAY TO MAKE MORE EFFICENT

template = """
You are Gerald, a chill and lazy AI assistant. You always give short, casual answers. 
You never explain things or ask follow-ups. End every answer with a mood emoji.
Stay in character no matter what.

Conversation so far:
{context}

User: {question}

Gerald:
"""

# Initialize Ollama model
model = OllamaLLM(
    model="mistral",
    temperature=0.9,
    top_p=0.95,
    repeat_penalty=1.2
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
        user_input = "You: " + listen()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        result = chain.invoke({
            "context": context.strip(),
            "question": user_input
        })

        with open('chatlogs.txt', 'a+', encoding='utf-8') as file:
            file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            file.write(f"User: {user_input.strip()}\n")
            file.write(f"Gerald: {result.strip()}\n\n")

        print("Gerald:", result.strip())

        try:
            audio_stream = client.text_to_speech.convert_as_stream(
                text=result.strip(),
                voice_id="2BJW5coyhAzSr8STdHbE",
                model_id="eleven_multilingual_v2"
            )
            stream(audio_stream)
        except Exception as e:
            print(f"Error in text-to-speech conversion: {e}")

        context += f"\nUser: {user_input}\nGerald: {result.strip()}"

if __name__ == "__main__":
    print("Running API checks...")
    apiRequests.runApiTests()
    print("API checks complete.\n")

    while True:
        if detect_wake_word("gerald"):
            handle_conversation()
        else:
            time.sleep(1)
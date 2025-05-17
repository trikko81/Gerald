import speech_recognition as sr  # type: ignore

recognizer = sr.Recognizer()

def listen():
    while True:
        try:
            with sr.Microphone() as mic:
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                print("Listening...")
                audio = recognizer.listen(mic, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio)
                text = text.lower()
                print(f"You: {text}")
                return text

        except sr.UnknownValueError:
            print("Could not understand.")
        except sr.RequestError as e:
            print(f"RequestError: {e}")
            return "error"
        except KeyboardInterrupt:
            print("\nListening stopped by el usuario!!.")
            return "stopped"

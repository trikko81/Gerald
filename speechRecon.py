import speech_recognition as sr  # type: ignore

recognizer = sr.Recognizer()

def listen():
    while True:
        try:
            with sr.Microphone() as mic:
                print()
                print("Listening...")
                audio = recognizer.listen(mic, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio)
                text = text.lower()
                return text

        except sr.WaitTimeoutError:
            print("No speech detected in time window.")
            return ""  

        except sr.UnknownValueError:
            print("Could not understand.")
            return ""  

        except sr.RequestError as e:
            print(f"RequestError: {e}")
            return "error"

        except KeyboardInterrupt:
            print("\nListening stopped by el usuario!!")
            return "stopped"

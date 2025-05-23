# Gerald — Your Chill AI Voice Buddy

Gerald is a laid-back AI assistant who listens when you say its name and answers your questions with short, casual responses. It talks out loud using cool text-to-speech voices and keeps track of your chats.

---

## What Can Gerald Do?

- Wake up when you say **"gerald"**
- Understand what you say and answer in a chill, friendly way
- Talk out loud using ElevenLabs text-to-speech
- Adjust for background noise to hear you better
- Save your conversations with timestamps
- Check if all the APIs it uses are working before starting

---

## What’s Inside?

- **Python** code using speech recognition and AI models
- ElevenLabs API for voice output
- Ollama LLM model for generating responses
- Handy functions to listen, talk, and handle API calls

---

## How to Get Gerald Running

1. **Download the code**
 
```git clone https://github.com/yourusername/gerald-assistant.git```
```cd gerald-assistant```

2. **Set up enviorment**

```python -m venv venv```
```source venv/bin/activate  # (On Windows, use venv\Scripts\activate)```
```pip install -r requirements.txt```

3. **Add your ElevenLabs API key**
-Make a .env file in the project folder
```API-KEY=eelvenlabsapi```

4. **Start Gerald**
```python main.py```

## How to Use Gerald

- Say **"gerald"** to wake it up  
- Talk to it — ask questions or say commands  
- Listen as it talks back in a friendly voice  
- Say **"exit"** to end the chat  

---

## How It Works — Simple Breakdown

- **Listening:** Uses your microphone and Google Speech Recognition to turn your voice into text.  
- **Thinking:** Sends your question to an AI model (Ollama) that generates a casual response.  
- **Talking:** Uses ElevenLabs to turn the AI’s text answer into speech you can hear.  
- **Logging:** Saves every conversation to a file with timestamps.  
- **API Checks:** Runs tests on ElevenLabs API to make sure everything is connected before starting.  

---

## Files You’ll Find

- `main.py` — The main program that ties everything together  
- `speechRecon.py` — Handles listening and converting speech to text  
- `apiRequests.py` — Deals with talking to ElevenLabs API and running tests  
- `chatlogs.txt` — Where your conversations are saved  

---

## License

This project is open source under the MIT License.

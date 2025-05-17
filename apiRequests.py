import requests
import os

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1"

HEADERS = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

def makeGetRequest(url, params=None):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[GET] {url} - Error: {e}")
        return None

def makePostRequest(url, data=None):
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[POST] {url} - Error: {e}")
        return None

def runApiTests():
    tests = [
        {
            "name": "List Voices",
            "method": "GET",
            "url": f"{BASE_URL}/voices",
            "expected_key": "voices"
        },
        {
            "name": "Text-to-Speech (default voice)",
            "method": "POST",
            "url": f"{BASE_URL}/text-to-speech/{getDefaultVoiceid()}",
            "data": {
                "text": "Hello from Eleven Labs test script!",
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            },
            "expected_key": None  
        }
    ]

    for test in tests:
        print(f"Running: {test['name']}")
        if test["method"] == "GET":
            result = makeGetRequest(test["url"])
        else:
            result = requests.post(
                test["url"],
                headers=HEADERS,
                json=test["data"]
            )
            if result.status_code == 200:
                print(f"{test['name']} passed. Audio data received.\n")
                continue
            else:
                print(f"{test['name']} failed: {result.text}\n")
                continue

        if result and (test["expected_key"] is None or test["expected_key"] in result):
            print(f"{test['name']} passed.\n")
        else:
            print(f"{test['name']} failed.\n")

def getDefaultVoiceid():
    data = makeGetRequest(f"{BASE_URL}/voices")
    if data and "voices" in data and len(data["voices"]) > 0:
        return data["voices"][0]["voice_id"]
    return "EXISTING_VOICE_ID"

if __name__ == "__main__":
    if not API_KEY:
        print("_API_KEY not set.")
    else:
        runApiTests()

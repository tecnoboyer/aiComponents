import openai
import os
import requests

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the text-to-speech API endpoint
TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"

# Define the headers for the API request
headers = {
    "Authorization": f"Bearer {openai.api_key}",
    "Content-Type": "application/json"
}

# Define the payload for the API request
payload = {
    "model": "tts-1",  # Replace with the correct model name if available
    "input": "I know how it feels to be overwhelmed by the endless tasks involved in the job hunt. The mountain of writing, the countless tailored resumes and cover letters… it's a lot.",
    "voice": "onyx",  # Options: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
    "response_format": "mp3"  # Options: "mp3", "opus", "aac", "flac"
}

# Make the API request
response = requests.post(TTS_ENDPOINT, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Save the audio as generate.mp3 in the same directory
    with open('generate.mp3', 'wb') as audio_file:
        audio_file.write(response.content)
    print("Audio saved as generate.mp3")
else:
    print(f"Failed to generate audio. Status code: {response.status_code}, Response: {response.text}")
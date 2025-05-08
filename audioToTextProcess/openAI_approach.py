from openai import OpenAI
import os

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Set your API key

# Transcribe audio
with open("basicOfFear.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="text"  # or "json" for structured output
    )

print(transcript)
import os
import requests
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt for the image
prompt = (
    "Presentation-quality digital illustration titled 'AI Readiness'. "
    "Left side: abstract AI brain made of circuits and binary code. "
    "Center: developer at desk writing code and interacting with a chat assistant on screen. "
    "Right side: ethical AI concerns – justice scale, surveillance eye, and padlock. "
    "Modern, clean, futuristic style with a blue-purple color scheme. 16:9 layout."
)

# Generate image
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",  # Landscape presentation format
    quality="hd",
    n=1
)

# Get image URL
image_url = response.data[0].url
print("Generated image URL:", image_url)

# Download and save the image in current directory
filename = "ai_readiness.png"
img_data = requests.get(image_url).content
with open(filename, "wb") as handler:
    handler.write(img_data)

print(f"Image saved as: {os.path.abspath(filename)}")

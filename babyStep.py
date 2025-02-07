import openai
import os

# Set your API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)

openai.api_key = api_key

def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace with the correct model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# Example usage
prompt = "Once upon a time"
output = generate_text(prompt)
print(output)

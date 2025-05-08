from openai import OpenAI
import os
import json

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Transcribe with full word-level details
with open("supraCaracas.m4a", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

# Save FULL TRANSCRIPTION
with open("full_transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript.text)  # The complete text content

# Extract problem words (confidence < 0.85)
problem_words = []
for segment in transcript.segments:
    for word in segment.words:
        if word.confidence < 0.85:
            problem_words.append({
                "word": word.word,
                "start": word.start,
                "end": word.end,
                "confidence": word.confidence,
                "context_sentence": segment.text  # The full sentence containing the word
            })

# Save PROBLEM WORDS as JSON (structured data)
with open("problem_words.json", "w", encoding="utf-8") as f:
    json.dump(problem_words, f, indent=2)

# Save PROBLEM WORDS as readable TXT
with open("pronunciation_analysis.txt", "w", encoding="utf-8") as f:
    f.write("PRONUNCIATION ANALYSIS REPORT\n")
    f.write("="*50 + "\n\n")
    f.write(f"Audio File: basicOfFear.mp3\n")
    f.write(f"Total Problem Words Found: {len(problem_words)}\n\n")
    
    for i, word in enumerate(problem_words, 1):
        f.write(f"{i}. WORD: {word['word'].upper()}\n")
        f.write(f"   • Confidence: {word['confidence']:.2f}/1.00\n")
        f.write(f"   • Position: {word['start']:.2f}-{word['end']:.2f} seconds\n")
        f.write(f"   • Context: \"{word['context_sentence']}\"\n")
        f.write(f"   • Practice: Listen and repeat 5 times at this timestamp\n")
        f.write("-"*50 + "\n")

print("Successfully generated:")
print("- full_transcript.txt (complete transcription)")
print("- problem_words.json (structured word data)")
print("- pronunciation_analysis.txt (practice guide)")
from pydub import AudioSegment
import whisper

# Convert MP3 to WAV (no FFmpeg needed for this step)
audio = AudioSegment.from_mp3("basicOfFear.mp3")
audio.export("temp.wav", format="wav")  # Uncompressed WAV

# Transcribe the WAV file
model = whisper.load_model("base")
result = model.transcribe("temp.wav")  # WAV doesn't require FFmpeg
print(result["text"])
import whisper
# Load The Whisper Model
model = whisper.load_model("base")

# Transcript The Audio File
result = model.transcribe("temp_audio.wav")

# Output The Transcription
print(result['text'])
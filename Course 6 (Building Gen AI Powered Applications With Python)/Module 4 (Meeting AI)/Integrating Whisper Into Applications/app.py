from flask import Flask, request
import whisper
import tempfile

app = Flask(__name__)

model = whisper.load_model("base")

@app.route("/", methods=["GET"])
def home():
    return {"message": "Whisper Audio Transcription API is running. Send a POST request to /transcribe with an audio file."}

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    # Get the uploaded audio file from the HTTP request
    audio_file = request.files["audio"]

    # Save the uploaded file temporarily so Whisper can process it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        audio_file.save(temp.name)

        # Convert the speech in the audio file to text
        result = model.transcribe(temp.name)

    # Return the transcription as a JSON response
    return {"transcription": result["text"]}

if __name__ == "__main__":
    # Start Flask Server
    app.run(debug=True)

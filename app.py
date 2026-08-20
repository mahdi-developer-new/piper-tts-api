from flask import Flask, request, send_file, jsonify
from piper import PiperVoice
import tempfile
import wave
import os

app = Flask(__name__)

MODEL_PATH = os.getenv("MODEL_PATH", "en_US-lessac-medium.onnx")

voice = PiperVoice.load(MODEL_PATH)

@app.get("/")
def home():
    return jsonify({"status": "Piper TTS API is running"})

@app.post("/tts")
def tts():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    output = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    output.close()

    with wave.open(output.name, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    return send_file(
        output.name,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="voice.wav"
                  )

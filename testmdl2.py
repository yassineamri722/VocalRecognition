import os
import queue
import sounddevice as sd
import sys
import json
from vosk import Model, KaldiRecognizer

# Set the model path
MODEL_PATH = "vosk-model-ar-mgb2-0.4\\vosk-model-ar-mgb2-0.4"

# Check if model exists
if not os.path.exists(MODEL_PATH):
    print("Model not found at", MODEL_PATH)
    print("Please make sure the model folder is in the correct path.")
    sys.exit(1)

# Load the model
print("Loading model...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Prepare queue and audio stream
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    q.put(bytes(indata))

# Start listening
try:
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("✔️ Speak into your microphone (Arabic)... Press Ctrl+C to stop.")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result.get("text"):
                    print("🗣 You said (Arabic):", result["text"])
            else:
                partial = json.loads(recognizer.PartialResult())
                if partial.get("partial"):
                    print("...Listening:", partial["partial"], end="\r")

except KeyboardInterrupt:
    print("\n🛑 Done.")
except Exception as e:
    print("Error:", str(e))

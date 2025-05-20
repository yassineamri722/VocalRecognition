import os
import vosk
import sounddevice as sd
import queue
import json
from gtts import gTTS
import pygame

# Set up model path
MODEL_PATH = "vosk-model-small-ar-tn-0.1-linto\\vosk-model-small-ar-tn-0.1-linto"  # Change this to the actual path

# Load the Vosk model
if not os.path.exists(MODEL_PATH):
    print("Model not found! Check the path.")
    exit(1)

vosk.SetLogLevel(-1)  # Disable verbose logs
model = vosk.Model(MODEL_PATH)

# Create a queue to store audio data
q = queue.Queue()

# Function to callback recorded audio
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

# Configure microphone stream
samplerate = 16000  # Most Vosk models use 16kHz sample rate
device = None  # Change to your specific microphone index if needed

# Initialize pygame mixer for playing audio files
pygame.mixer.init()

# Specify the location for the permanent file
audio_file_path = "audio_output.mp3"  # You can change this to any location

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                       dtype="int16", channels=1, callback=callback):
    print("Listening...")
    rec = vosk.KaldiRecognizer(model, samplerate)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            
            print("Recognized:", text)

            # If text is recognized, use gTTS for speech synthesis
            if text:
                tts = gTTS(text=text, lang='ar')  # Language set to Arabic ('ar')
                
                # Save the speech to a permanent file
                tts.save(audio_file_path)

                # Load and play the audio using pygame
                pygame.mixer.music.load(audio_file_path)
                pygame.mixer.music.play()

                # Wait for the audio to finish playing
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

                # After the audio is played, stop the mixer and remove the file
                pygame.mixer.music.stop()  # Stop the music to release the file
                os.remove(audio_file_path)  # Remove the file after stopping

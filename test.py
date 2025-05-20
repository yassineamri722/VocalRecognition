import os
import queue
import sounddevice as sd
import vosk
import asyncio
import edge_tts
import threading
from rapidfuzz import fuzz, process
import pygame
import datetime
import random
import json
import tempfile

class TunisianAssistant:
    def __init__(self, model_path):
        self.model = vosk.Model(model_path)
        self.q = queue.Queue()
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

        self.loop = asyncio.new_event_loop()
        t = threading.Thread(target=self.loop.run_forever, daemon=True)
        t.start()

        self.running = True

        self.responses = {
            "اهلا دار": ["اهلا غيث", "عسلامة"],
            "التوقيت": [lambda: f"توا الساعة {datetime.datetime.now().strftime('%H:%M')}"],
            "سكر الباب": ["سكرت الباب"],
            "سكر الشباك": ["سكرت الشباك"],
            "سكر الضوء": ["سكرت الضوء"],
            "عيشك": ["عيشك غيث"],  # trigger to stop
        }

        pygame.mixer.init()
        self.speak_lock = asyncio.Lock()

    async def speak_async(self, text):
        # Create a unique temporary file for each TTS output
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
            output_file = tf.name

        async with self.speak_lock:
            tts = edge_tts.Communicate(text=text, voice="ar-TN-HediNeural")
            await tts.save(output_file)
            try:
                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    await asyncio.sleep(0.1)
                pygame.mixer.music.stop()
                if hasattr(pygame.mixer.music, 'unload'):
                    pygame.mixer.music.unload()
            finally:
                try:
                    os.remove(output_file)
                except PermissionError:
                    await asyncio.sleep(1)
                    os.remove(output_file)

    def speak(self, text):
        asyncio.run_coroutine_threadsafe(self.speak_async(text), self.loop)

    async def respond(self, text):
        threshold = 70
        matches = process.extract(text, self.responses.keys(), scorer=fuzz.partial_ratio, limit=1)
        if matches and matches[0][1] >= threshold:
            key = matches[0][0]
            response = random.choice(self.responses[key])
            if callable(response):
                response = response()
            print("Assistant says:", response)
            await self.speak_async(response)
            if key == "عيشك":
                print("Assistant is closing...")
                await asyncio.sleep(2)
                self.running = False
        else:
            print("No good match found for:", text)

    def respond_sync(self, text):
        future = asyncio.run_coroutine_threadsafe(self.respond(text), self.loop)
        future.result()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio status:", status)
        self.q.put(bytes(indata))

    def run(self):
        with sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, dtype='int16',
                               channels=1, callback=self.audio_callback):
            print("Assistant started. Say something...")
            while self.running:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = json.loads(result).get("text", "")
                    if text:
                        print("You said:", text)
                        self.respond_sync(text)
            print("Assistant stopped.")

if __name__ == "__main__":
    MODEL_PATH = "vosk-model-small-ar-tn-0.1-linto\\vosk-model-small-ar-tn-0.1-linto"
    assistant = TunisianAssistant(MODEL_PATH)
    assistant.run()

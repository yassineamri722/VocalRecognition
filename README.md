
# 🎙️ Arabic Vocal Assistant (Tunisian Dialect)

This is a simple voice assistant project that recognizes spoken Arabic (Tunisian dialect) using the [Vosk](https://alphacephei.com/vosk/) speech recognition toolkit.

## 🧠 Model Requirement

Before running the project, you **must download** the appropriate speech recognition model:

* 🔗 [Download the model from Vosk](https://alphacephei.com/vosk/models)
* 📦 Model name: `vosk-model-small-ar-tn-0.1-linto`
* 📁 After downloading, **unzip** the model and place it in the project directory with the folder name exactly:

```
vosk-model-small-ar-tn-0.1-linto
```

## 🛠️ Installation

1. Install required dependencies:

```bash
pip install vosk pyaudio
```

> If `pyaudio` fails to install, try:

```bash
pip install pipwin
pipwin install pyaudio
```

2. Make sure your microphone is working and accessible by Python.

## ▶️ Usage

Run the main script:

```bash
python test.py
```

Replace `test.py` with the actual filename if needed.

## 🗣️ Features

* Offline speech recognition using Vosk
* Supports Arabic (Tunisian dialect)
* Light and fast model

## 📄 Notes

* No internet connection is required once the model is downloaded.
* Works best in quiet environments for accurate recognition.

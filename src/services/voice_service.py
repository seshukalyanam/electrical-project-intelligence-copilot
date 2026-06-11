from __future__ import annotations


def transcribe_audio_file(path: str) -> str:
    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_whisper(audio)
    except Exception as exc:
        return f"Voice transcription unavailable locally: {exc}"


def speak_text(text: str) -> str:
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "Spoken with local pyttsx3."
    except Exception as exc:
        return f"Local TTS unavailable: {exc}"

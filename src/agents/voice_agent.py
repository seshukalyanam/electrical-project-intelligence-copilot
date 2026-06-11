from __future__ import annotations

from src.agents.field_technician_agent import answer_for_field
from src.services.file_db_service import save_voice_transcript
from src.services.voice_service import speak_text, transcribe_audio_file


def handle_voice_question(project_id: str, model: str, manual_text: str = "", audio_path: str | None = None, speak: bool = False) -> dict:
    transcript = manual_text.strip()
    if not transcript and audio_path:
        transcript = transcribe_audio_file(audio_path)
    if not transcript:
        return {"transcript": "", "answer": "No voice transcript or manual question was provided.", "sources": []}
    result = answer_for_field(project_id, transcript, model)
    tts_status = speak_text(result["answer"]) if speak else "TTS not requested."
    save_voice_transcript(project_id, transcript, result["answer"])
    return {"transcript": transcript, "answer": result["answer"], "sources": result["sources"], "tts_status": tts_status}

# 🛠️ Tech Stack & Integrations

## Languages & Frameworks
- **Python 3.11** — Main programming language
- **FastAPI** — Web framework for building APIs ([docs](https://fastapi.tiangolo.com/))
- **Uvicorn** — ASGI server for FastAPI ([docs](https://www.uvicorn.org/))

## Key Libraries (requirements.txt)
- **httpx** — Async HTTP client ([docs](https://www.python-httpx.org/))
- **aiohttp** — Async HTTP client (used for multipart/form-data) ([docs](https://docs.aiohttp.org/))
- **pydantic** — Data validation and settings management ([docs](https://docs.pydantic.dev/))
- **loguru** — Logging utility ([docs](https://loguru.readthedocs.io/))
- **pydub** — Audio processing ([docs](https://github.com/jiaaro/pydub))
- **python-dotenv** — Loads environment variables from .env ([docs](https://saurabh-kumar.com/python-dotenv/))
- **google-cloud-dialogflow-cx** — Dialogflow CX API client ([docs](https://cloud.google.com/python/docs/reference/dialogflow-cx/latest))
- **google-cloud-texttospeech** — Google TTS API client ([docs](https://cloud.google.com/text-to-speech/docs/reference/libraries))

## System Dependencies
- **ffmpeg** — Audio conversion tool (installed in Docker image) ([docs](https://ffmpeg.org/))

## External APIs & Services
- **WhatsApp Business Cloud API (Meta)** — Receives and sends WhatsApp messages ([docs](https://developers.facebook.com/docs/whatsapp/))
- **Google Dialogflow CX** — Conversational AI ([docs](https://cloud.google.com/dialogflow/cx/docs))
- **Google Cloud Text-to-Speech** — Converts text to audio ([docs](https://cloud.google.com/text-to-speech/docs))
- **Google Cloud Run** — (Optional) For deployment ([docs](https://cloud.google.com/run))
- **ngrok** — (Optional) For local webhook testing ([docs](https://ngrok.com/))

## Project Structure
- `app/clients/` — WhatsApp API client
- `app/controllers/` — API endpoints (webhook)
- `app/middlewares/` — CORS middleware
- `app/models/` — Pydantic models for WhatsApp payloads
- `app/services/` — Business logic (Dialogflow, WhatsApp, TTS)
- `app/utils/` — Audio conversion, session management
- `json/` — Example payloads and responses
- `imgs/` — Images for documentation/tutorials

---
For more details, see `requirements.txt`, `Dockerfile`, and the codebase. 
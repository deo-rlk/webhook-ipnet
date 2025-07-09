# 📘 Detailed Guide: WhatsApp Business Webhook + Dialogflow CX

## Overview
This project is a FastAPI-based webhook that integrates WhatsApp Business API (Meta) with Google Dialogflow CX for conversational AI. It receives WhatsApp messages, processes them with Dialogflow, and sends responses back (text/audio).

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting API Keys & Credentials](#getting-api-keys--credentials)
3. [Project Setup](#project-setup)
4. [Environment Variables](#environment-variables)
5. [Dependency Installation](#dependency-installation)
6. [Running the Application](#running-the-application)
7. [Exposing Locally with ngrok](#exposing-locally-with-ngrok)
8. [Registering the Webhook with Meta](#registering-the-webhook-with-meta)
9. [Testing the Integration](#testing-the-integration)
10. [Troubleshooting & FAQ](#troubleshooting--faq)

---

## Prerequisites
- Python 3.11+
- Google Cloud account (Dialogflow CX & Text-to-Speech enabled)
- Meta (Facebook) Developer account with WhatsApp Business API access
- Docker (optional, for containerized run)
- ffmpeg (for audio conversion, installed automatically in Docker)

---

## Getting API Keys & Credentials
### 1. Google Cloud (Dialogflow CX & TTS)
- Create a Google Cloud project.
- Enable Dialogflow CX and Text-to-Speech APIs.
- Create a service account with access to these APIs.
- Download the `service-account.json` key file and place it in the project root.

### 2. Meta (WhatsApp Business API)
- Go to [Meta for Developers](https://developers.facebook.com/).
- Create an app and add the WhatsApp product.
- Get your:
  - WhatsApp Phone Number ID
  - WhatsApp Access Token
  - WhatsApp Sandbox/Test Number
- Define a **Verify Token** (any secret string) for webhook verification.

---

## Project Setup
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd ipnet-whatsapp-connector-main
   ```
2. **Add your `service-account.json`** to the project root.
3. **Create a `.env` file** (see below).

---

## Environment Variables
Create a `.env` file in the project root with:
```
DFCX_PROJECT_ID=your-dialogflow-project-id
DFCX_AGENT_ID=your-dialogflow-agent-id
META_WA_PHONE_NUMBER_ID=your-wa-phone-number-id
META_WA_ACCESS_TOKEN=your-wa-access-token
META_WA_VERIFY_TOKEN=your-verify-token
```

---

## Dependency Installation
### With Python (recommended for local dev):
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### With Docker:
```bash
docker build -t whatsapp-gateway .
```

---

## Running the Application
### Locally (Python):
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### With Docker:
```bash
docker run -p 8080:8080 --env-file .env -v $(pwd)/service-account.json:/app/service-account.json whatsapp-gateway
```

---

## Exposing Locally with ngrok
To receive webhooks from Meta, expose your local server:
```bash
ngrok http 8080
```
Copy the HTTPS URL provided by ngrok.

---

## Registering the Webhook with Meta
1. Go to your app in [Meta for Developers](https://developers.facebook.com/).
2. In WhatsApp > Configuration, add your ngrok/public URL + `/whatsapp/webhook` as the callback URL.
3. Enter your **Verify Token**.
4. Subscribe to the `messages` event.

---

## Testing the Integration
- Send a WhatsApp message to your sandbox/test number.
- Check logs/output for received messages and Dialogflow responses.
- Use the sample payloads in `json/` for local testing.

---

## Troubleshooting & FAQ
- **Google API errors:** Ensure your service account has the right permissions and the key file is present.
- **Meta webhook not verified:** Double-check your verify token and public URL.
- **Audio not working:** Ensure ffmpeg is installed (or use Docker).
- **.env not loaded:** Make sure `.env` is in the project root and variables are correct.
- **Port conflicts:** Change the port in the run command if 8080 is in use.

For more details, see the code and comments, or contact the project maintainer. 
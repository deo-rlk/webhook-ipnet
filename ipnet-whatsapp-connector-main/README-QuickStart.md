# 🚀 QuickStart: WhatsApp Business Webhook + Dialogflow CX

## Prerequisites
- Python 3.11+
- Docker (optional, for containerized run)
- Google Cloud service account key (Dialogflow CX & TTS)
- WhatsApp Business API credentials (from Meta)
- ffmpeg (if running locally, not in Docker)

## 1. Clone the Repository
```bash
git clone <repo-url>
cd ipnet-whatsapp-connector-main
```

## 2. Set Environment Variables
Create a `.env` file in the project root with:
```
DFCX_PROJECT_ID=your-dialogflow-project-id
DFCX_AGENT_ID=your-dialogflow-agent-id
META_WA_PHONE_NUMBER_ID=your-wa-phone-number-id
META_WA_ACCESS_TOKEN=your-wa-access-token
META_WA_VERIFY_TOKEN=your-verify-token
```
Place your Google Cloud `service-account.json` in the project root.

## 3. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## 4. Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

Or with Docker:
```bash
docker build -t whatsapp-gateway .
docker run -p 8080:8080 --env-file .env -v $(pwd)/service-account.json:/app/service-account.json whatsapp-gateway
```

## 5. Test the Webhook
- Use [ngrok](https://ngrok.com/) to expose port 8080 if testing locally:
  ```bash
  ngrok http 8080
  ```
- Register the public URL with Meta as your webhook.
- Send a WhatsApp message to your sandbox/test number.

---
For full details, see `README-Detailed.md`. 
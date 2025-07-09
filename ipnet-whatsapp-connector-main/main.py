import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from app.controllers.whatsapp_controller import WhatsAppController
from app.services.whatsapp_service import WhatsAppService
from app.services.dialogflow_service import DialogflowService
from app.clients.whatsapp_client import WhatsAppClient
from app.middlewares.cors_middleware import add_cors_middleware
from app.utils.session_manager import SessionManager
from app.services.tts_service import TextToSpeechService
load_dotenv(override=True)

app = FastAPI(title="WhatsApp Business API - FastAPI")

add_cors_middleware(app)

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'service-account.json'

tts_service = TextToSpeechService()
session_manager = SessionManager()
dialogflow_service = DialogflowService(
    project_id=os.getenv("DFCX_PROJECT_ID"),
    location="global",
    agent_id=os.getenv("DFCX_AGENT_ID"),
    session_manager=session_manager,
    tts_service=tts_service,
)

whatsapp_client = WhatsAppClient(
    base_url="https://graph.facebook.com/v22.0",
    phone_number_id=os.getenv("META_WA_PHONE_NUMBER_ID"),
    token=os.getenv("META_WA_ACCESS_TOKEN"),
)

whatsapp_service = WhatsAppService(
    whatsapp_client=whatsapp_client,
    dialogflow_service=dialogflow_service
)

whatsapp_controller = WhatsAppController(whatsapp_service=whatsapp_service)

app.include_router(whatsapp_controller.router)


@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "API is running!"}


# if __name__ == "__main__":
#     uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)

from typing import Dict, Any
import os
from app.services.dialogflow_service import DialogflowService
from app.clients.whatsapp_client import WhatsAppClient
from app.models.message_model import WhatsAppPayload
from app.utils.audio_utils import AudioUtils
import logging

logger = logging.getLogger(__name__)


class WhatsAppService:
    def __init__(self, whatsapp_client: WhatsAppClient, dialogflow_service: DialogflowService):
        self.whatsapp_client = whatsapp_client
        self.dialogflow_service = dialogflow_service

    async def process_message(self, data: Dict[str, Any]) -> Dict[str, str]:

        payload = WhatsAppPayload(**data)
        print(payload)
        if not payload or not payload.messages:
            logger.warning("Payload inválido ou sem mensagens: %s", data)
            return

        sender_id = payload.contacts[0].wa_id
        message = payload.messages[0]

        if message.type == "text":
            user_input = message.text.body
            response = await self.dialogflow_service.detect_intent_text(sender_id, user_input)
            return await self.whatsapp_client.send_message_text(sender_id, response)
            
        if message.type == "audio":
            audio_url = await self.whatsapp_client.get_media_url(message.audio.id)
            audio_bytes = await self.whatsapp_client.download_media(audio_url)
            
            converted_audio_bytes = AudioUtils.convert_whatsapp_audio_to_dialogflow(audio_bytes)
            audio_bytes = await self.dialogflow_service.detect_intent_audio(sender_id, converted_audio_bytes)

            audio_id = await self.whatsapp_client.upload_media_from_bytes(audio_bytes)
            response = await self.whatsapp_client.send_message_audio(sender_id, audio_id)
            
        logger.warning("Tipo de mensagem não suportado: %s", message.type)
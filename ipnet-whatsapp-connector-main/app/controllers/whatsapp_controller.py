import os
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from app.controllers.base_controller import BaseController
from app.services.whatsapp_service import WhatsAppService


class WhatsAppController(BaseController):
    def __init__(self, whatsapp_service: WhatsAppService):
        super().__init__(prefix="/whatsapp")
        self.whatsapp_service = whatsapp_service

    def register_routes(self):
        self.router.add_api_route("/webhook", self.check_webhook, methods=["GET"])
        self.router.add_api_route("/webhook", self.handle_webhook, methods=["POST"])

    async def check_webhook(self, request: Request):
        """Verifica a URL do webhook do WhatsApp."""
        verify_token = os.getenv("META_WA_VERIFY_TOKEN")
        query_params = request.query_params

        if query_params.get("hub.verify_token") == verify_token:
            challenge = query_params.get("hub.challenge")
            return PlainTextResponse(content=challenge)

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token inválido.")

    async def handle_webhook(self, request: Request):
        """Recebe mensagens do WhatsApp e processa via service."""
        try:
            data = await request.json()

            entry = data.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            content = changes.get("value", {})

            if "contacts" in content and "messages" in content:
                response = await self.whatsapp_service.process_message(content)
                return Response(status_code=200)
            else:
                print("Payload inválido ou sem mensagens.")
                return JSONResponse(status_code=200, content={"status": "ok"})
            
        except Exception as e:
            print(f"Erro no webhook do WhatsApp: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

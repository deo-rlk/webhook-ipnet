import httpx
from typing import Optional, Dict, Any
from aiohttp import FormData, ClientSession

""" Atualizar o código para que utilize apenas uma biblioteca para requisições HTTP"""

class WhatsAppClient:
    def __init__(self, base_url: str, phone_number_id: str, token: str):
        self.base_url = base_url
        self.phone_number_id = phone_number_id
        self.token = token


    async def _make_request(self, method: str, url: str, headers: Dict[str, str], json: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, json=json, files=files)
            response.raise_for_status()
            return response.json()


    async def send_message_text(self, recipient_id: str, text: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "text",
            "text": {"body": text}
        }

        return await self._make_request("POST", url, headers, json=payload)


    async def send_message_audio(self, recipient_id: str, media_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "audio",
            "audio": {
                "id": media_id
            }
        }

        response = await self._make_request("POST", url, headers, json=payload)
        return response


    async def get_media_url(self, media_id: str) -> str:
        url = f"{self.base_url}/{media_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = await self._make_request("GET", url, headers)
        return response.get("url")


    async def download_media(self, media_url: str) -> bytes:
        headers = {"Authorization": f"Bearer {self.token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(media_url, headers=headers)
            response.raise_for_status()
            return response.content


    async def upload_media_from_bytes(self, audio_bytes: bytes) -> str:
        url = f"{self.base_url}/{self.phone_number_id}/media"
        headers = {"Authorization": f"Bearer {self.token}"}

        form_data = FormData()
        form_data.add_field("file", audio_bytes, filename='audio', content_type="audio/mpeg")
        form_data.add_field("type", "audio/mpeg")
        form_data.add_field("messaging_product", "whatsapp")

        async with ClientSession() as session:
            async with session.post(url, headers=headers, data=form_data) as resp:
                resp_json = await resp.json()
                if resp.status != 200:
                    raise Exception(f"Erro ao enviar mídia: {resp.status} - {resp_json}")
                return resp_json.get("id")
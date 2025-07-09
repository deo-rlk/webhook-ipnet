import os
import subprocess
from datetime import datetime
import tempfile

class AudioUtils:
    @staticmethod
    def convert_whatsapp_audio_to_dialogflow(audio_bytes: bytes, sample_rate: int = 48000) -> bytes:
        """
        Salva o áudio recebido do WhatsApp (OGG/OPUS) em disco, converte para o formato
        que o Dialogflow espera e retorna os bytes prontos para envio.
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        input_path = f"temp/whatsapp_audio_{timestamp}.ogg"
        output_path = input_path.replace(".ogg", "_converted.ogg")

        os.makedirs("temp", exist_ok=True)

        with open(input_path, "wb") as f:
            f.write(audio_bytes)

        subprocess.run(
            ["ffmpeg", "-i", input_path, "-c:a", "libopus", "-ar", str(sample_rate), output_path],
            check=True
        )

        with open(output_path, "rb") as f:
            converted_bytes = f.read()

        return converted_bytes
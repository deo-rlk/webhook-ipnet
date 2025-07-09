from google.cloud.dialogflowcx_v3 import SessionsClient, InputAudioConfig, AudioEncoding, DetectIntentRequest
from google.cloud.dialogflowcx_v3.types.session import AudioInput, TextInput, QueryInput
from app.utils.session_manager import SessionManager
from app.services.tts_service import TextToSpeechService 


class DialogflowService:
    def __init__(self, project_id: str, location: str, agent_id: str, session_manager: SessionManager, tts_service: TextToSpeechService):
        self.project_id = project_id
        self.location = location
        self.agent_id = agent_id
        self.session_client = SessionsClient()
        self.session_manager = session_manager
        self.tts_service = tts_service 

    def __get_session_path(self, session_id: str) -> str:
        return f"projects/{self.project_id}/locations/{self.location}/agents/{self.agent_id}/sessions/{session_id}"


    async def detect_intent_text(self, sender_id: str, user_input: str) -> str:

        session_id = self.session_manager.get_session_id(sender_id)
        session_path = self.__get_session_path(session_id)

        query_input = QueryInput(
            text=TextInput(text=user_input),
            language_code="pt-BR"
        )

        request = DetectIntentRequest(
            session=session_path,
            query_input=query_input,
        )
        
        response = self.session_client.detect_intent(request=request)

        answer = response.query_result.response_messages[0].text.text[0]

        return answer


    async def detect_intent_audio(self, sender_id: str, audio_content: bytes, sample_rate: int = 48000) -> bytes:
        session_id = self.session_manager.get_session_id(sender_id)
        session_path = self.__get_session_path(session_id)

        query_input = QueryInput(
            audio=AudioInput(
                config=InputAudioConfig(
                    audio_encoding=AudioEncoding.AUDIO_ENCODING_OGG_OPUS,
                    sample_rate_hertz=sample_rate,
                ),
                audio=audio_content,
            ),
            language_code="pt-BR"
        )

        request = DetectIntentRequest(
            session=session_path,
            query_input=query_input,
        )

        response = self.session_client.detect_intent(request=request)

        text_response = response.query_result.response_messages[0].text.text[0]

        audio_bytes = self.tts_service.synthesize_speech(text_response)

        return audio_bytes
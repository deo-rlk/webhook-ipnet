from google.cloud.texttospeech import TextToSpeechClient, SynthesisInput, VoiceSelectionParams, AudioConfig, AudioEncoding, SsmlVoiceGender

class TextToSpeechService():
    def __init__(self):
        self.client = TextToSpeechClient()

    def synthesize_speech(self, text: str) -> bytes:

        synthesis_input = SynthesisInput(text=text)
        
        voice = VoiceSelectionParams(
            language_code="pt-BR", 
            name="pt-BR-Wavenet-D", 
            ssml_gender=SsmlVoiceGender.FEMALE
        )

        audio_config = AudioConfig(audio_encoding=AudioEncoding.MP3)

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content
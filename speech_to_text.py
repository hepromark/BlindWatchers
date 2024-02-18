import io

from google.oauth2 import service_account
from google.cloud import speech


class SpeechToText():
    CLIENT_FILE = 'sa_speech.json'
    CREDENTIALS = service_account.Credentials.from_service_account_file(CLIENT_FILE)

    def __init__(self) -> None:
        self.client = speech.SpeechClient(credentials=self.CREDENTIALS)
    
    def convert_to_text(self, audio_file):
        # Load audio file
        with io.open(audio_file, 'rb') as f:
            content = f.read()
            audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=44100,
            language_code='en-US'
        )

        response = self.client.recognize(config=config, audio=audio)

        text = response.results[0].alternatives[0].transcript

        return text

if __name__ == "__main__":
    s = SpeechToText()
    print(s.convert_to_text("chairtables.mp3"))




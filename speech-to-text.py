import io
import soundfile as sf
import pyaudio

from google.oauth2 import service_account
from google.cloud import speech


class SpeechToText():
    CLIENT_FILE = 'sa_speech.json'
    CREDENTIALS = service_account.Credentials.from_service_account_file(CLIENT_FILE)

    def __init__(self) -> None:
        self.client = speech.SpeechClient(credentials=self.CREDENTIALS)
    
    def record(self, file_path, sample_rate):
        p = pyaudio.PyAudio()
        
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=1024)
        
        print("Recording...")
        
        frames = []
        for i in range(0, int(sample_rate / 1024 * 5)):
            data = stream.read(1024)
            frames.append(data)

        print("Recording complete.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio as a WAV file
        with sf.SoundFile(file_path, 'w', samplerate=sample_rate, channels=1) as f:
            f.write(frames)

        print(f"Audio saved as: {file_path}.wav")


    def _convert_to_text(self, audio_file):
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

        print(response)



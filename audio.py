from gtts import gTTS 
import os
from io import BytesIO
from openal import oalOpen, oalQuit, oalGetListener, Listener
from openal.al import alSource3f, AL_POSITION, AL_PLAYING, AL_GAIN
import time
import wave
import numpy as np

from pydub import AudioSegment


class Audio:
    def __init__(self, pitch=1.0, voice="ca", slow=False):
        self.position = [0,0,0]
        self.pitch = pitch
        self.voice = voice
        self.slow = slow
        self.text = ""
    
    def __deinit__(self):
        os.remove("tmp.wav")
        os.remove("tmp.mp3")
        
    def __play_spatial_audio(self, file_path):
        # Load the .wav file
        source = oalOpen(file_path)

        # Set the position of the source
        source.set_pitch(self.pitch)
        source.set_rolloff_factor(0.9)
        source.set_max_distance(10.0)
        # Play the source
        source.play()

        while source.get_state() == AL_PLAYING:
            source.set_position(self.position)
        #close the source
        oalQuit()

    def __convert_mp3_to_wav(self, mp3_path, wav_path):
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")
   
   
    def __text_to_speech(self, position, text):
        self.position = position
        self.text = text
        if(text == ""):
            return
        # Passing the text and language to the engine
        tts = gTTS(text=self.text, tld=self.voice, slow=self.slow) 

        # Saving the converted audio in a wav file named sample
        tts.save('tmp.mp3')
        
        # convert to wav so that openal can play it
        self.__convert_mp3_to_wav('tmp.mp3', 'tmp.wav') 
        self.__play_spatial_audio("tmp.wav")
         
    def run(self, arr):
        self.__text_to_speech(arr[1], arr[0])
    
# if __name__ == "__main__":
#     audio = Audio(voice="co.uk", slow=False)
#     audio.text_to_speech([-50, 0.0, -0.5], "Hello, this is a spatial audio test.") # usage

    
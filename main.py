from data_synthesis import Synthesis
from camera_driver import CameraDriver
from speech_to_text import SpeechToText
from audio import Audio
import RPi.GPIO as GPIO
import time
import wave
import struct
import pyaudio
import soundfile as sf
from pvrecorder import PvRecorder

for index, device in enumerate(PvRecorder.get_available_devices()):
    print(f"[{index}] {device}")
EXIT_PIN = 12
VOICE_INPUT_PIN = 16
SAMPLE_RATE = 48000

print("INITIALIZE")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(EXIT_PIN, GPIO.IN)
GPIO.setup(VOICE_INPUT_PIN, GPIO.IN)

def record():
    file_path = "/audio/command.wav"
    p = pyaudio.PyAudio()
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=SAMPLE_RATE,
                    input=True,
                    frames_per_buffer=1024)
    
    print("Recording...")
    
    frames = []
    try:
        while GPIO.input(VOICE_INPUT_PIN) == GPIO.HIGH:
            data = stream.read(1024)
            frames.append(data)
    except:
        pass

    print("Recording complete.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio as a WAV file
    with sf.SoundFile(file_path, 'w', samplerate=SAMPLE_RATE, channels=1) as f:
        f.write(frames)

    print(f"Audio saved as: {file_path}")


def waitState():
    print("Entering Wait State")
    while GPIO.input(VOICE_INPUT_PIN) == GPIO.LOW:
        time.sleep(.01)
    record()
    print("Exiting Wait")
    converter = SpeechToText()
    function, filter = converter.take_voice_command()

    if function == 1:
        whatState()
    else:
        whereState(filter)

def whereState(filter):
    print("Entering Where")
    cam = CameraDriver(0,1)
    left_detection, right_detection = cam.detect()
    syn = Synthesis(left_detection, right_detection, filter=filter)
    output = syn.output()

    audio = Audio()
    audio.run(output)


def whatState():
    print("Entering What")
    cam = CameraDriver(0,1)
    left_detection, right_detection = cam.detect()
    syn = Synthesis(left_detection, right_detection)
    output = syn.output()

    audio = Audio()
    audio.run(output)

if __name__ == "__main__":
    print("Entering Main")
    while GPIO.input(EXIT_PIN) == GPIO.LOW:
        waitState()
    
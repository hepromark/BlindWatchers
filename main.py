from data_synthesis import Synthesis
from camera_driver import CameraDriver
from speech_to_text import SpeechToText
from audio import Audio
import RPi.GPIO as GPIO
import time
import wave
import struct
import pyaudio
import os
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
    file_path = "command.wav"
    recorder = PvRecorder(device_index=2, frame_length=512)
    # p = pyaudio.PyAudio()
    
    # stream = p.open(format=pyaudio.paInt16,
    #                 channels=1,
    #                 rate=SAMPLE_RATE,
    #                 input=True,
    #                 frames_per_buffer=1024)
    
    print("Recording...")
    
    frames = []
    audio = []
    now = time.time()
    print(now)
    try:
        recorder.start()

        while now + 5 > time.time():
            frame = recorder.read()
            audio.extend(frame)
        # Do something ...
    except KeyboardInterrupt:
        recorder.stop()
    finally:
        recorder.delete()
    # while GPIO.input(VOICE_INPUT_PIN) == GPIO.HIGH:
    #     data = stream.read(1024)
    #     frames.append(data)

    print("Recording complete.")
    # Stop and close the stream
    # stream.stop_stream()
    # stream.close()
    # p.terminate()
    # Save the recorded audio as a WAV file
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with wave.open(file_path, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))

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
    elif function == -1:
        waitState()
    else:
        whereState(filter)

def whereState(filter):
    print("Entering Where")
    cam = CameraDriver(0,1)
    left_detection, right_detection = cam.detect()
    syn = Synthesis(left_detection, right_detection, filter=filter)
    output = syn.output()
    print("output:")
    print(output)
    audio = Audio()
    audio.run(output)


def whatState():
    print("Entering What")
    cam = CameraDriver(0,1)
    left_detection, right_detection = cam.detect()
    syn = Synthesis(left_detection, right_detection)
    output = syn.output()
    print("output:")
    print(output)
    audio = Audio()
    audio.run(output)

if __name__ == "__main__":
    print("Entering Main")
    while GPIO.input(EXIT_PIN) == GPIO.LOW:
        waitState()
    
import RPi.GPIO as GPIO
import time

RESET_STATE_PIN = 18
VOICE_INPUT_PIN = 23

GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(voice, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def waitPin(pin):
    while GPIO.input(pin) == GPIO.LOW:
        time.sleep(0.01)
    GPIO.setmode(GPIO.BCM)

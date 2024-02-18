import io

from google.oauth2 import service_account
from google.cloud import speech

class SpeechToText():
    CLIENT_FILE = 'sa_speech.json'
    CREDENTIALS = service_account.Credentials.from_service_account_file(CLIENT_FILE)

    def __init__(self) -> None:
        self.objects_plural_to_singular = {
        "persons": "person", "bicycles": "bicycle", "cars": "car", "motorcycles": "motorcycle",
        "airplanes": "airplane", "buses": "bus", "trains": "train", "trucks": "truck",
        "boats": "boat", "traffic lights": "traffic light", "fire hydrants": "fire hydrant",
        "stop signs": "stop sign", "parking meters": "parking meter", "benches": "bench",
        "birds": "bird", "cats": "cat", "dogs": "dog", "horses": "horse",
        "sheep": "sheep", "cows": "cow", "elephants": "elephant", "bears": "bear",
        "zebras": "zebra", "giraffes": "giraffe", "backpacks": "backpack", "umbrellas": "umbrella",
        "handbags": "handbag", "ties": "tie", "suitcases": "suitcase", "frisbees": "frisbee",
        "skis": "ski", "snowboards": "snowboard", "sports balls": "sports ball", "kites": "kite",
        "baseball bats": "baseball bat", "baseball gloves": "baseball glove", "skateboards": "skateboard",
        "surfboards": "surfboard", "tennis rackets": "tennis racket", "bottles": "bottle",
        "wine glasses": "wine glass", "cups": "cup", "forks": "fork", "knives": "knife",
        "spoons": "spoon", "bowls": "bowl", "bananas": "banana", "apples": "apple",
        "sandwiches": "sandwich", "oranges": "orange", "broccolis": "broccoli", "carrots": "carrot",
        "hot dogs": "hot dog", "pizzas": "pizza", "donuts": "donut", "cakes": "cake",
        "chairs": "chair", "couches": "couch", "potted plants": "potted plant", "beds": "bed",
        "tables": "table", "toilets": "toilet", "tvs": "tv", "laptops": "laptop",
        "mice": "mouse", "remotes": "remote", "keyboards": "keyboard", "cell phones": "cell phone",
        "microwaves": "microwave", "ovens": "oven", "toasters": "toaster", "sinks": "sink",
        "refrigerators": "refrigerator", "books": "book", "clocks": "clock", "vases": "vase",
        "scissors": "scissor", "teddy bears": "teddy bear", "hair driers": "hair drier",
        "toothbrushes": "toothbrush"}

        self.STATE_1_COMMAND = ["what is around", "what's around"]

        self.client = speech.SpeechClient(credentials=self.CREDENTIALS)
        self.audio_file = "command.wav"
        # self.audio_file = "whatsaround.mp3"
    
    def take_voice_command(self):
        text = self.__convert_to_text__()
        print(text)

        if not text:
            return [-1, []]

        # State 1
        if text in self.STATE_1_COMMAND:
            return [1, []]
        
        # State 2
        positive_filter = []
        for word in text.split():
            if word in self.objects_plural_to_singular.keys() or word in self.objects_plural_to_singular.values():
                positive_filter.append(word)
        
        return [2, positive_filter]
    
    def __convert_to_text__(self):
        # Load audio file
        with io.open(self.audio_file, 'rb') as f:
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
    print(s.take_voice_command())




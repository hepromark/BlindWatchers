import cv2
import numpy as np
from ultralytics import YOLO

import matplotlib.pyplot as plt

class CameraDriver():
    CONFIDENCE = 0.5
    def __init__(self, cam_port_1, cam_port_2) -> None:
        self.model = YOLO('yolov8s.pt')
        self.YOLO_LABELS = {"0": "person", "1": "bicycle", "2": "car", "3": "motorcycle", "4": "airplane", "5": "bus", "6": "train", "7": "truck", "8": "boat", "9": "traffic light", "10": "fire hydrant", "11": "stop sign", "12": "parking meter", "13": "bench", "14": "bird", "15": "cat", "16": "dog", "17": "horse", "18": "sheep", "19": "cow", "20": "elephant", "21": "bear", "22": "zebra", "23": "giraffe", "24": "backpack", "25": "umbrella", "26": "handbag", "27": "tie", "28": "suitcase", "29": "frisbee", "30": "skis", "31": "snowboard", "32": "sports ball", "33": "kite", "34": "baseball bat", "35": "baseball glove", "36": "skateboard", "37": "surfboard", "38": "tennis racket", "39": "bottle", "40": "wine glass", "41": "cup", "42": "fork", "43": "knife", "44": "spoon", "45": "bowl", "46": "banana", "47": "apple", "48": "sandwich", "49": "orange", "50": "broccoli", "51": "carrot", "52": "hot dog", "53": "pizza", "54": "donut", "55": "cake", "56": "chair", "57": "couch", "58": "potted plant", "59": "bed", "60": "dining table", "61": "toilet", "62": "tv", "63": "laptop", "64": "mouse", "65": "remote", "66": "keyboard", "67": "cell phone", "68": "microwave", "69": "oven", "70": "toaster", "71": "sink", "72": "refrigerator", "73": "book", "74": "clock", "75": "vase", "76": "scissors", "77": "teddy bear", "78": "hair drier", "79": "toothbrush"}

        self.cam_1 = 0
        self.cam_2 = 0

        # If camera isn't used
        if cam_port_1 != "null":
            self.cam_1 = cv2.VideoCapture(cam_port_1)
        if cam_port_2 != "null":
            self.cam_2 = cv2.VideoCapture(cam_port_2)
    
    def detect(self):
        frame1, frame2 = self._get_frame()
        return self._process_frame([frame1, frame2])

    def test(self):
        frame1, frame2 = self._get_frame()
        print("===========================================")
        detections = self._process_frame([frame1, frame2])
        print(detections)

    def _process_frame(self, frames):
        print("Processing frame....")
        print()
        output = [[], []]

        for i, frame in enumerate(frames):
            result = self.model(frame)

            # Loop through each bounding box in an image
            if not len(result):
                print("No bounding box seen :(")
            else:
                res_1 = result[0]
                for k, detection in enumerate(res_1.boxes):

                    # Confidence thresholding
                    if detection.conf < self.CONFIDENCE:
                        continue

                    xywh = detection.xywh.tolist()[0]
                    pred_class = self.YOLO_LABELS[f'{int(detection.cls.item())}']
                    print(f'Processing detection {k}: {pred_class}')

                    # print(f'xywh: {xywh}')
                    # print(f'Class: {pred_class}')

                    # Aggregate to output
                    output[i].append(xywh + [pred_class])

                plt.imshow(res_1.plot())
                plt.imsave(f'img{i}.jpg', res_1.plot())
                plt.show()

        return output
    
    def _get_frame(self):
        frame1 = 0
        frame2 = 0

        if self.cam_1:
            ret1, frame1 = self.cam_1.read()

        if self.cam_2:
            ret2, frame2 = self.cam_2.read()

        return frame1, frame2
    
if __name__ == "__main__":
    c = CameraDriver(0, 1)
    c.test()
from data_synthesis import Synthesis
from camera_driver import CameraDriver

class BlindWatchers:
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    cam = CameraDriver(0, 1)
    left_detection, right_detection = cam.detect()

    syn = Synthesis(left_detection, right_detection, ["person"])
    output = syn.output()
    print(len(output))
    print(output)
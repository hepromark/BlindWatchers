import math
from collections import defaultdict 

class Synthesis:
    def __init__(self, left_obj, right_obj, filter = None, negFilter = None):
        #objects in the form of [[x, y, w, h, class name]] x, y (0,0) being top left
        self.width = 640
        self.height = 480
        self.radius = 30
        self.iou = .9
        self.edgeTolerance = 30
        self.ANGLE = 110

        self.left, self.right = self.filter(filter, negFilter, left_obj, right_obj)

    def filter(self, filter, negFilter, left_obj, right_obj):
        if negFilter != None:
            for count in range(len(left_obj) - 1, 0, -1):
                if left_obj[count][4] in negFilter:
                    left_obj.pop(count)

            for count in range(len(right_obj) - 1, 0, -1):
                if right_obj[count][4] in negFilter:
                    right_obj.pop(count)
        
        if filter != None:
            for count in range(len(left_obj) - 1, 0, -1):
                if left_obj[count][4] not in filter:
                    left_obj.pop(count)

            for count in range(len(right_obj) - 1, 0, -1):
                if right_obj[count][4] not in filter:
                    right_obj.pop(count)
        return left_obj, right_obj

    def removeIntersection(self):
        left = self.left
        right = self.right
        leftEdge = []
        rightEdge = []

        for count in range(len(left) - 1, 0, -1):
            if left[count][0] + left[count][2] - self.width > -self.edgeTolerance:
                leftEdge.append(count)

        for count in range(len(right) - 1, 0, -1):
            if right[count][0] + right[count][2] - self.width > -self.edgeTolerance:
                rightEdge.append(count)

        removeRight = []
        removeLeft = []
        for l in range(len(leftEdge) - 1):
            for r in range(len(rightEdge) - 1):
                intersection = min(left[l][1], right[r][1]) - max(left[l][1]-left[l][3], right[l][1]-right[l][3])
                
                union = max(left[l][1], right[r][1]) - min(left[l][1]-left[l][3], right[l][1]-right[l][3])
                if intersection / union < self.iou and intersection / union > 0:
                    if l not in removeLeft:
                        removeLeft.append(l)
                    elif r not in removeRight:
                        removeRight.append(r)

        removeLeft = sorted(removeLeft)
        removeRight = sorted(removeRight)

        for item in removeRight:
            right.pop(item)

        self.left = left
        self.right = right


    def getSpacial(self, x, y, w, h, isRight):
        x = x + w // 2
        if not isRight:
            x = x - self.width
        
        angleFromCenter = x / self.width * self.ANGLE
        
        newX = int(self.radius * math.sin(90 - angleFromCenter))
        newY = int(self.radius * math.cos(90 - angleFromCenter))

        return angleFromCenter, [newX, newY, 0]
    
    def getSentence(self, angle, isRight, className):
        #removing negative angle
        angle = angle if isRight else -1 * angle 
        angle = int(round(angle))
        direction = "right" if isRight else "left"
        if angle != 0:
            return "A " + className + " is " + str(angle) + " degrees to the " + direction 
        else:
            return "A " + className + " is straight ahead"

    def transform(self, isRight : bool, view):
        output = []
        for object in view:
            angle, quards = self.getSpacial(object[0], object[1], object[2], object[3], isRight)

            sentence = self.getSentence(angle, isRight, object[4])

            output.append([sentence, quards])
        return output

    def setRadius(self, radius):
        self.radius = radius

    def getSummary(self, leftView, rightView):
        summary_sentence = ""
        object_freq = {}

        for object in leftView:
            if object[4] not in object_freq.keys():
                object_freq[object[4]] = 1
            else:
                object_freq[object[4]] += 1

        for object in rightView:
            if object[4] not in object_freq.keys():
                object_freq[object[4]] = 1
            else:
                object_freq[object[4]] += 1

        # Process summary sentence
        if len(object_freq.keys()):
            summary_sentence = "There are"
        for key, value in object_freq.items():
            summary_sentence += f' {value} {key}s'
        
        return [summary_sentence, [0, 0, 0]]

    def output(self):
        self.removeIntersection()
        summary = self.getSummary(self.left, self.right)
        left = self.transform(isRight=False, view = self.left)
        right = self.transform(isRight = True, view = self.right)
        return summary + left + right
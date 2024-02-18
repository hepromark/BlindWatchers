import math

class Synthesis:
    def __init__(self, left_obj, right_obj, filter = None, negFilter = None):
        #objects in the form of [[x, y, w, h, class name]] x, y (0,0) being top left
        self.width = 640
        self.height = 480
        self.radius = 30
        self.intersection = .9
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
        leftEdge = []
        rightEdge = []
        for r in range(len(self.left) -1):
            for l in range()

    def getSpacial(self, x, y, w, h, isRight):
        x = x + w // 2
        y = y - h // 2
        if not isRight:
            x = x - self.width
        
        angle = x / self.width * self.ANGLE
        
        x = int(self.radius * math.sin(angle))
        y = int(self.radius * math.cos(angle))

        return angle, [x, y, 0]
    
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
        #output [[string, 3d pos]]
        output = []
        direction = "right" if isRight else "left"
        for object in view:
            angle, quards = self.getSpacial(object[0], object[1], object[2], object[3], isRight)

            sentence = self.getSentence(angle, isRight, object[4])

            output.append([sentence, quards])
        return output

    def setRadius(self, radius):
        self.radius = radius

    def output(self):
        #self.removeIntersection()
        left = self.transform(isRight=False, view = self.left)
        right = self.transform(isRight = True, view = self.right)
        return left + right
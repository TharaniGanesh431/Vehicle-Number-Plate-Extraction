import cv2
import math

class contourProperty:

    def __init__(self, _contour):
        self.contour = _contour

        self.Rectangle = cv2.boundingRect(self.contour)
        [self.X, self.Y, self.Width, self.Height] = self.Rectangle
   
        self.Area = self.Width * self.Height

        self.CenterX = (self.X + self.X + self.Width) / 2
        self.CenterY = (self.Y + self.Y + self.Height) / 2

        self.diagonalSize = math.sqrt((self.Width ** 2) + (self.Height ** 2))

        self.aspectRatio = float(self.Width) / float(self.Height)

class Plates:
    def __init__(self):
        self.Plate = None
        self.Gray = None
        self.Thresh = None

        self.Location= None

        self.Chars = ""

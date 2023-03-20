import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gameMapImage import gameMapImage
import imutils

# Takes a cv2 image and returns a cv2 image
# finds the corners of the map from the full image
# Returns a cropped image of only the map


class userMapImage:
    def __init__(self, cv2Image, ratio: str = "") -> None:
        self.__image = gameMapImage(cv2Image, ratio)
        self.__ratio = self.__image.ratio()
        self.__thresheldImage = None
        self.__targets = None

        __slots__ = ["__image", "__ratio", "run", "getThresheldImage", "findRedDots", "__thresheldImage"]

    def run(self) -> gameMapImage:
        if self.__ratio == "":
            self.ratio = self.__detectAspectRatio()
        cropSize = self.__returnCropSize(self.__image().shape, self.ratio)
        croppedImage = self.__cropImage(self.__image(), cropSize)
        changedImage = self.__changeImageAspectRatio(croppedImage)
        self.__thresheldImage = self.getThresheldImage()
        return gameMapImage(changedImage, self.ratio)
    # Takes a cv2 image and returns a cv2 image
    # change to a 1:1 aspect ratio
    # change to 800x800

    def getThresheldImage(self) -> gameMapImage:
        return gameMapImage.thresholdImage(self.__image)

    def findRedDots(self) -> list:
        # find the red dots
        image = gameMapImage(cv.cvtColor(self.__image(), cv.COLOR_BGR2GRAY), self.__image.ratio())
        image = gameMapImage(cv.GaussianBlur(image(), (5, 5), 0), image.ratio())
        cnts = cv.findContours(image(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        circles = []
        for c in cnts:
            # compute the center of the contour
            M = cv.moments(c)
            if M["m00"] != 0:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
                # draw the contour and center of the shape on the image
                #cv.drawContours(image(), [c], -1, (0, 255, 0), 2)
                minshape = cv.minEnclosingCircle(c)
                circles.append(minshape)
        # Filtered the circles
        toDraw = self.__filterCirlces(circles)
        print(len(toDraw))
        returnPoints = []
        for circle in toDraw:
            # draw the circle on the image
            cv.circle(image(), (int(circle[0][0]), int(circle[0][1])), int(circle[1]), (255, 255, 255), 2)
            # Remove the radius value, we don't need it after filtering
            returnPoints.append((int(circle[0][0]), int(circle[0][1])))
        i = 0
        for i in range(len(returnPoints)):
            # Scale the points to the size of the map
            returnPoints[i] = (int(returnPoints[i][0]*(4096/800)), int(returnPoints[i][1]*(4096/800)))
        self.__targets = returnPoints
        return returnPoints

    def __filterCirlces(self, circles: list[tuple[tuple[int, int], int]]) -> list[tuple[tuple[int, int], int]]:
        toDraw = []
        toRemove = []
        for circle in circles:
            for circle2 in circles:
                if circle != circle2:
                    if circle2[1] > 15:
                        continue
                    distance = math.sqrt((circle[0][0]-circle2[0][0])**2+(circle[0][1]-circle2[0][1])**2)
                    if (distance < (circle[1]+circle2[1]+(circle[1]+circle2[1])*0.5)):
                        newCircle = ((circle[0][0]+circle2[0][0])/2, (circle[0]
                                                                      [1]+circle2[0][1])/2), (circle[1]+circle2[1]+(circle[1]+circle2[1])*0.5)
                        if newCircle not in toDraw:
                            toDraw.append(newCircle)
                        toRemove.append(circle)
                        toRemove.append(circle2)
                        break
                    else:
                        if circle not in toDraw:
                            toDraw.append(circle)
        for circle in toRemove:
            toDraw = self.__remove(toDraw, circle)
        return toDraw

    def __remove(self, the_list: list, val) -> list:
        return [value for value in the_list if value != val]

    def __detectAspectRatio(self) -> str:
        height, width, channels = self.__image.shape()
        if height * 4 == width * 3:
            return "4:3"
        if height * 16 == width * 10:
            return "16:10"
        if height * 16 == width * 9:
            return "16:9"
        raise ValueError("Invalid aspect ratio", height, width)

    def __cropImage(self, image: np.ndarray, cropSize: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]) -> np.ndarray:
        topLeft, topRight, bottomLeft, bottomRight = cropSize
        croppedImage = image[topLeft[1]:bottomLeft[1], topLeft[0]:topRight[0]]
        return croppedImage

    def __returnCropSize(self, imageShape: tuple[int, int, int], ratio: str) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        height, width, channels = imageShape
        # The dictionary is in the format {aspectRatio: (leftMarginRatio, righMarginRatip, bottomMarginRatio)}
        if "by" in ratio:
            ratio = ratio.replace("by", ":")
        scalarDict = {"4:3": (192/1920, 283/1920, 62/1080), "16:10": (315/1680, 379 /
                                                                      1680, 62/1050), "16:9": (420/1920, 485/1920, 64/1080)}
        if ratio not in scalarDict:
            raise ValueError("Invalid aspect ratio", ratio)
        leftWidthRatio, rightWidthRatio, bottomHeightRatio = scalarDict[ratio]
        rightWidth = int(width * rightWidthRatio)
        leftWidth = int(width * leftWidthRatio)
        bottomHeight = int(height * bottomHeightRatio)
        topLeft = (leftWidth, 0)
        topRight = (width - rightWidth, 0)
        bottomLeft = (leftWidth, height - bottomHeight)
        bottomRight = (width - rightWidth, height - bottomHeight)
        return (topLeft, topRight, bottomLeft, bottomRight)

    def __changeImageAspectRatio(self, image: np.ndarray) -> np.ndarray:
        image = cv.resize(image, (image.shape[0], image.shape[0]), interpolation=cv.INTER_AREA)
        image = cv.resize(image, (800, 800), interpolation=cv.INTER_AREA)
        return image

# Path: gameMapImage.py

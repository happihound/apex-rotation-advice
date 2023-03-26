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
    __slots__ = [
        "__thresheldImage", "__targets", "__imageOriginalImage", "__croppedImage"]

    def __init__(self, cv2Image: np.ndarray, ratio: str = "") -> None:
        self.__imageOriginalImage = gameMapImage(cv2Image, ratio)
        # If the aspect ratio is not set, detect it from the image
        if ratio not in self.getValidRatios() and ratio != "":
            raise ValueError(
                f"Invalid aspect ratio. Valid ratios are {self.getValidRatios()}")
        if self.__imageOriginalImage.ratio() == "":
            self.__imageOriginalImage = gameMapImage(self.__imageOriginalImage(), self.__detectAspectRatio())
        # Determine the crop size by the aspect ratio
        cropSize = self.__returnCropSize(self.__imageOriginalImage.shape(), self.__imageOriginalImage.ratio())

        # Change the image aspect ratio
        self.__croppedImage = gameMapImage(self.__changeImageAspectRatio(
            self.__cropImage(self.__imageOriginalImage(), cropSize)), "1:1")

        # Get the thresheld image
        self.__thresheldImage = gameMapImage(self.__makeThresholdImage(), "1:1")

        # Find the red dots
        self.__targets = self.__findRedDots()

    def getThresheldImage(self) -> gameMapImage:
        if self.__thresheldImage is None:
            self.__thresheldImage = gameMapImage(self.__makeThresholdImage(), "1:1")
        return self.__thresheldImage

    def getOriginalImage(self) -> gameMapImage:
        return self.__imageOriginalImage

    def getCroppedImage(self) -> gameMapImage:
        return self.__croppedImage

    def getValidRatios(self) -> list[str]:
        return ["1:1", "4:3", "16:9", "16:10", "1by1", "4by3", "16by9", "16by10"]

    def getTargets(self) -> list:
        return self.__targets

    def __findRedDots(self) -> list:
        # find the red dots
        image = gameMapImage(cv.cvtColor(self.__thresheldImage(), cv.COLOR_BGR2GRAY), self.__thresheldImage.ratio())
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
                # cv.drawContours(image(), [c], -1, (0, 255, 0), 2)
                minshape = cv.minEnclosingCircle(c)
                circles.append(minshape)
        # Filtered the circles
        toDraw = self.__filterCirlces(circles)
        returnPoints = []
        for circle in toDraw:
            # draw the circle on the image
            # cv.circle(self.__targetImage(), (int(circle[0][0]), int(circle[0][1])), int(circle[1]), (255, 255, 255), 2)
            # Remove the radius value, we don't need it after filtering
            returnPoints.append((int(circle[0][0]), int(circle[0][1])))
        i = 0
        for i in range(len(returnPoints)):
            # Scale the points to the size of the map
            returnPoints[i] = (int(returnPoints[i][0]*(4096/800)), int(returnPoints[i][1]*(4096/800)))
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

    def __makeThresholdImage(self) -> np.ndarray:
        # convert to hsv
        hsv = cv.cvtColor(self.__croppedImage(), cv.COLOR_BGR2HSV)

        # define range of red color in hsv
        # some of the colors wrap around the hue value, so we have to define two ranges
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])

        # threshold the hsv image to get only red colors
        mask = cv.inRange(hsv, lower_red, upper_red)

        mask2 = cv.inRange(hsv, lower_red2, upper_red2)

        # bitwise and mask and original image
        res = cv.bitwise_and(self.__croppedImage(), self.__croppedImage(), mask=mask)

        res2 = cv.bitwise_and(self.__croppedImage(), self.__croppedImage(), mask=mask2)

        res = cv.bitwise_or(res, res2)
        # erode to remove noise
        res = cv.erode(res, None, iterations=1)
        # dilate to fill in gaps
        res = cv.dilate(res, None, iterations=1)

        return res

    def __remove(self, the_list: list, val) -> list:
        return [value for value in the_list if value != val]

    def __detectAspectRatio(self) -> str:
        height, width, channels = self.__imageOriginalImage.shape()
        if height * 4 == width * 3:
            return "4:3"
        if height * 16 == width * 10:
            return "16:10"
        if height * 16 == width * 9:
            return "16:9"
        raise ValueError("Invalid aspect ratio", height, width)

    def __cropImage(self, image: np.ndarray, cropSize: tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]) -> np.ndarray:
        # Extract the four corners of the cropping rectangle
        topLeft, topRight, bottomLeft, bottomRight = cropSize
        # Crop the image
        croppedImage = image[topLeft[1]: bottomLeft[1], topLeft[0]: topRight[0]]
        return croppedImage

    def __returnCropSize(self, imageShape: tuple[int, int, int], ratio: str) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        # The image shape is a tuple with height, width, and channels
        height, width, channels = imageShape
        # The dictionary is in the format {aspectRatio: (leftMarginRatio, righMarginRatip, bottomMarginRatio)}
        # The aspect ratio is defined as the width divided by the height
        # The ratios are defined as the ratio of the margin width or height to the width or height of the image
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
        # resize image to desired height
        image = cv.resize(image, (image.shape[0], image.shape[0]), interpolation=cv.INTER_AREA)
        # resize image to desired width
        image = cv.resize(image, (800, 800), interpolation=cv.INTER_AREA)
        return image

    def __call__(self) -> gameMapImage:
        return self.__imageOriginalImage

# Path: gameMapImage.py

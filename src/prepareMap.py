import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from gameMapImage import gameMapImage
# Takes a cv2 image and returns a cv2 image
# finds the corners of the map from the full image
# Returns a cropped image of only the map


class prepareMap:
    def __init__(self, image):
        self.image = image.image()
        self.ratio = image.ratio()

        __slots__ = ["image", "ratio", "run"]

    def run(self) -> gameMapImage:
        if self.ratio == "":
            self.ratio = self.__detectAspectRatio(self.image.shape)
        cropSize = self.__returnCropSize(self.image.shape, self.ratio)
        croppedImage = self.__cropImage(self.image, cropSize)
        changedImage = self.__changeImageAspectRatio(croppedImage)

        return gameMapImage(changedImage, self.ratio)
    # Takes a cv2 image and returns a cv2 image
    # change to a 1:1 aspect ratio
    # change to 800x800

    def __detectAspectRatio(self, imageShape: tuple[int, int, int]) -> str:
        height, width, channels = imageShape
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

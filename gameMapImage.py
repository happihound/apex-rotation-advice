import cv2 as cv
import numpy as np


class gameMapImage:
    def __init__(self, image: np.ndarray, ratio: str = "") -> None:
        self.__image = image
        self.__ratio = ratio

    __slots__ = ["__image", "__ratio"]

    def ratio(self) -> str:
        return self.__ratio

    def ratioNumber(self) -> float:
        if "by" in self.__ratio:
            ratio = self.__ratio.split("by")
        else:
            ratio = self.__ratio.split(":")
        return float(ratio[0]) / float(ratio[1])

    def image(self) -> np.ndarray:
        return self.__image

    def copy(self) -> "gameMapImage":
        return gameMapImage(self.__image, self.__ratio)

    def thresholdImage(self) -> "gameMapImage":
        # convert to hsv
        hsv = cv.cvtColor(self.__image, cv.COLOR_BGR2HSV)

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
        res = cv.bitwise_and(self.__image, self.__image, mask=mask)

        res2 = cv.bitwise_and(self.__image, self.__image, mask=mask2)

        res = cv.bitwise_or(res, res2)
        # erode to remove noise
        res = cv.erode(res, None, iterations=1)
        # dilate to fill in gaps
        res = cv.dilate(res, None, iterations=1)

        return gameMapImage(res, self.__ratio)

    def shape(self) -> tuple:
        return self.__image.shape[:2]

    def __call__(self, *args, **kwargs) -> np.ndarray:
        return self.__image

# Path: prepareMap.py

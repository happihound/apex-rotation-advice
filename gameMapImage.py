import cv2 as cv
import numpy as np


class gameMapImage:
    __slots__ = ["__image", "__ratio"]

    def __init__(self, image: np.ndarray, ratio: str = "") -> None:
        self.__image = image
        self.__ratio = ratio

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

    def shape(self) -> tuple:
        return self.__image.shape

    def __call__(self, *args, **kwargs) -> np.ndarray:
        return self.__image

# Path: prepareMap.py

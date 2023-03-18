import cv2 as cv
import numpy as np


class gameMapImage:
    def __init__(self, image: np.ndarray, ratio: str = "") -> None:
        self.__image = image
        self.__ratio = ratio

    __slots__ = ["__image", "__ratio"]

    def ratio(self) -> str:
        return self.__ratio

    def image(self) -> np.ndarray:
        return self.__image

    def copy(self) -> "gameMapImage":
        return gameMapImage(self.__image, self.__ratio)

    def __call__(self, *args, **kwargs) -> np.ndarray:
        return self.__image

# Path: prepareMap.py

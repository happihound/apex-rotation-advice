import cv2 as cv


class gameMapImage:
    def __init__(self, image, ratio=""):
        self.__image = image
        self.__ratio = ratio

    __slots__ = ["__image", "__ratio"]

    def ratio(self):
        return self.__ratio

    def image(self):
        return self.__image

    def copy(self):
        return gameMapImage(self.__image, self.__ratio)

    def __call__(self, *args, **kwargs):
        return self.__image

# Path: prepareMap.py

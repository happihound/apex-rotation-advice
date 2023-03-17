import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from prepareMap import prepareMap
from gameMapImage import gameMapImage
from pytest import approx


def test_return_ratio_16by10():
    cv2Image = cv.imread("test_images/16by10/test_image1_16by10.png")
    image = gameMapImage(cv2Image, "16by10")
    assert image.ratio() == "16by10"


def test_return_ratio_16by9():
    cv2Image = cv.imread("test_images/16by9/test_image1_16by9.png")
    image = gameMapImage(cv2Image, "16by9")
    assert image.ratio() == "16by9"


def test_return_ratio_4by3():
    cv2Image = cv.imread("test_images/4by3/test_image1_4by3.png")
    image = gameMapImage(cv2Image, "4by3")
    assert image.ratio() == "4by3"


def test_return_image_16by10():
    cv2Image = cv.imread("test_images/16by10/test_image1_16by10.png")
    image = gameMapImage(cv2Image, "16by10")
    assert image.image() is cv2Image


def test_return_image_16by9():
    cv2Image = cv.imread("test_images/16by9/test_image1_16by9.png")
    image = gameMapImage(cv2Image, "16by9")
    assert image.image() is cv2Image


def test_return_image_4by3():
    cv2Image = cv.imread("test_images/4by3/test_image1_4by3.png")
    image = gameMapImage(cv2Image, "4by3")
    assert image.image() is cv2Image

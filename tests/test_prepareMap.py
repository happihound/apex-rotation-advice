import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from userMapImage import userMapImage
delay = 2000


def test_returnCropSize_16by10():
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    changedImage = userMapImage(cv2Image, "16by10")
    cv.imshow("16by10", changedImage.getCroppedImage().image())
    cv.waitKey(delay)
    cv.destroyAllWindows()


def test_returnCropSize_4by3():
    cv2Image = cv.imread("tests/test_images/4by3/test_image1_4by3.png")
    changedImage = userMapImage(cv2Image, "4by3")
    cv.imshow("4by3", changedImage.getCroppedImage().image())
    cv.waitKey(delay)
    cv.destroyAllWindows()


def test_returnCropSize_16by9():
    cv2Image = cv.imread("tests/test_images/16by9/test_image1_16by9.png")
    changedImage = userMapImage(cv2Image, "16by9")
    cv.imshow("4by3", changedImage.getCroppedImage().image())
    cv.waitKey(delay)
    cv.destroyAllWindows()


def test_wrongApspectRatio():
    cv2Image = cv.imread("tests/test_images/16by9/test_image1_16by9.png")
    try:
        userMapImage(cv2Image, "21by9")
    except ValueError:
        return
    raise ValueError("21by9 ratio is not supported, but was not caught")


if __name__ == "__main__":
    test_returnCropSize_16by10()
    test_returnCropSize_4by3()
    test_returnCropSize_16by9()
    test_wrongApspectRatio()

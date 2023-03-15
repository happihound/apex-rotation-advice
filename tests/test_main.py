import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def test_returnCropSize_16by10():
    main = __import__("main")
    # Setup
    image = cv.imread("test_images/16by10/test_image1_16by10.png")
    # Test
    topLeft, topRight, bottomLeft, bottomRight = main.returnCropSize(image.shape, "16:10")
    # Assert
    assert topLeft == (315, 0)
    assert topRight == (1302, 0)
    assert bottomLeft == (315, 989)
    assert bottomRight == (1302, 989)

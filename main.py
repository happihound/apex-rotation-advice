import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def main():
    #image = cv.imread("test_images/4by3/test_image1_4by3.png")
    image = cv.imread("test_images/4by3/test_image1_4by3.png")
    changedImage = findCornersOfMap(image)
    cv.imshow("changedImage", changedImage)
    cv.waitKey(0)


# Takes a cv2 image and returns a cv2 image
# finds the corners of the map from the full image
# Returns a cropped image of only the map
def findCornersOfMap(image, ratio=""):
    if ratio == "":
        ratio = detectAspectRatio(image.shape)
    topLeft, topRight, bottomLeft, bottomRight = returnCropSize(image.shape, ratio)
    # Crop the image
    image = image[topLeft[1]:bottomLeft[1], topLeft[0]:topRight[0]]
    # Change the aspect ratio of the image
    image = changeImageAspectRatio(image)
    return image


# Takes a cv2 image and returns a cv2 image
# change to a 1:1 aspect ratio
# change to 800x800


def detectAspectRatio(imageShape):
    height, width, channels = imageShape
    if height * 4 == width * 3:
        return "4:3"
    if height * 16 == width * 10:
        return "16:10"
    if height * 16 == width * 9:
        return "16:9"
    raise ValueError("Invalid aspect ratio", height, width)


def returnCropSize(imageShape, ratio):
    height, width, channels = imageShape
    # The dictionary is in the format {aspectRatio: (leftMarginRatio, righMarginRatip, bottomMarginRatio)}
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


def changeImageAspectRatio(image):
    image = cv.resize(image, (image.shape[0], image.shape[0]), interpolation=cv.INTER_AREA)
    return image


if __name__ == "__main__":
    main()

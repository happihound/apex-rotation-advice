import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from prepareMap import prepareMap
from gameMapImage import gameMapImage
import imutils
import csv
from poi_coordinator import coordinator
from poi_node import poi


def main():
    myCoordinator = coordinator()
    myCoordinator.loadMap("WE")
    totalDistance = 0
    start = myCoordinator.getPoi(poiID=7)
    end = myCoordinator.getPoi(poiID=65)
    path = myCoordinator.findShortestPath(start, end)
    for i in range(len(path) - 1):
        totalDistance += myCoordinator.distanceBetweenPoi(path[i], path[i + 1])
    print("Start: " + start.getName())
    print("End: " + end.getName())
    print("Total distance: " + str(totalDistance))
    print("Path: ")
    for i in range(len(path)):
        print("\t"+path[i].getName())
    xcoords = []
    ycoords = []
    for i in range(len(path)):
        xcoords.append(path[i].getX())
        ycoords.append(path[i].getY())
    plt.imshow(cv.imread("game_map/default/mapWE.png", cv.IMREAD_GRAYSCALE), cmap='gray')
    plt.plot(xcoords, ycoords)
    plt.show()


def main2():
    cv2Image = cv.imread("test_images/4by3/test_image1_4by3.png")
    #cv2Image = cv.imread("test_images/16by10/test_image1_16by10.png")
    # Create an object of gameMapImage data type
    image = gameMapImage(cv2Image, "4by3")
    # Run the prepareMap class on the image
    changedImage = prepareMap(image).run()
    cv.imshow("formatted", image())
    cv.waitKey(0)
    # Show the image
    image = thresholdImage(changedImage)
    cv.imshow("thresholdImage", image.image())
    cv.waitKey(0)
    countRedChevons(image)
    cv.destroyAllWindows()


def thresholdImage(image):
    # threshold all the pixels that arent bright red
    ratio = image.ratio()
    image = image.image()

    # convert to hsv
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # define range of red color in hsv
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # threshold the hsv image to get only red colors
    mask = cv.inRange(hsv, lower_red, upper_red)

    # bitwise and mask and original image
    res = cv.bitwise_and(image, image, mask=mask)

    return gameMapImage(res, ratio)


def countRedChevons(image):
    # convert the image to grayscale
    gray = cv.cvtColor(image.image(), cv.COLOR_BGR2GRAY)

    # blur it slightly
    thresh = cv.GaussianBlur(gray, (15, 15), 0)

    labels = cv.connectedComponentsWithStats(thresh)
    mask = np.zeros(thresh.shape, dtype="uint8")

    # loop over the unique components
    for i in range(0, labels[0]):
        # if this is the first component then we examine the
        # *background* (typically we would just ignore this
        # component in our loop)
        if i == 0:
            text = "examining component {}/{}".format(i + 1,
                                                      labels[0])
            print("[INFO] {}".format(text))
            continue

        # otherwise, construct the label mask and count the
        # number of pixels
        print("[INFO] examining component {}/{}".format(i + 1,
                                                        labels[0]))
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels[1] == i] = 255
        numPixels = cv.countNonZero(labelMask)

        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if numPixels > 300:
            mask = cv.add(mask, labelMask)

    # find the contours in the mask, then sort them from left to
    # right
    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,
                           cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    print("[INFO] {} unique contours found".format(len(cnts)))
    cv.imshow("Mask", mask)
    cv.waitKey(0)

    # loop over the contours


if __name__ == "__main__":
    main()

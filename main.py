import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from prepareMap import prepareMap
from gameMapImage import gameMapImage
import imutils
import csv


def main():
    # take in the csv from nodes/poi_WE.csv
    # the csv is in the format of: id,name, x, y, radius, type
    # where type is either choke or poi
    # if it is a choke, then it is a point, if it is a poi, then it is a circle
    # graph using matplotlib
    # create a graph of the map
    x = []
    y = []
    radius = []
    i = 0
    with open("game_map/nodes/poi_WE.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            print(row)
            i += 1
            x.append(int(row[2]))
            y.append(int(row[3]))
            if "True" in row[5]:
                radius.append(9*2)
            else:
                radius.append(int(row[4])*2)
    # load the image from game_map/default/mapWE.png and display in the graph
    plt.scatter(x, y, s=radius)
    plt.imshow(cv.imread("game_map/default/mapWE.png"))
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
    main2()

import math
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
    start = myCoordinator.getPoi(poiID=28)
    end = myCoordinator.getPoi(poiID=28)
    start2 = myCoordinator.getPoi(poiID=71)
    end2 = myCoordinator.getPoi(poiID=39)
    avoidCoords = doImage()
    path = myCoordinator.avoidPlayers(start, end, avoidCoords)
    #path2 = myCoordinator.avoidPlayers(start2, end2, avoidCoords)
    #path = path + path2
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
    for i in range(len(avoidCoords)):
        plt.scatter(avoidCoords[i][0], avoidCoords[i][1], s=30, color='red')
    plt.plot(xcoords, ycoords)

    plt.show()
    plt.pause(0.001)


def doImage():
    # cv2Image =
    # cv2Image =
    # Create an object of gameMapImage data type
    #image = gameMapImage(cv.imread("test_images/4by3/test_image3_4by3.png"), "4by3")
    #image = gameMapImage(cv.imread("test_images/16by9/test_image2_16by9.png"), "16by9")
    image = gameMapImage(cv.imread("test_images/16by10/test_image1_16by10.png"), "16by10")
    # cv.imshow("changedImage", image())
    # cv.waitKey(0)
    # Run the prepareMap class on the image
    changedImage = prepareMap(image)
    changedImage = changedImage.run()
    # cv.imshow("changedImage", changedImage())
    # cv.waitKey(0)
    # Show the image
    changedImage = thresholdImage(changedImage)
    # cv.imshow("changedImage", changedImage())
    # cv.waitKey(0)
    return findRedDots(changedImage)


def thresholdImage(image):
    # threshold all the pixels that arent red
    ratio = image.ratio()
    image = image.image()

    # convert to hsv
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

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
    res = cv.bitwise_and(image, image, mask=mask)

    res2 = cv.bitwise_and(image, image, mask=mask2)

    res = cv.bitwise_or(res, res2)
    # erode to remove noise
    res = cv.erode(res, None, iterations=1)
    # dilate to fill in gaps
    res = cv.dilate(res, None, iterations=1)

    return gameMapImage(res, ratio)


def findRedDots(image):
    # find the red dots
    image = gameMapImage(cv.cvtColor(image(), cv.COLOR_BGR2GRAY), image.ratio())
    image = gameMapImage(cv.GaussianBlur(image(), (5, 5), 0), image.ratio())
    # image = cv.Canny(image, 50, 100)
    # image = cv.dilate(image, None, iterations=1)
    # image = cv.erode(image, None, iterations=1)
    # cv.imshow("canny", image)
    # cv.waitKey(0)
    # image = cv.threshold(image, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    # cv.imshow("threshold", image)
    # cv.waitKey(0)
    cnts = cv.findContours(image(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    circles = []
    for c in cnts:
        # compute the center of the contour
        M = cv.moments(c)
        if M["m00"] != 0:
            cX = int((M["m10"] / M["m00"]))
            cY = int((M["m01"] / M["m00"]))
            #print("cX: " + str(cX) + " cY: " + str(cY))
            # draw the contour and center of the shape on the image
            cv.drawContours(image(), [c], -1, (0, 255, 0), 2)
            minshape = cv.minEnclosingCircle(c)
            circles.append(minshape)
            # filter out huge circle
    i = 0
    toDraw = filterCirlces(circles)

    for circle in toDraw:
        cv.circle(image(), (int(circle[0][0]), int(circle[0][1])), int(circle[1]), (255, 255, 255), 2)
    print(len(toDraw))
    returnPoints = []
    for circle in toDraw:
        returnPoints.append((int(circle[0][0]), int(circle[0][1])))
    for i in range(len(returnPoints)):
        returnPoints[i] = (int(returnPoints[i][0]*(4096/800)), int(returnPoints[i][1]*(4096/800)))
    return returnPoints


def filterCirlces(circles):
    toDraw = []
    toRemove = []
    for circle in circles:
        for circle2 in circles:
            if circle != circle2:
                if circle2[1] > 15:
                    continue
                distance = math.sqrt((circle[0][0]-circle2[0][0])**2+(circle[0][1]-circle2[0][1])**2)
                if (distance < (circle[1]+circle2[1]+(circle[1]+circle2[1])*0.5)):
                    newCircle = ((circle[0][0]+circle2[0][0])/2, (circle[0]
                                 [1]+circle2[0][1])/2), (circle[1]+circle2[1]+(circle[1]+circle2[1])*0.5)
                    if newCircle not in toDraw:
                        toDraw.append(newCircle)
                    toRemove.append(circle)
                    toRemove.append(circle2)
                    break
                else:
                    if circle not in toDraw:
                        toDraw.append(circle)
    for circle in toRemove:
        toDraw = remove(toDraw, circle)
    return toDraw


def remove(the_list, val):
    return [value for value in the_list if value != val]


if __name__ == "__main__":
    main()

import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import userMapImage as mapImage
from gameMapImage import gameMapImage
import csv
from poi_coordinator import coordinator
from poi_node import poi


def main():
    myCoordinator = coordinator()
    myCoordinator.loadMap("WE")
    totalDistance = 0
    start = myCoordinator.getPoi(poiID=1)
    end = myCoordinator.getPoi(poiID=74)
    start2 = myCoordinator.getPoi(poiID=74)
    end2 = myCoordinator.getPoi(poiID=14)
    usermap = cv.imread("tests/test_images/16by10/test_image4_16by10.png", cv.IMREAD_UNCHANGED)
    userMapImage = mapImage.userMapImage(usermap, "16:10")
    avoidCoords = userMapImage.getTargets()
    path = myCoordinator.avoidPlayers(start, end, avoidCoords)
    path2 = myCoordinator.avoidPlayers(start2, end2, avoidCoords)
    path = path + path2
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
    WEmap = cv.imread("game_map/default/mapWE.png", cv.IMREAD_UNCHANGED)
    WEmap = cv.cvtColor(WEmap, cv.COLOR_BGR2RGB)
    plt.imshow(WEmap)
    for i in range(len(avoidCoords)):
        plt.scatter(avoidCoords[i][0], avoidCoords[i][1], s=30, color='red')
    plt.plot(xcoords, ycoords)
    plt.show()
    plt.pause(0.001)


if __name__ == "__main__":
    main()

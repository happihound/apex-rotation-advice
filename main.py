import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from userMapImage import userMapImage
from gameMapImage import gameMapImage
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
    avoidCoords =
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


if __name__ == "__main__":
    main()

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from prepareMap import prepareMap
from gameMapImage import gameMapImage
import imutils
import csv
from poi_coordinator import coordinator
x = []
y = []
radius = []
currentPoiList = []
myCoordinator = coordinator()


def main():
    myCoordinator.loadMap("WE")
    assocationLinesX = []
    assocationLinesY = []
    # load the image from game_map/default/mapWE.png and display in the graph
    for poi in myCoordinator.getPoiList():
        print(poi.getName())
        xcoord, ycoord = poi.getCoords()
        x.append(xcoord)
        y.append(ycoord)
        if poi.getChoke() == True:
            radius.append(9*4)
        else:
            radius.append(poi.getRadius())
        if poi.getAssociations() != []:
            for association in poi.getAssociations():
                assocationLinesX.append([xcoord, association.getCoords()[0]])
                assocationLinesY.append([ycoord, association.getCoords()[1]])
                print("\t", association.getName())

    plt.scatter(x, y, s=radius, color='green')
    for value in range(len(assocationLinesX)):
        pass
        # plt.plot(assocationLinesX[value], assocationLinesY[value], color='red', linewidth=0.2)
    plt.imshow(cv.imread("game_map/default/mapWE.png", cv.IMREAD_GRAYSCALE), cmap='gray')
    # print all clicks

    def onclick(event):
        xClick = int(event.xdata)
        yClick = int(event.ydata)
        clickType = event.button
        if clickType == 1:
            plt.cla()
            plt.scatter(x, y, s=radius, color='green')
            plt.imshow(cv.imread("game_map/default/mapWE.png", cv.IMREAD_GRAYSCALE), cmap='gray')
            plt.pause(0.001)
            plt.show()
            for i in range(len(x)):
                if xClick > x[i] - radius[i] and xClick < x[i] + radius[i] and yClick > y[i] - radius[i] and yClick < y[i] + radius[i]:
                    primaryNode = myCoordinator.getPoi(poiID=i+1)
                    associatedPois = primaryNode.getAssociations()
                    for poi in associatedPois:
                        plt.plot((primaryNode.getX(), poi.getX()),
                                 (primaryNode.getY(), poi.getY()), color='red', linewidth=0.3)
            plt.pause(0.001)
            plt.show()

    def onclick1(event):
        xClick = event.xdata
        yClick = event.ydata
        clickType = event.button
        if clickType == 1:
            for i in range(len(x)):
                if xClick > x[i] - radius[i] and xClick < x[i] + radius[i] and yClick > y[i] - radius[i] and yClick < y[i] + radius[i]:
                    print(i+1, end=",", flush=True)
                    currentPoiList.append(int(i+1))
                    #print(myCoordinator.getPoi(poiID=int(i+1)).getAssociationNames(), flush=True)
                    break
        if clickType == 3:
            print("", flush=True)
            for enum, value in enumerate(currentPoiList):
                xcoord, ycoord = myCoordinator.getPoi(poiID=value).getCoords()
                xlocal, ylocal = myCoordinator.getPoi(poiID=currentPoiList[0]).getCoords()
                plt.plot((xcoord, xlocal), (ycoord, ylocal), color='blue')
                print(myCoordinator.getPoi(poiID=value).getName(), end=", ")
            plt.pause(0.001)
            plt.show()
            currentPoiList.clear()
            print("", flush=True)

    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    plt.pause(0.001)


if __name__ == "__main__":
    main()

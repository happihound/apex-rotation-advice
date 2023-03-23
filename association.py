import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from userMapImage import userMapImage
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
    # load the map
    myCoordinator.loadMap("WE")
    # create the lists to store the x and y coordinates of the points of interest
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
    # Show the image
    WEmap = cv.imread("game_map/default/mapWE.png", cv.IMREAD_GRAYSCALE)
    WEmap = cv.cvtColor(WEmap, cv.COLOR_BGR2RGB)
    plt.imshow(WEmap)

    # This will draw the lines between all the associations on the map
    # for value in range(len(assocationLinesX)):
    #   plt.plot(assocationLinesX[value], assocationLinesY[value], color='red', linewidth=0.2)

    # to show the current associations of a poi
    cid = plt.gcf().canvas.mpl_connect('button_press_event', showCurrentPoiAssociations)

    # to create new association
    #cid = plt.gcf().canvas.mpl_connect('button_press_event', createAssociation)
    plt.show()
    plt.pause(0.001)


def showCurrentPoiAssociations(event):
    try:
        # Retrieve the x and y coordinates of the click
        xClick = int(event.xdata)
        yClick = int(event.ydata)

        # Clear the plot and draw the map and the POIs again
        plt.clf()
        plt.scatter(x, y, s=radius, color='green')
        #plt.imshow(cv.imread("game_map/default/mapWE.png", cv.IMREAD_GRAYSCALE), cmap='gray')
        plt.pause(0.001)
        plt.show()

        # Check if the click is inside a POI
        for i in range(len(x)):
            if xClick > x[i] - radius[i] and xClick < x[i] + radius[i] and yClick > y[i] - radius[i] and yClick < y[i] + radius[i]:
                # Retrieve the POI object
                primaryNode = myCoordinator.getPoi(poiID=i+1)

                # Retrieve the list of associated POIs
                associatedPois = primaryNode.getAssociations()

                # Draw the associations
                for poi in associatedPois:
                    plt.plot((primaryNode.getX(), poi.getX()),
                             (primaryNode.getY(), poi.getY()), color='red', linewidth=0.3)
        plt.pause(0.001)
        plt.show()
    except Exception as e:
        print(e)


def createAssociation(event):
    try:
        # get the x and y coordinates of the click
        xClick = event.xdata
        yClick = event.ydata
        # determine if it was a left or right click
        clickType = event.button
        if clickType == 1:
            # iterate through all the poi's
            for i in range(len(x)):
                # determine if the click was within the radius of the poi
                if xClick > x[i] - radius[i] and xClick < x[i] + radius[i] and yClick > y[i] - radius[i] and yClick < y[i] + radius[i]:
                    print(i+1, end=",", flush=True)
                    currentPoiList.append(int(i+1))
                    break
        if clickType == 3:
            print("", flush=True)
            # iterate through the poi's in the array
            for enum, value in enumerate(currentPoiList):
                # get the x and y coordinates of the poi
                xcoord, ycoord = myCoordinator.getPoi(poiID=value).getCoords()
                # get the x and y coordinates of the first poi in the array
                xlocal, ylocal = myCoordinator.getPoi(poiID=currentPoiList[0]).getCoords()
                # plot a line between the two poi's
                plt.plot((xcoord, xlocal), (ycoord, ylocal), color='blue')
                # print the name of the poi, which can be copied and pasted into the csv file
                print(myCoordinator.getPoi(poiID=value).getName(), end=", ")
            plt.pause(0.001)
            plt.show()
            currentPoiList.clear()
            print("", flush=True)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

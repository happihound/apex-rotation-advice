import cv2 as cv
import matplotlib.pyplot as plt
from poi_coordinator import coordinator


class association:
    __slots__ = ['__currentPoiList', '__coordinator', "__mapName", "__mapImage", "__validMaps"]

    def __init__(self, mode, validMaps, mapName):
        self.__validMaps = validMaps
        if mode == None or mode == "":
            raise Exception("Please enter a mode. Valid modes are 'all', 'view', and 'create'")
        if mode != "all" and mode != "view" and mode != "create" and mode != 1 and mode != 2 and mode != 3:
            raise Exception("Invalid mode. Please enter 'all', 'view', or 'create', not " + mode)
        self.__mapName = mapName
        self.__coordinator = coordinator(self.__validMaps)
        self.__coordinator.loadMap(self.__mapName)
        self.__currentPoiList = []
        self.__plotAllPois()
        # load the image from game_map/default/mapWE.png and display in the graph along with the POIs
        # to show the current associations of a poi
        # Convert the mode to an integer
        if mode == "all":
            mode = 1
        if mode == "view":
            mode = 2
        if mode == "create":
            mode = 3
        # if mode is 1 or "all", then show the map and the associations
        if mode == 1:
            self.__plotAllAssociations()
        # if mode is 2 or "view", then show the map and allow the user to view individual associations
        if mode == 2:
            cid = plt.gcf().canvas.mpl_connect('button_press_event', self.__showCurrentPoiAssociations)
        # if mode is 3 or "create", then show the map and allow the user to create associations
        if mode == 3:
            cid = plt.gcf().canvas.mpl_connect('button_press_event', self.__createAssociation)
        plt.show()
        plt.pause(0.001)

    def __plotAllPois(self):
        # Show the image
        self.__loadGameMap()
        plt.clf()
        plt.imshow(self.__mapImage)
        # Plot all the POIs
        for poi in self.__coordinator.getPoiList():
            plt.scatter(poi.getX(), poi.getY(), s=poi.getRadius(), color='green')
        plt.gcf().canvas.draw()

    def __plotAllAssociations(self):
        # Show the image
        self.__plotAllPois()
        plt.imshow(self.__mapImage, cmap='gray')
        # Plot all the POIs
        for poi in self.__coordinator.getPoiList():
            # Plot the POI
            plt.scatter(poi.getX(), poi.getY(), s=poi.getRadius(), color='green')
            # Plot the POI's associations
            for association in poi.getAssociations():
                plt.plot((poi.getX(), association.getX()), (poi.getY(), association.getY()), color='red',
                         linewidth=0.3)
        plt.pause(0.001)
        plt.show()

    def __loadGameMap(self):
        if self.__mapName not in self.__validMaps:
            raise Exception("Invalid map name given, " + self.__mapName + " please enter a valid map name.")
        if self.__mapName == "WE":
            tempMap = cv.imread("game_map/default/mapWE.png", cv.IMREAD_UNCHANGED)
            self.__mapImage = cv.cvtColor(tempMap, cv.COLOR_BGR2RGB)

    def __showCurrentPoiAssociations(self, event):
        try:
            # Retrieve the x and y coordinates of the click
            xClick = int(event.xdata)
            yClick = int(event.ydata)

            # Clear the plot and draw the map and the POIs again
            plt.clf()
            self.__plotAllPois()

            # Find the poi closest to the click
            primaryNode = self.__coordinator.findPoiFromLocation(xClick, yClick)

            # Retrieve the list of associated POIs
            associatedPois = primaryNode.getAssociations()

            # Draw the associations
            for poi in associatedPois:
                plt.plot((primaryNode.getX(), poi.getX()),
                         (primaryNode.getY(), poi.getY()), color='red', linewidth=0.3)
            plt.pause(0.001)
            plt.gcf.canvas.draw()
        except Exception as e:
            pass

    def __createAssociation(self, event):
        try:
            # get the x and y coordinates of the click
            xClick = int(event.xdata)
            yClick = int(event.ydata)
            # determine if it was a left or right click
            clickType = event.button
            if clickType == 1:
                # find the poi closest to the click
                xClick = int(event.xdata)
                yClick = int(event.ydata)
                if len(self.__currentPoiList) == 0:
                    nearestPoi = self.__coordinator.findPoiFromLocation(xClick, yClick)
                    self.__currentPoiList.append(nearestPoi)
                else:
                    # Find the poi closest to the click
                    nearestPoi = self.__coordinator.findPoiFromLocation(xClick, yClick)
                if nearestPoi not in self.__currentPoiList and nearestPoi.getID() not in self.__currentPoiList[0].getAssociationIDs():
                    print(nearestPoi.getID(), end=",", flush=True)
                # add the poi to the array
                self.__currentPoiList.append(nearestPoi)
                xcoord, ycoord = nearestPoi.getCoords()
                xlocal, ylocal = self.__currentPoiList[0].getCoords()
                plt.scatter(xlocal, ylocal, s=self.__currentPoiList[0].getRadius(), color='red')
                plt.plot((xcoord, xlocal), (ycoord, ylocal), color='blue')
                # print the poi's id, which can be copied and pasted into the csv file
                plt.pause(0.001)
            if clickType == 3:
                self.__plotAllPois()
                print("", flush=True)
                self.__currentPoiList = []

        except Exception as e:
            print(e)

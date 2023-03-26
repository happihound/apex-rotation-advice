import glob
import cv2 as cv
import matplotlib.pyplot as plt
import userMapImage as mapImage
from poi_coordinator import coordinator


class findSafePath:
    __slots__ = ['__mapName', '__mapImage', '__gameMapImage',
                 '__coordinator', '__poiList', '__userMapImage', '__currentPoiList', '__validMaps']

    def __init__(self, mapName, validMaps, ratio=None):
        self.__mapName = mapName
        self.__validMaps = validMaps
        self.__currentPoiList = []
        if ratio != None:
            self.__userMapImage = mapImage.userMapImage(self.__loadUserMap(), ratio)
        else:
            self.__userMapImage = mapImage.userMapImage(self.__loadUserMap())
        self.run()

    def __loadUserMap(self):
        # grab the image file in the inputScan folder regardless of name
        path = "inputScan/*.png"
        files = glob.glob(path)
        if len(files) == 0:
            raise Exception("No image found in inputScan folder.")
        elif len(files) > 1:
            raise Exception("Multiple images found in inputScan folder.")
        else:
            usermap = cv.imread(files[0], cv.IMREAD_UNCHANGED)
        return usermap

    def __loadGameMap(self):
        # grab the image file in the inputScan folder
        if self.__mapName not in self.__validMaps:
            raise Exception("Invalid map name given, " + self.__mapName + " please enter a valid map name.")
        if self.__mapName == "WE":
            tempMap = cv.imread("game_map/default/mapWE.png", cv.IMREAD_UNCHANGED)
            self.__mapImage = cv.cvtColor(tempMap, cv.COLOR_BGR2RGB)
        else:
            raise Exception("Invalid map name given, "+self.__mapName+" please enter a valid map name.")

    def run(self):
        self.__coordinator = coordinator(self.__validMaps)
        self.__coordinator.loadMap(self.__mapName)
        totalDistance = 0
        avoidCoords = self.__userMapImage.getTargets()
        poisToVisit = self.__pickTwoPois()
        start = poisToVisit[0]
        end = poisToVisit[-1]
        path = []
        for i in range(len(poisToVisit)-1):
            path += self.__coordinator.avoidPlayers(poisToVisit[i], poisToVisit[i+1], avoidCoords)
        for i in range(len(path) - 1):
            totalDistance += self.__coordinator.distanceBetweenPoi(path[i], path[i + 1])
        print("Start: " + start.getName())
        print("\tPois to visit: ", self.__coordinator.poiListToNames(poisToVisit))
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

        plt.imshow(self.__mapImage)
        for i in range(len(avoidCoords)):
            plt.scatter(avoidCoords[i][0], avoidCoords[i][1], s=30, color='red')
        plt.plot(xcoords, ycoords, color='white', linewidth=2)
        colors = ['red', 'green', 'blue', 'yellow', 'orange']
        vistedCount = 0
        for i in range(1, len(path)):
            # add arrows to the line
            plt.annotate("", xy=(xcoords[i], ycoords[i]), xytext=(xcoords[i-1], ycoords[i-1]),
                         arrowprops=dict(arrowstyle="->", color="white"), size=22)
        plt.show()
        plt.pause(0.001)

    def plotAllPois(self):
        # Show the image
        self.__loadGameMap()
        plt.imshow(self.__mapImage)
        # Plot all the POIs
        for poi in self.__coordinator.getPoiList():
            plt.scatter(poi.getX(), poi.getY(), s=poi.getRadius(), color='red')

    def __pickTwoPois(self) -> list:
        self.plotAllPois()
        # Show the image
        plt.imshow(self.__mapImage)
        # Connect the two POIs
        cid = plt.gcf().canvas.mpl_connect('button_press_event', self.__selectTwoPois)
        plt.show()
        plt.pause(0.001)
        plt.gcf().canvas.mpl_disconnect(cid)
        plt.gcf().clf()
        plt.close()
        return self.__currentPoiList

    def __selectTwoPois(self, event):
        try:
            # Retrieve the x and y coordinates of the click
            xClick = int(event.xdata)
            yClick = int(event.ydata)
            # Clear the plot and draw the map and the POIs again
            # Find the poi closest to the click
            primaryNode = self.__coordinator.findPoiFromLocation(xClick, yClick)
            # Draw the primary node
            plt.scatter(primaryNode.getX(), primaryNode.getY(),
                        s=primaryNode.getRadius(), color='green')
            self.__currentPoiList.append(primaryNode)
            plt.gcf().canvas.draw()
            plt.pause(0.001)
        except Exception as e:
            pass

from poi_node import poi as poi_node
import csv


class coordinator:
    __slots__ = ["__poi_list", "__poi_dict", "__poi_count", "__map", "__validMaps"]

    def __init__(self, validMaps: list):
        self.__map = ""
        self.__poi_list = []
        self.__poi_dict = {}
        self.__poi_count = 0
        self.__validMaps = validMaps

    def loadMap(self, mapName: str) -> None:
        if (type(mapName) != str):
            raise TypeError("mapName must be of type str")
        # Right now we only have WE, so we'll override the mapName
        if (mapName not in self.__validMaps):
            raise NotImplementedError("Map " + mapName + " is not implemented, only " +
                                      str(self.__validMaps) + " are supported at this time in loadMap")
        self.__map = mapName
        self.__loadPoi("poi_" + self.__map + ".csv")

    def getValidMapNames(self) -> str:
        returnString = ""
        for supported in self.__validMaps:
            returnString += supported + ", "
        returnString = returnString[:-2]
        return returnString

    def getPoiList(self) -> list:
        return self.__poi_list

    def getPoiListNames(self) -> list:
        names = []
        for poi in self.__poi_list:
            names.append(poi.getName())
        return names

    def getPoiDict(self) -> dict:
        return self.__poi_dict

        # This method returns a poi_node object from the list or dictionary of poi_nodes
    def getPoi(self, poiName="", poiID=-1) -> poi_node:
        # Checks that poiName is of type str
        if (type(poiName) != str):
            raise TypeError("poiName must be of type str in getPoi")
        # Checks that poiID is of type int
        if (type(poiID) != int):
            raise TypeError("poiID must be of type int in getPoi")
        # Checks that poiName and poiID are not both blank
        if (poiName == "" and poiID == -1):
            raise ValueError("poiName and poiID cannot both be empty in getPoi")
        # Checks that poiName and poiID are not both filled
        if (poiName != "" and poiID != ""):
            # Iterates through the list of poi_nodes
            for poi in self.__poi_list:
                # Checks that the name and ID of the poi_node match the input
                if (poi.getName() == poiName and poi.getID() == poiID):
                    return poi
            # Raises an error if the name and ID do not match the input
            raise ValueError("poiName and poiID do not match in getPoi")
        # Checks that poiName is not blank
        if (poiName != ""):
            # Iterates through the list of poi_nodes
            for poi in self.__poi_list:
                # Checks that the name of the poi_node matches the input
                if (poi.getName() == poiName):
                    return poi
            # Raises an error if the name does not match the input
            raise ValueError("poiName is not found in getPoi")
        # Checks that poiID is not blank
        if (poiID != -1):
            # Iterates through the list of poi_nodes
            for poi in self.__poi_list:
                # Checks that the ID of the poi_node matches the input
                if (poi.getID() == poiID):
                    return poi
            # Raises an error if the ID does not match the input
            raise ValueError("poiID is not found in getPoi")
        # Checks that poiName is not blank
        if (poiName != ""):
            # Returns a poi_node from the dictionary of poi_nodes
            return self.__poi_dict[poiName]
        # Raises an error if all other checks fail
        raise ValueError("An error has occurred in getPoi")

    def getNumberOfPoi(self) -> int:
        return self.__poi_count

    def distanceBetweenPoi(self, point1: poi_node, point2: poi_node) -> int:
        if (type(point1) != poi_node):
            raise TypeError("point1 must be of type poi_node in distanceBetweenPoi, not " +
                            str(type(point1)))
        if (type(point2) != poi_node):
            raise TypeError("point2 must be of type poi_node in distanceBetweenPoi, not " +
                            str(type(point2)))
        # Return the distance between two poi nodes
        return int(((point1.getX() - point2.getX())**2 + (point1.getY() - point2.getY())**2)**0.5)

    def findShortestPath(self, start: poi_node, end: poi_node) -> list:
        # check that start and end are of type poi_node
        if (type(start) != poi_node):
            raise TypeError("start must be of type poi_node in findShortestPath")
        if (type(end) != poi_node):
            raise TypeError("end must be of type poi_node in findShortestPath")
        # create an empty list that will store the path
        path = []
        # add the starting poi_node to the list
        path.append(start)
        # iterate through the list until the last element is the end poi_node
        while (path[-1] != end):
            # set the shortestDistance to 1 (because all distances are greater than 0)
            shortestDistance = 1
            # set the shortestPoi to None (because there is no poi_node yet)
            shortestPoi = None
            # iterate through the associations of the last element in the list
            for poi in path[-1].getAssociations():
                # if the poi_node is already in the list, skip it
                if (poi in path):
                    continue
                # if the shortestDistance has not been set, set it
                if (shortestDistance == 1):
                    shortestDistance = self.distanceBetweenPoi(poi, end)
                    shortestPoi = poi
                else:
                    # compare the current shortest distance to the current distance
                    if (self.distanceBetweenPoi(poi, end) < shortestDistance):
                        # if the current distance is shorter, set it as the shortest distance
                        shortestDistance = self.distanceBetweenPoi(poi, end)
                        shortestPoi = poi
            # add the poi_node with the shortest distance to the end to the list
            path.append(shortestPoi)
        # return the list
        return path

    def findPoiFromLocation(self, x: int, y: int) -> poi_node:
        # Check that x and y are of type int
        if (type(x) != int):
            raise TypeError("x must be of type int in findPoiFromLocation")
        if (type(y) != int):
            raise TypeError("y must be of type int in findPoiFromLocation")
        # Initialise variables
        shortestDistance = 999999
        shortestPoi = None
        locationPOI = self.convertCoordsToPoi((x, y))
        # Find the shortest distance between the location and the POIs
        for poi in self.__poi_list:
            if (self.distanceBetweenPoi(locationPOI, poi) < shortestDistance):
                shortestDistance = self.distanceBetweenPoi(locationPOI, poi)
                shortestPoi = poi
        return shortestPoi  # type: ignore

    def convertCoordsToPoi(self, coords: tuple) -> poi_node:
        # coords must be a tuple of 2 ints
        if (type(coords) != tuple):
            raise TypeError("coords must be of type tuple, not " + str(type(coords)) + "in convertCoordsToPOI")
        if (len(coords) != 2):
            raise ValueError("coords must be of length 2 not " + str(len(coords)) + "in convertCoordsToPOI")
        if (type(coords[0]) != int):
            raise TypeError("coords[0] must be of type int in convertCoordsToPOI")
        if (type(coords[1]) != int):
            raise TypeError("coords[1] must be of type int in convertCoordsToPOI")
        # return a poi_node object with coords as its coordinates
        returnPoint = poi_node(-1, "poiFromCoords", coords[0], coords[1], 1, False)
        return returnPoint

    def findAllNearPoi(self, mainPoi: poi_node, distance: int) -> list:
        # Checks that the poi_node given is of type poi_node
        if (type(mainPoi) != poi_node):
            raise TypeError("poi must be of type poi_node in findAllNearPoi")
        # Checks that the distance given is an integer
        if (type(distance) != int):
            raise TypeError("distance must be of type int in findAllNearPoi")
        # Checks that the distance given is greater than 0
        if (distance < 0):
            raise ValueError("distance must be greater than 0 in findAllNearPoi")
        # Creates a list to store poi_nodes that are within the given distance
        nearPoi = []
        # Goes through each poi_node in the graph
        for poi in self.__poi_list:
            # Checks if the poi_node is within the given distance
            if (self.distanceBetweenPoi(mainPoi, poi) <= distance):
                # Adds the poi_node to the list
                nearPoi.append(poi)
        return nearPoi

    def avoidPlayers(self, start: poi_node, end: poi_node, playerLocations: list) -> list:
        # check that start and end are of type poi_node
        if (type(start) != poi_node):
            raise TypeError("start must be of type poi_node in avoidPlayers")
        if (type(end) != poi_node):
            raise TypeError("end must be of type poi_node in avoidPlayers")

        # check that playerLocations is a list
        if (type(playerLocations) != list):
            raise TypeError("playerLocations must be of type list in avoidPlayers")

        # check that playerLocations is not empty
        if (len(playerLocations) == 0):
            raise ValueError("playerLocations must not be empty in avoidPlayers")

        path = self.__internalAvoidPlayers(start, end, playerLocations, 1)
        return path

    def poiListToNames(self, poiList) -> str:
        # check if poiList is of type list
        if (type(poiList) != list):
            raise TypeError("poiList must be of type list in poiListToNames")
        # check if poiList is not empty
        if (len(poiList) == 0):
            raise ValueError("poiList must not be empty in poiListToNames")
        # initialize return string
        returnString = ""
        # iterate over poiList and add poi names to return string
        for poi in poiList:
            returnString += poi.getName() + "->"
        # remove last two characters (->) from return string
        return returnString[:-2]

    def __internalAvoidPlayers(self, start: poi_node, end: poi_node, playerLocations: list, attempt: int) -> list:
        # If we have tried more than 10 times to find a path, we give up and raise an error
        if attempt > 10:
            raise ValueError("Too many attempts to find a path")
        # Convert the player locations to poi nodes
        playerAvoidNodes = []
        for location in playerLocations:
            playerAvoidNodes.append(self.convertCoordsToPoi(location))
        nearestLocations = []
        # If there are no players to avoid, we just return the shortest path
        if playerAvoidNodes == []:
            return self.findShortestPath(start, end)
        # Find all the points of interest within 250 / attempt (we divide by attempt so that we can get more points of interest as the attempt number increases)
        for poi in playerAvoidNodes:
            nearestLocations.append(self.findAllNearPoi(poi, (250//attempt)))
        print("Avoiding players at:")
        # Set all the points of interest to avoid
        if len(nearestLocations) > 0:
            for poi in nearestLocations:
                for poi2 in poi:
                    poi2.setAvoid(True)
                    print("\t"+poi2.getName())
        # Set the start and end to not avoid
        start.setAvoid(False)
        end.setAvoid(False)
        # Try to find the shortest path
        try:
            path = self.findShortestPath(start, end)
        # If no path is found, we try again with a higher distance to avoid
        except AttributeError:
            print("No path found on : " + str(attempt) +
                  " attempt, trying again with a risky path (avoid players further than: " + str(250//attempt+1) + ")")
            for poi in self.__poi_list:
                poi.setAvoid(False)
            return self.__internalAvoidPlayers(start, end, playerLocations, attempt+1)
        return path

    def __addPoi(self, poi: poi_node) -> None:
        # Check that the poi is of type poi_node
        if (type(poi) != poi_node):
            raise TypeError("poi must be of type poi_node in __addPoi")
        # Check that the poi is not already in the graph
        if (poi.getName() in self.__poi_dict):
            raise ValueError("poi: " + poi.getName() + " already exists! in __addPoi")
        # Add the poi to the graph
        self.__poi_list.append(poi)
        self.__poi_dict[poi.getName()] = poi
        self.__poi_count += 1

    def __loadPoi(self, poiFile: str) -> None:
        # open the file
        poiFile = "game_map/nodes/" + poiFile
        onAssociation = False
        with open(poiFile, "r") as f:
            reader = csv.reader(f)
            # skip the first row
            next(reader)
            for row in reader:
                # check if we are on the association row
                if "ASSOCIATION" in row:
                    onAssociation = True
                    continue
                # if we are not on the association row, then we are on the poi row
                if onAssociation == False:
                    # create a new poi
                    choke = False
                    for i in range(len(row)):
                        row[i] = row[i].strip()
                    if "True" in row[5]:
                        choke = True
                    else:
                        choke = False
                    poi = poi_node(int(row[0]), row[1], int(row[2]), int(row[3]), int(row[4]), choke)
                    # add the poi to the list
                    self.__addPoi(poi)
                # if we are on the association row, then we need to add the association to the poi
                if onAssociation == True:
                    # get the current poi
                    currentPoi = self.getPoi(poiID=int(row[0]))
                    # add associations to the current poi
                    for ID in row[1:]:
                        ID = ID.strip()
                        if ID == "":
                            continue
                        currentPoi.addAssociation(self.getPoi(poiID=int(ID)))
        # make sure all the pois are of type poi_node
        for poi in self.__poi_list:
            assert type(poi) == poi_node, "poi must be of type poi_node in __loadPoi " + str(type(poi))

    def __repr__(self):
        return str(self.__poi_list)

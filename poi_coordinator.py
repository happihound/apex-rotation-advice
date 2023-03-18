from poi_node import poi as poi_node
import csv


class coordinator:
    __slots__ = ["__poi_list", "__poi_dict", "__poi_count", "__map"]

    def __init__(self):
        self.__map = ""
        self.__poi_list = []
        self.__poi_dict = {}
        self.__poi_count = 0

    def __addPoi(self, poi: poi_node) -> None:
        if (type(poi) != poi_node):
            raise TypeError("poi must be of type poi_node")
        self.__poi_list.append(poi)
        self.__poi_dict[poi.getName()] = poi
        self.__poi_count += 1

    def __loadPoi(self, poiFile: str) -> None:
        poiFile = "game_map/nodes/" + poiFile
        onAssociation = False
        with open(poiFile, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if "ASSOCIATION" in row:
                    onAssociation = True
                    continue
                if onAssociation == False:
                    choke = False
                    for i in range(len(row)):
                        row[i] = row[i].strip()
                    if "True" in row[5]:
                        choke = True
                    else:
                        choke = False
                    poi = poi_node(int(row[0]), row[1], int(row[2]), int(row[3]), int(row[4]), choke)
                    self.__addPoi(poi)
                if onAssociation == True:
                    currentPoi = self.getPoi(poiID=int(row[0]))
                    for ID in row[1:]:
                        ID = ID.strip()
                        if ID == "":
                            continue
                        currentPoi.addAssociation(self.getPoi(poiID=int(ID)))

    def loadMap(self, mapName: str) -> None:
        if (type(mapName) != str):
            raise TypeError("mapName must be of type str")
        # Right now we only have WE, so we'll override the mapName
        # self.__map = mapName       #uncomment this line when we have more maps
        self.__map = "WE"
        self.__loadPoi("poi_" + self.__map + ".csv")

    def getPoiList(self) -> list:
        return self.__poi_list

    def getPoiDict(self) -> dict:
        return self.__poi_dict

    def getPoi(self, poiName="", poiID=-1) -> poi_node:
        if (type(poiName) != str):
            raise TypeError("poiName must be of type str")
        if (type(poiID) != int):
            raise TypeError("poiID must be of type int")
        if (poiName == "" and poiID == -1):
            raise ValueError("poiName and poiID cannot both be empty")
        if (poiName != "" and poiID != ""):
            for poi in self.__poi_list:
                if (poi.getName() == poiName and poi.getID() == poiID):
                    return poi
            raise ValueError("poiName and poiID do not match")
        if (poiName != ""):
            for poi in self.__poi_list:
                if (poi.getName() == poiName):
                    return poi
            raise ValueError("poiName is not found")
        if (poiID != -1):
            for poi in self.__poi_list:
                if (poi.getID() == poiID):
                    return poi
            raise ValueError("poiID is not found")
        if (poiName != ""):
            return self.__poi_dict[poiName]
        raise ValueError("An error has occurred")

    def distanceBetweenPoi(self, point1: poi_node, point2: poi_node) -> int:
        if (type(point1) != poi_node):
            raise TypeError("point1 must be of type poi_node")
        if (type(point2) != poi_node):
            raise TypeError("point2 must be of type poi_node")
        return int(((point1.getX() - point2.getX())**2 + (point1.getY() - point2.getY())**2)**0.5)

    def findShortestPath(self, start: poi_node, end: poi_node) -> list:
        if (type(start) != poi_node):
            raise TypeError("start must be of type poi_node")
        if (type(end) != poi_node):
            raise TypeError("end must be of type poi_node")
        path = []
        path.append(start)
        while (path[-1] != end):
            print(path[-1].getName())
            shortestDistance = 1
            shortestPoi = None
            for poi in path[-1].getAssociations():
                if (poi in path):
                    continue
                if (shortestDistance == 1):
                    shortestDistance = self.distanceBetweenPoi(poi, end)
                    shortestPoi = poi
                else:
                    if (self.distanceBetweenPoi(poi, end) < shortestDistance):
                        shortestDistance = self.distanceBetweenPoi(poi, end)
                        shortestPoi = poi
            path.append(shortestPoi)
        return path

    def findPoiFromLocation(self, x: int, y: int):
        if (type(x) != int):
            raise TypeError("x must be of type int")
        if (type(y) != int):
            raise TypeError("y must be of type int")
        shortestDistance = 1
        shortestPoi = None
        for poi in self.__poi_list:
            if (shortestDistance == 1):
                shortestDistance = self.distanceBetweenPoi(poi, poi_node(0, "", x, y, 0, False))
                shortestPoi = poi
            else:
                if (self.distanceBetweenPoi(poi, poi_node(0, "", x, y, 0, False)) < shortestDistance):
                    shortestDistance = self.distanceBetweenPoi(poi, poi_node(0, "", x, y, 0, False))
                    shortestPoi = poi
        return shortestPoi

    def convertCoordsToPlayerPOI(self, coords: tuple) -> poi_node:
        if (type(coords) != tuple):
            raise TypeError("coords must be of type tuple, not " + str(type(coords)) + "!")
        if (len(coords) != 2):
            raise ValueError("coords must be of length 2")
        if (type(coords[0]) != int):
            raise TypeError("coords[0] must be of type int")
        if (type(coords[1]) != int):
            raise TypeError("coords[1] must be of type int")
        returnPoint = poi_node(0, "", coords[0], coords[1], 0, False)
        return returnPoint

    def findAllNearPoi(self, mainPoi: poi_node, distance: int) -> list:
        if (type(mainPoi) != poi_node):
            raise TypeError("poi must be of type poi_node")
        if (type(distance) != int):
            raise TypeError("distance must be of type int")
        nearPoi = []
        for poi in self.__poi_list:
            if (self.distanceBetweenPoi(mainPoi, poi) <= distance):
                nearPoi.append(poi)
        return nearPoi

    def avoidPlayers(self, start: poi_node, end: poi_node, playerLocations: list) -> list:
        if (type(start) != poi_node):
            raise TypeError("start must be of type poi_node")
        if (type(end) != poi_node):
            raise TypeError("end must be of type poi_node")
        if (type(playerLocations) != list):
            raise TypeError("playerLocations must be of type list")
        playerAvoidNodes = []
        for location in playerLocations:
            playerAvoidNodes.append(self.convertCoordsToPlayerPOI(location))
        nearestLocations = []
        for poi in playerAvoidNodes:
            nearestLocations.append(self.findAllNearPoi(poi, 250))
        print("Avoiding players at:")
        for poi in nearestLocations:
            for poi2 in poi:
                poi2.setAvoid(True)
                print("\t"+poi2.getName())
        start.setAvoid(False)
        end.setAvoid(False)
        try:
            path = self.findShortestPath(start, end)
        except AttributeError:
            print("No path found, trying again with a more risky path")
            for poi in nearestLocations:
                for poi2 in poi:
                    poi2.setAvoid(False)
                for poi in playerAvoidNodes:
                    nearestLocations.append(self.findAllNearPoi(poi, 125))
            print("Avoiding players at:")
            for poi in nearestLocations:
                for poi2 in poi:
                    poi2.setAvoid(True)
                    print("\t"+poi2.getName())
            start.setAvoid(False)
            end.setAvoid(False)
            try:
                path = self.findShortestPath(start, end)
            except AttributeError:
                print("Still no path found, even with a more risky path")
                exit()
        return path

    def __repr__(self):
        return str(self.__poi_list)

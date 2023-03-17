class poi_node:
    __slots__ = ['__poiID', '__poiName', '__x', '__y', '__radius', '__neighbors', '__isChoke']

    def __init__(self, poiID, poiName, x, y, radius, isChoke, neighbors=[]):
        self.__poiID = poiID
        self.__poiName = poiName
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__neighbors = []
        self.__isChoke = isChoke

    def addNeighbor(self, neighbor):
        if (type(neighbor) != poi_node):
            raise TypeError("neighbor must be of type poi_node")
        for n in self.__neighbors:
            if (n == neighbor):
                return
        for n in neighbor.getNeighbors():
            if (n == self):
                return
        self.__neighbors.append(neighbor)

    def getNeighbors(self):
        return self.__neighbors

    def getID(self):
        return self.__poiID

    def getName(self):
        return self.__poiName

    def getCoords(self):
        return self.__x, self.__y

    def getRadius(self):
        return self.__radius

    def __str__(self):
        return str(self.__poiID) + " " + str(self.__poiName) + " " + str(self.__x) + " " + str(self.__y) + " " + str(self.__radius)

    def __repr__(self):
        return str(self.__poiID) + " " + str(self.__poiName) + " " + str(self.__x) + " " + str(self.__y) + " " + str(self.__radius)

    def __eq__(self, other):
        return self.__poiID == other.__poiID

    def __hash__(self):
        return hash(self.__poiID)

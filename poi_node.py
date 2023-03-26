class poi:
    __slots__ = ['__poiID', '__poiName', '__x', '__y', '__radius', '__neighbors', '__isChoke', '__avoid']

    def __init__(self, poiID: int, poiName: str, x: int, y: int, radius: int, isChoke: bool, neighbors: list = []):
        self.__poiID = poiID
        self.__poiName = poiName
        self.__x = x
        self.__y = y
        self.__radius = radius
        self.__neighbors = []
        self.__isChoke = isChoke
        if self.__isChoke:
            self.__radius = 36
        self.__avoid = False

    def addAssociation(self, neighbor: 'poi') -> None:
        if (type(neighbor) != poi):
            raise TypeError("neighbor must be of type poi_node")
        if (neighbor not in self.__neighbors):
            self.__neighbors.append(neighbor)
        if (self not in neighbor.getAssociations()):
            neighbor.addAssociation(self)

    def getAssociations(self) -> list:
        returnNeighbors = []
        for neighbor in self.__neighbors:
            if (neighbor.getAvoid() == False):
                returnNeighbors.append(neighbor)
        return returnNeighbors

    def getAssociationNames(self) -> list:
        names = []
        for neighbor in self.__neighbors:
            names.append(neighbor.getName())
        return names

    def getAssociationIDs(self) -> list:
        ids = []
        for neighbor in self.__neighbors:
            ids.append(neighbor.getID())
        return ids

    def getID(self) -> int:
        return self.__poiID

    def getName(self) -> str:
        return self.__poiName

    def getCoords(self) -> tuple:
        return (self.__x, self.__y)

    def getX(self) -> int:
        return self.__x

    def getY(self) -> int:
        return self.__y

    def getRadius(self) -> int:
        return self.__radius

    def getChoke(self) -> bool:
        return self.__isChoke

    def setAvoid(self, avoid: bool) -> None:
        self.__avoid = avoid

    def getAvoid(self) -> bool:
        return self.__avoid

    def __str__(self) -> str:
        return "poiID: " + str(self.__poiID) + ", poiName: " + self.__poiName + ", x: " + str(self.__x) + ", y: " + str(self.__y) + ", radius: " + str(self.__radius) + ", isChoke: " + str(self.__isChoke)

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: 'poi') -> bool:
        try:
            return self.__poiID == other.getID() and self.__poiName == other.getName() and self.__x == other.getX()
        except AttributeError:
            print("Error with comparing poi objects, the errors are as follows:" +
                  self.__poiName + " and " + other.getName())
        return False

    def __hash__(self) -> int:
        return hash(self.__poiID)

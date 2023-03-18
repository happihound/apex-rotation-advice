from poi_node import poi as poi_node
import csv


class coordinator:
    __slots__ = ["__poi_list", "__poi_dict", "__poi_count", "__map"]

    def __init__(self):
        self.__map = ""
        self.__poi_list = []
        self.__poi_dict = {}
        self.__poi_count = 0

    def loadMap(self, mapName: str) -> None:
        if (type(mapName) != str):
            raise TypeError("mapName must be of type str")
        # Right now we only have WE, so we'll override the mapName
        # self.__map = mapName       #uncomment this line when we have more maps
        self.__map = "WE"
        self.__loadPoi("poi_" + self.__map + ".csv")

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

    def __repr__(self):
        return str(self.__poi_list)

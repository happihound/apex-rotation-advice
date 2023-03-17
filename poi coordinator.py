from poi_node import poi_node
import csv


class poi_coordinator:
    __slots__ = ["__poi_list", "__poi_dict", "__poi_count", "__map"]

    def __init__(self):
        self.__map = "WE"
        self.__poi_list = []
        self.__poi_dict = {}
        self.__poi_count = 0

    def loadMap(self, mapName):
        if (type(mapName) != str):
            raise TypeError("mapName must be of type str")
        self.__map = mapName
        self.__loadPoi("poi_" + mapName + ".csv")

    def __addPoi(self, poi):
        if (type(poi) != poi_node.poi_node):
            raise TypeError("poi must be of type poi_node")
        self.__poi_list.append(poi)
        self.__poi_dict[poi.getName()] = poi
        self.__poi_count += 1

    def __loadPoi(self, poiFile):
        poiFile = "game_map/nodes/" + poiFile
        with open(poiFile, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                poi = poi_node(row[0], row[1], row[2], row[3], row[4])
                next(reader)
                for neighbor in reader:
                    if (neighbor[0] == "END"):
                        break
                    poi.addNeighbor(neighbor)
                self.__addPoi(poi)

import pathlib
import unittest
from poi_node import poi as poi_node
from poi_coordinator import coordinator
import matplotlib.pyplot as plt
import numpy as np
import pytest
import csv
import sys


def test_makeCoordinator():
    myCoordinator = coordinator()
    assert myCoordinator is not None, "The coordinator object was not created"


def test_loadMap_WE():
    # Create a coordinator object
    myCoordinator = coordinator()
    # Load the map data for Worlds Edge
    myCoordinator.loadMap("WE")
    # Set up a counter for the number of points of interest in the map file
    poiCount = 0
    # Read the points of interest from the map file
    with open("game_map/nodes/poi_WE.csv") as file:
        next(file)
        csvFile = list(file)
        for line in csvFile:
            # Stop reading once we reach the associations
            if "ASSOCIATION" in line:
                break
            # Increment the counter for each point of interest
            poiCount += 1

    # Check that the number of points of interest in the map file matches the number of points of interest in the coordinator object
    assert myCoordinator.getNumberOfPoi(
    ) == poiCount, "The number of points of interest in the map file does not match the number of points of interest in the coordinator object"


def test_getPoiList():
    # Create a coordinator object
    myCoordinator = coordinator()
    # Load the map data for Worlds Edge
    myCoordinator.loadMap("WE")
    # Set up a list to hold the points of interest in the map file
    poiList = []
    # Read the points of interest from the map file
    with open("game_map/nodes/poi_WE.csv") as file:
        next(file)
        csvFile = list(file)
        for line in csvFile:
            # Stop reading once we reach the associations
            if "ASSOCIATION" in line:
                break
            # Add each point of interest to the list
            poiList.append(line.split(',')[1].strip())

    returnedPoiList = myCoordinator.getPoiListNames()
    # Check that the list of points of interest is at least one element long
    assert len(poiList) > 0, "The list of points of interest is empty"
    # Check that the lists are the same length
    assert len(poiList) == len(
        returnedPoiList), "The list of points of interest in the map file does not match the list of points of interest in the coordinator object"
    # Check that the list of points of interest in the map file matches the list of points of interest in the coordinator object
    for value in poiList:
        assert value in returnedPoiList, "The list of points of interest in the map file does not match the list of points of interest in the coordinator object, at " + value
    # Check that the first element of the list is a poi_node object
    poiList = myCoordinator.getPoiList()
    assert isinstance(
        poiList[0], poi_node), "The first element of the list of points of interest is not a poi_node object"


if __name__ == "__main__":
    import sys
    sys.path.append(path.join(path.dirname(__file__), '..'))

    test_makeCoordinator()
    test_loadMap_WE()
    test_getPoiList()

from poi_node import poi as poi_node
from poi_coordinator import coordinator

validMaps = ["WE"]


def test_makeCoordinator():
    myCoordinator = coordinator(validMaps=validMaps)
    assert myCoordinator is not None, "The coordinator object was not created"


def test_loadMap_WE():
    # Create a coordinator object
    myCoordinator = coordinator(validMaps=validMaps)
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
    myCoordinator = coordinator(validMaps=validMaps)
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


def test_getValidMapNames():
    # Create a coordinator object
    myCoordinator = coordinator(validMaps=validMaps)
    # Check that the list of valid maps is at least one element long
    assert len(validMaps) > 0, "The list of valid maps is empty"
    # Check that the list of valid maps in the coordinator object matches the list of valid maps in the coordinator object
    assert myCoordinator.getValidMapNames(
    ) == validMaps[0], "The list of valid maps in the coordinator object does not match the list of valid maps in the coordinator object"


def test_getPoiListNames():
    # Create a coordinator object
    myCoordinator = coordinator(validMaps=validMaps)
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


def test_getPoi():
    # Create a coordinator object
    myCoordinator = coordinator(validMaps=validMaps)
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

    # Check that the first element of the list is a poi_node object
    poiList = myCoordinator.getPoiList()
    assert poiList[0] == myCoordinator.getPoi(poiID=1)


def test_getNumberOfPoi():
    myCoordinator = coordinator(validMaps=validMaps)
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
            # Add each point of interest to the list
            poiCount += 1

    # Check that the number of points of interest in the map file matches the number of points of interest in the coordinator object
    assert myCoordinator.getNumberOfPoi(
    ) == poiCount, "The number of points of interest in the map file does not match the number of points of interest in the coordinator object"


def test_distanceBetweenPoi():
    myCoordinator = coordinator(validMaps=validMaps)
    myCoordinator.loadMap("WE")
    # Set up a counter for the number of points of interest in the map file
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
    testPoi1 = myCoordinator.getPoi(poiID=1)
    testPoi2 = myCoordinator.getPoi(poiID=2)
    testPoi3 = myCoordinator.getPoi(poiID=myCoordinator.getNumberOfPoi()-2)
    # Check that the distance between two points of interest is a positive number
    assert myCoordinator.distanceBetweenPoi(
        testPoi1, testPoi2) > 0, "The distance between two points of interest is not a positive number"
    assert myCoordinator.distanceBetweenPoi(
        testPoi1, testPoi3) < 6000, "The distance between two points of interest is not a positive number"


def test_findPoiFromLocation():
    # Create a coordinator object
    myCoordinator = coordinator(validMaps=validMaps)
    # Load a map into the coordinator object
    myCoordinator.loadMap("WE")
    # Get the poi node with id 10
    poi = myCoordinator.getPoi(poiID=10)
    # Get the poi node using the findPoiFromLocation function
    poiFromLoc = myCoordinator.findPoiFromLocation(2970, 760)
    # Assert that the poi node from the getPoi function is the same as the poi node from the findPoiFromLocation function
    assert (poi == poiFromLoc), "The findPoiFromLocation function does not return the correct poi_node object"


def test_convertCoordsToPoi():
    # Create a coordinator object and load the "WE" map
    myCoordinator = coordinator(validMaps=validMaps)
    myCoordinator.loadMap("WE")

    # Get the poi_node object that should be returned
    realPoi = myCoordinator.getPoi(poiID=10)

    # Get the poi_node object that is returned by the convertCoordsToPoi function
    testPoi = myCoordinator.convertCoordsToPoi((2970, 760))

    # Check if the returned poi_node object is close enough to the real poi_node object
    assert myCoordinator.distanceBetweenPoi(
        testPoi, realPoi) < 1, "The convertCoordsToPoi function does not return the correct poi_node object"


def test_findAllNearPoi():
    # Create a coordinator object
    myCoordinator = coordinator(validMaps=validMaps)
    # Load the WE map
    myCoordinator.loadMap("WE")
    # Get the poi with ID 10
    testPoi = myCoordinator.getPoi(poiID=10)
    # Find all poi_nodes near the poi
    testList = myCoordinator.findAllNearPoi(testPoi, 250)
    # Check that the length of the list is 2
    assert len(testList) == 2, "The findAllNearPoi function does not return the correct number of poi_node objects"


def test_poiListToNames():
    # Create a new instance of the MapCoordinator class, and assign it to the variable myCoordinator
    myCoordinator = coordinator(validMaps=validMaps)

    # Load the map named "WE" into myCoordinator
    myCoordinator.loadMap("WE")

    # Get the Poi object with ID 10 from myCoordinator
    testPoi1 = myCoordinator.getPoi(poiID=10)

    # Get the Poi object with ID 11 from myCoordinator
    testPoi2 = myCoordinator.getPoi(poiID=11)

    # Create a list of the two Poi objects
    testList = myCoordinator.poiListToNames([testPoi1, testPoi2])

    # Create a string containing the expected output
    expectedString = "Climatizer->East Skyhook Choke"

    # Assert that the output of the function matches the expected output
    assert testList == expectedString, "The poiListToNames function does not return the correct string"

import sys
from association import association
from findSafePath import findSafePath

validMaps = ["WE"]
debug = True


def main(args):
    # check if the user inputted any arguments
    if len(args) == 1:
        # if they didn't, raise an error
        raise Exception("Please enter a valid command.")
    # check if the user inputted too many arguments
    if len(args) > 4:
        # if they did, raise an error
        raise Exception("Too many arguments.")

    # initialize the selected map variable
    selectedMap = None
    # initialize the ratio variable
    ratio = None
    # initialize the association mode variable
    associationMode = None
    # initialize the valid map variable
    validMap = False
    # initialize the program mode variable
    programMode = args[1]

    # iterate through the arguments
    for arg in args:
        # strip the argument
        arg.strip()
        # lowercase the argument
        arg = arg.lower()
        # print the argument
        print("arg: ", arg)
        # check if the argument contains association
        if "association" in arg:
            # if it does, set the program mode to association
            programMode = "association"
        # check if the argument contains findsafepath
        elif "findsafepath" in arg:
            # if it does, set the program mode to findsafepath
            programMode = "findSafePath"
        # check if the argument contains mapname
        if "mapname=" in arg:
            # if it does, set the selected map to the argument
            selectedMap = arg[8:]
            # uppercase the selected map
            selectedMap = selectedMap.upper()
            # check if the selected map is in the list of valid maps
            if selectedMap in validMaps:
                # if it is, set the valid map to true
                validMap = True
        # check if the argument contains ratio
        if "ratio=" in arg:
            # if it does, set the ratio to the argument
            ratio = arg[6:]
        # check if the argument contains mode
        if "mode=" in arg:
            # if it does, set the association mode to the argument
            associationMode = arg[5:]
    # check if the program mode is not none
    assert programMode != None, "Please enter a valid command."
    # check if the valid map is false
    if validMap == False:
        # if it is, raise an error
        raise Exception(str("Please enter a valid map name, not " + str(selectedMap)))
    # check if the program mode is association
    if programMode == "association":
        # if it is, check if the association mode is none
        assert associationMode != None, "Please enter a valid association mode."
        # run the association function
        association(mode=associationMode, mapName=selectedMap, validMaps=getValidMaps())
    # check if the program mode is findsafepath
    elif programMode == "findSafePath":
        # run the findSafePath function
        findSafePath(mapName=selectedMap, validMaps=getValidMaps(), ratio=ratio)


def getValidMaps():
    return validMaps


if __name__ == "__main__" and debug == False:
    main(sys.argv)

import main


def test_main_validMaps():
    assert main.getValidMaps() == ["WE"]


def test_main_association_all():
    # 1. Run the main.py file with the association mapName and mode=all
    main.main(["main.py", "association", "mapName=WE", "mode=all"])
    # 2. Assert that the test is True
    assert True


def test_main_association_view():
    # Runs the main.py script with the association and view options
    main.main(["main.py", "association", "mapName=WE", "mode=view"])
    # Asserts that the script completed without errors
    assert True


def test_main_association_create():  # define a test function
    main.main(["main.py", "association", "mapName=WE", "mode=create"])  # call the main function with the arguments
    assert True  # assert that the main function did not raise any errors


def test_main_wrongMapName():
    # We expect an exception to be raised, so we put the test in a try-except block
    try:
        # Run the main function
        main.main(["main.py", "association", "mapName=WRONG", "mode=all"])
        # If no exception is raised, we fail the test
        assert False
    except Exception as e:
        # If an exception is raised, we check that it is the expected one
        assert str(e) == "Please enter a valid map name, not WRONG"


def test_main_noMapName():
    try:
        # Run the main function with an invalid map name
        main.main(["main.py", "association", "mode=all"])
        # If no exception is raised, fail the test
        assert False
    except Exception as e:
        # Check that the exception raised is the one we expect
        assert str(e) == "Please enter a valid map name, not None"


def test_main_noAssociationMode():
    try:
        # The following line will raise an exception because the
        # association mode is missing.
        main.main(["main.py", "association", "mapName=WE"])
        # If the above line did not raise an exception, then the
        # test failed.
        assert False
    except Exception as e:
        # If the above line raised an exception, verify that the
        # exception message is correct.
        assert str(e) == "Please enter a valid association mode."


def test_main_noProgramMode():
    # The main function should raise an exception if it is called with no command line arguments
    try:
        # Call the main function with no arguments
        main.main(["main.py"])
        # If the main function does not raise an exception, then the test fails
        assert False
    except Exception as e:
        # If the main function does raise an exception, then the test passes if the
        # exception message is the expected message
        assert str(e) == "Please enter a valid command. Type -h or help for more information."


def test_main_findSafePath():
    # This test will only work with a 16:10 aspect ratio image in the input folder, so we skip it
    return
    # Call the main function with the arguments as a list
    main.main(["main.py", "findSafePath", "mapName=WE", "ratio=16:10"])
    # Assert that the test passed
    assert True


def test_main_wrongRatio_findSafePath():
    try:
        # Call main.main() with the arguments: ["main.py", "findSafePath", "mapName=WE", "ratio=WRONG"]
        main.main(["main.py", "findSafePath", "mapName=WE", "ratio=WRONG"])
        # Fail the test if no exception is thrown
        assert False
    except Exception as e:
        # Assert that the exception message contains the string "Invalid aspect ratio. Valid ratios are"
        assert str(e).__contains__("Invalid aspect ratio. Valid ratios are")


def test_main_noRatio_findSafePath():
    # Call main.main with the arguments as a list
    main.main(["main.py", "findSafePath", "mapName=WE"])
    # Assert that the test passed
    assert True


def test_main_wrongProgramMode():
    # try to run the program with a wrong program mode
    try:
        main.main(["main.py", "WRONG", "mapName=WE"])
    # if an exception is raised, catch it
    except Exception as e:
        # check if the exception message is the expected one
        assert str(e) == "Please enter a valid command."

import cv2 as cv
from userMapImage import userMapImage
delay = 2000


def test_returnCropSize_16by10():
    # Set the image to test to the 16 by 10 test image
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # Create a userMapImage object from the test image and set the crop size to 16 by 10
    changedImage = userMapImage(cv2Image, "16by10")
    # Show the cropped image
    cv.imshow("16by10", changedImage.getCroppedImage().image())
    cv.waitKey(delay)
    cv.destroyAllWindows()


def test_returnCropSize_4by3():
    # Read in the image
    cv2Image = cv.imread("tests/test_images/4by3/test_image1_4by3.png")

    # Create a UserMapImage object with the image, and a string representing the image's aspect ratio
    changedImage = userMapImage(cv2Image, "4by3")

    # Show the image
    cv.imshow("4by3", changedImage.getCroppedImage().image())

    # Wait for the user to press any key to continue
    cv.waitKey(delay)

    # Close all windows
    cv.destroyAllWindows()


def test_returnCropSize_16by9():
    # Read the image from the specified path
    cv2Image = cv.imread("tests/test_images/16by9/test_image1_16by9.png")

    # Create the userMapImage object
    changedImage = userMapImage(cv2Image, "16by9")

    # Display the image
    cv.imshow("4by3", changedImage.getCroppedImage().image())
    cv.waitKey(delay)
    cv.destroyAllWindows()


def test_wrongApspectRatio():
    # Load test image
    cv2Image = cv.imread("tests/test_images/16by9/test_image1_16by9.png")
    # Attempt to create user map image
    try:
        userMapImage(cv2Image, "21by9")
    except ValueError:
        return
    # If no error is raised, raise a ValueError
    raise ValueError("21by9 ratio is not supported, but was not caught")


def test_detectAspectRatio():
    # Read the image from the file
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")

    # Apply the user-defined image mapping
    changedImage = userMapImage(cv2Image)

    # Display the result
    cv.imshow("16by10", changedImage.getCroppedImage().image())
    cv.waitKey(delay)
    cv.destroyAllWindows()


def test_findRedDots():
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # Create the userMapImage
    changedImage = userMapImage(cv2Image)
    # Show that the image is thresholded correctly
    cv.imshow("16by10", changedImage.getThresheldImage().image())
    cv.waitKey(delay)
    cv.destroyAllWindows()


def test_getTargets():
    # Given a sample image
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # When the image is converted to a userMapImage
    changedImage = userMapImage(cv2Image)
    # Then the image should have between 1 and 60 targets
    assert len(changedImage.getTargets()) > 0
    assert len(changedImage.getTargets()) < 60


def test_returnValidAspectRatios():
    # Load a test image
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # Initialize the class
    changedImage = userMapImage(cv2Image)
    # Test for valid ratio
    assert "16by10" in changedImage.getValidRatios()
    # Test for invalid ratio
    assert "21by9" not in changedImage.getValidRatios()

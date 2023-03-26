import cv2 as cv
from gameMapImage import gameMapImage
from pytest import approx


def test_return_ratio_16by10():
    # Load an image from the test_images folder
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # Create an instance of the gameMapImage class
    image = gameMapImage(cv2Image, "16by10")
    # Assert that the ratio function returns 16by10
    assert image.ratio() == "16by10", "Ratio should be 16by10"


def test_return_ratio_16by9():
    # Load the image to test
    cv2Image = cv.imread("tests/test_images/16by9/test_image1_16by9.png")
    # Create the gameMapImage object
    image = gameMapImage(cv2Image, "16by9")
    # Assert that the ratio is correct
    assert image.ratio() == "16by9", "Ratio should be 16by9"


def test_return_ratio_4by3():
    # Read image from file
    cv2Image = cv.imread("tests/test_images/4by3/test_image1_4by3.png")
    # Create a gameMapImage object from the image
    image = gameMapImage(cv2Image, "4by3")
    # Assert that the ratio is 4by3
    assert image.ratio() == "4by3", "Ratio should be 4by3"


def test_return_image_16by10():
    # Load test image
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # Create a gameMapImage object
    image = gameMapImage(cv2Image, "16by10")
    # Assert that the image() method returns the same image as the original
    assert image.image() is cv2Image, "Image should be the same"


def test_return_image_16by9():
    # Load image
    cv2Image = cv.imread("tests/test_images/16by9/test_image1_16by9.png")
    # Create game map image
    image = gameMapImage(cv2Image, "16by9")
    # Assert that the image returned is the same as the original image
    assert image.image() is cv2Image, "Image should be the same"


def test_return_image_4by3():
    # Read in the image
    cv2Image = cv.imread("tests/test_images/4by3/test_image1_4by3.png")
    # Create a gameMapImage object
    image = gameMapImage(cv2Image, "4by3")
    # Check that the image is the same as the one we read in
    assert image.image() is cv2Image, "Image should be the same"


def test_copy_16by10():
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # Load the image
    image = gameMapImage(cv2Image, "16by10")
    # Create a copy of the image
    assert image.copy().image() is not cv2Image, "Image should be a copy"
    # Image should be a copy
    assert image.copy().image() == approx(cv2Image), "Image should be a copy"
    assert image.copy().ratio() == "16by10", "Ratio should be 16by10"
    # Ratio should be 16by10


def test_shape():
    # This is the test image we will be using
    cv2Image = cv.imread("tests/test_images/16by10/test_image1_16by10.png")
    # Create a gameMapImage object
    image1 = gameMapImage(cv2Image, "16by10")
    # Check that the shape of the image is as expected
    assert image1.shape() == (1050, 1680, 3), "Shape should be (1080, 1920, 3)"

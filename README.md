# apex-rotation-advice

A short description of what your project does and what problem it solves.

## Table of Contents

- [apex-rotation-advice](#apex-rotation-advice)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
  - [Usage](#usage)
    - [Examples](#examples)
  - [Running the Tests](#running-the-tests)
  - [Built With](#built-with)
  - [Roadmap](#roadmap)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
 

### Installation

Step 1: Clone the repo
```bash
    git clone https://github.com/happihound/apex-rotation-advice.git
```
Step 2: Navigate to the project directory
```bash
    cd apex-rotation-advice
```
Step 3: Install dependencies
```bash
    pip install -r requirements.txt
```
Step 4: Run the project
```bash
    python main.py
```

## Usage
This utility accepts the following command line arguments:

To see all valid command line arguments:
```bash
    main.py -h
```
To start the association viewer utlity:
```bash
    main.py association -mapName= -mode=
```
To start the safe path viewer utility:
```bash
    main.py findSafePath -mapName= -ratio= 
```
The ratio argument is the ratio of the screenshot placed in the inputScanner folder. 

If not ratio is given, the program will attempt to find the ratio, this is not always accurate, so it is recommended to provide the ratio.
### Examples

Provide some examples of how your project can be used. Include code snippets, screenshots, or even GIFs to illustrate the functionality.

Viewing all association data for World's Edge:
```bash
    python main.py association -mapName=WE -mode=all
```
Finding a safe path between two poi's on worlds edge from a 16:9 aspect ratio screenshot:
```bash
    python main.py findSafePath -mapName=WE -ratio=16:9
```

## Running the Tests

If you'd like to run the tests, you can do so by running the following command:
```bash
    python runTests.py
```

## Built With

* [Opencv](https://opencv.org/) - The primary framework or library used
* [Numpy](https://numpy.org/) - The secondary framework or library used
* [matplotlib](https://matplotlib.org/) - The tertiary framework or library used


## Roadmap

    1. Convert the image to convert to 1:1 aspect ratio and then to 800x800 pixels - Done
    2. Take the input image and do threshholding on it to highlight enemy markers- Done
    3. If the markers are close enough, group them together and find the center of the group - Done
    4. Draw a minimum convex hull around the center of the group - Done
    5. Find the center of the hull - Done
    6. Create a node based graph of the map - Done
    7. Plot safest path between two points - Done
    8. Publish the project to github - Done

## License

This project is not to be used for commercial purposes or any other purpose other than personal use.
Credit must be given to the original author of this project if it is used in any other project.
It may not be used in any project that is not open source.

## Acknowledgments

* Thanks to wattson_x for assisting with the labeling of the map, without his help this project would not have been possible.
* Thanks to the Apex Legends community for providing the data used in this project. 
* Thanks to KeanuJ for the inspiration for this project.
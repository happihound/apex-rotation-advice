# apex-rotation-advice

A python program to compute the safest path between two locations in apex legends

## Table of Contents

- [apex-rotation-advice](#apex-rotation-advice)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Examples:](#examples)
    - [Example 1:](#example-1)
    - [Example 2:](#example-2)
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
In order to to use the utility, you must first scan a beacon in game.
1. While the map still shows all the location of all enemies, take a screenshot
2. Place the screenshot in the inputScan folder.
3. Run the program with the mapName argument set to the name of the map you are playing on.
4. If you are using the safe path viewer, you should also provide the ratio argument.
   

The program will then attempt to find the location of all enemies, and the safest path between all selected poi's while avoiding all enemies.

Note:
The ratio argument is the ratio of the screenshot placed in the inputScan folder. 

If no ratio is given, the program will attempt to find the ratio, this is not always accurate, so it is recommended to provide the ratio.

## Examples:

### Example 1:
Viewing all association data for World's Edge:
```bash
    python main.py association -mapName=WE -mode=all
```
![view_all_association_data](githubImages/view_all.png)


### Example 2:


Example input screenshot
![input_screenshot](githubImages/input_screenshot.png)

Finding a safe path between two poi's on worlds edge from the 16:10 aspect ratio screenshot:
```bash
    python main.py findSafePath -mapName=WE -ratio=16:10
```
Running the above command will open this window in which you can select the poi's you want to find a safe path between. 


![pick_poi_to_visit](githubImages/pick_poi_to_visit.png)

The number of pois you can select is not limited, and they will be connected in the order you select them


![skyhook_and_lava_selected](githubImages/skyhook_lava_selected.png)

Example of Lava and Skyhook selected:


![safe_path_found](githubImages/safe_path.png)


Example result of the safe path between the two poi's


## Running the Tests

If you'd like to run the tests, you can do so by running the following command:
```bash
    python run_tests.py
```

## Built With

* [Opencv](https://opencv.org/)
* [Numpy](https://numpy.org/)
* [matplotlib](https://matplotlib.org/)


## Roadmap

    1. Convert the image to convert to 1:1 aspect ratio and then to 800x800 pixels - Done
    2. Take the input image and do threshholding on it to highlight enemy markers- Done
    3. If the markers are close enough, group them together and find the center of the group - Done
    4. Draw a minimum convex hull around the center of the group - Done
    5. Find the center of the hull - Done
    6. Create a node based graph of the map - Done
    7. Plot safest path between two points - Done
    8. Publish the project to github - Done
    9. Add more maps - To be done
    10. Add the ability to predict ring movement - To be done

    Have an idea? Feel free to open an issue or pull request and I'll look into it!

## License

This project is not to be used for commercial purposes or any other purpose other than personal use.
Credit must be given to the original author of this project if it is used in any other project.
It may not be used in any project that is not open source.

## Acknowledgments

* Thanks to wattson_x for assisting with the labeling of the map, without his help this project would not have been possible.
* Thanks to the Apex Legends community for providing the data used in this project. 
* Thanks to KeanuJ for the inspiration for this project.
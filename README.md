# FLL Game Field Pathfinding Algorithm

This program allows the use to create a basic "maze" based on an image of an FLL game field. The user has the option to adjust the pathfinding settings based on their robot size. The program iterates through each mission location and generates an optimal path for each. This is then converted into a set of instructions that the robot can interpret.

## Usage

Running the program will open a pygame window that acts as the GUI. A grid is formed on the screen to represent units on the field. Pressing space will start the calculations. The end results of the algorithm is stored in a json file. 

### Node Colour Key
- White: empty tile
- Black: wall/barrier tile
- Orange: mission location (*target location*)
- Green: tiles to-be-checked (*during algorithm*)
- Red: tile already checked (*during algorithm*)

### Inputs
- Left click to place barrier tile
- Right click to remove barrier tile
- Lshift click to place mission location

## Algorithm

The program uses the a* pathfinding algorithm which is a commonly used algorithm in applications such as navigation software and video game NPC navigation. 

## Requirements

- LEGO® Spike Prime Hub running [pybricks](https://pybricks.com/) firmware
- Python version at least 3.x.x
- Python [pygame](https://github.com/pygame/pygame) library
- Pybricks python library
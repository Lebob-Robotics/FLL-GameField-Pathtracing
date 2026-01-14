A visual implementation of the A* pathfinding algorithm using Python's pygame module.

**Tile colour key:******

Orange - start
Turqoise - end
Black - barrier
White - none
Green - open
Red - closed
Purple - path


**Instructions:******

Clicking while there is no start or end on the grid will place respective tiles at the mouse pointer.
Subsequent clicks will place barrier tiles and right clicking a tile will remove it.

Pressing space will begin the algorithm.
The frames slider can be used during a search to set the algorithm speed. (0 is fastest possible)


**Notes:******

The algorithm considers diagonal tiles valid successors for a path and takes into consideration the weighting. 

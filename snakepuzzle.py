"""
This finds working configurations for pieces of the the wooden snake puzzle
and solves their arrangement.

Pseudocode:
Start with a pile of pieces (two ends, some corners, some straights), and an
empty volume (a 3x3 cube).

Take an end ends and put it (not facing an outside) in the cube.
If that finished filling the cube, we're done.
	Yield the current sequence.
	Back up and try it in the next orientation.
If that didn't finish filling the cube,
	if it doesn't connect to another open spot,
		back up and try it in the next orientation.
	else it does connect to another spot, so
		pick another piece and put it (connected) in that spot.
Try another location/piece matching:
	if we were dealing with initial end piece,
		put it in the next spot.
	elif it was some subsequent piece,
		if there's another kind we haven't tried,
			pick another kind and put it (connected) in that spot.
		else we've tried all the possibilities, there,
			so back up and (in the previous spot)
			try another location/piece matching there.
"""

import Cube, End, Corner, Straight

cube = Cube()

allEnds = []
allCorners = []
allStraights = []

NUM_ENDS = 2
NUM_CORNERS = 15
NUM_STRAIGHTS = 

for i in xrange(NUM_ENDS):
	allEnds.append(End())
for i in xrange(NUM_CORNERS):
	allCorners.append(Corner())
for i in xrange(NUM_STRAIGHTS):
	allStraights.append(Straight())

def IsComplete(volume, ends, corners, straights):
	return volume.isFilled() and not any(ends, corners, straights)

def AddPiece(nextPiece, coord, volume, ends, corners, straights):
	if not volume.isOpen(coord):
		return
	volume.addPiece(nextPiece, coord)

startPiece = allEnds.pop()
for coord in cube.getCoordinates():
	sequences = AddPiece(startPiece, coord, cube,
		allEnds, allCorners, allStraights)
	for sequence in sequences:
		print sequence


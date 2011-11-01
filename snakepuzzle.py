"""
This finds working configurations for pieces of the the wooden snake puzzle
and solves their arrangement.
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


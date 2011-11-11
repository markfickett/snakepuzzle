"""
This finds working configurations for pieces of the the wooden snake puzzle
and solves their arrangement.


Pseudocode:

Start with a pile of pieces (two ends, 16 corners, 9 straights), and an
empty volume (a 3x3 cube).

Take an end ends and put it the cube.
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


The goals of this implementation are understandability, correctness; and
flexability, for example in solving arbitrary volumes or introducing new types
of pieces such as a Y. Notably, it is not very fast.

For more analysis, see http://www.jaapsch.net/puzzles/snakecube.htm and others.
"""


from Direction import Direction, GetOpposite
from Piece import Piece
from End import End
from Corner import Corner
from Straight import Straight
from CubeThreeByThree import CubeThreeByThree


volume = CubeThreeByThree()
NUM_ENDS = 2
NUM_CORNERS = 16
NUM_STRAIGHTS = volume.getNumLocations() - (NUM_ENDS + NUM_CORNERS)
ends =		[End()		for i in xrange(NUM_ENDS)	]
corners =	[Corner()	for i in xrange(NUM_CORNERS)	]
straights =	[Straight()	for i in xrange(NUM_STRAIGHTS)	]


def PlacePieceAndSearch(volume, prevPiece, piece, location,
		ends, corners, straights):
	if not volume.isAvailable(location):
		return
	volume.takeLocation(location)
	piece.location = location
	if prevPiece is not None:
		piece.faceFrom = GetOpposite(prevPiece.faceTo)
		prevPiece.next = piece
	if volume.isFilled():
		yield volume.getSolution()
	else:
		for faceTo in piece.getFaceToPossibilities():
			piece.faceTo = faceTo
			for solution in TryMorePieces(volume, piece,
					ends, corners, straights):
				yield solution
	volume.releaseLocation(location)
	if prevPiece is not None:
		prevPiece.next = None


def TryMorePieces(volume, piece, ends, corners, straights):
	if not any([ends, corners, straights]):
		raise RuntimeError('Need to try more pieces, but none left!')
	nextLocation = CalculateNextLocation(piece)
	if corners:
		nextCorner = corners.pop()
		for solution in PlacePieceAndSearch(
				volume, piece, nextCorner, nextLocation,
				ends, corners, straights):
			yield solution
		corners.append(nextCorner)
	if straights:
		nextStraight = straights.pop()
		for solution in PlacePieceAndSearch(
				volume, piece, nextStraight, nextLocation,
				ends, corners, straights):
			yield solution
		straights.append(nextStraight)
	if not any([corners, straights]):
		finalEnd = ends.pop()
		for solution in PlacePieceAndSearch(
				volume, piece, finalEnd, nextLocation,
				ends, corners, straights):
			yield solution
		ends.append(finalEnd)


def CalculateNextLocation(piece):
	"""
	X right, Y up, Z front
	"""
	location = piece.location
	if location is None:
		raise RuntimeError(
			'Cannot get next location, piece has no location.')
	if piece.faceTo is None:
		raise RuntimeError(
			'Cannot get next location, piece has no faceTo.')
	x, y, z = location

	if piece.faceTo == Direction.down:
		return (x, y-1, z)
	elif piece.faceTo == Direction.up:
		return (x, y+1, z)
	elif piece.faceTo == Direction.left:
		return (x-1, y, z)
	elif piece.faceTo == Direction.right:
		return (x+1, y, z)
	elif piece.faceTo == Direction.back:
		return (x, y, z-1)
	else:
		return (x, y, z+1)


if __name__ == '__main__':
	firstEnd = ends.pop()
	volume.first = firstEnd
	for location in volume.getUniqueStartingLocations():
		for solution in PlacePieceAndSearch(
				volume, None, firstEnd, location,
				ends, corners, straights):
			print solution



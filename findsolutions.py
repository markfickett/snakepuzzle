"""
This finds working configurations for pieces of the the wooden snake puzzle
and solves their arrangement. (See README for elaboration.)
"""


from direction import Direction, GetOpposite
from pieces import Piece, End, Corner, Straight
from volumes import VolumeFromFile


NUM_ENDS = 2


def PlacePieceAndSearch(volume, prevPiece, piece, location,
		ends, corners, straights):
	"""Places a Piece in the next location in the Volume, continues searching.

	Yields:
		Configurations of connected Pieces which fill the Volume, as lists of Piece
		objects.
	"""
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


def FindSolutions(volume, numCorners):
	numStraights = volume.getNumLocations() - (NUM_ENDS + numCorners)
	if numStraights < 0:
		raise RuntimeError(
				'Volume %s has only %d locations, but requested %d corners.'
				% (volume.name, volume.getNumLocations(), numCorners))
	ends = [End() for i in xrange(NUM_ENDS)]
	corners = [Corner() for i in xrange(numCorners)]
	straights = [Straight() for i in xrange(numStraights)]

	firstEnd = ends.pop()
	volume.first = firstEnd
	for location in volume.getUniqueStartingLocations():
		for solution in PlacePieceAndSearch(
				volume, None, firstEnd, location,
				ends, corners, straights):
			yield solution


if __name__ == '__main__':
	for solution in FindSolutions(VolumeFromFile('volumefiles/minsquare.txt'), 2):
		print ', '.join(str(piece) for piece in solution)
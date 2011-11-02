"""
This finds working configurations for pieces of the the wooden snake puzzle
and solves their arrangement.


Pseudocode:

Start with a pile of pieces (two ends, 16 corners, 9 straights), and an
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


from enum import Enum


Direction = Enum('down', 'up', 'left', 'right', 'front', 'back')


def GetOpposite(direction):
	pairIndex = direction.index
	inPairIndex = (1, 0)[direction.index % 2]
	return Direction[2*(pairIndex/2) + inPairIndex]


class Piece():
	def __init__(self):
		self.faceFrom = None
		self.faceTo = None
		self.location = None
		self.next = None

	def __str__(self):
		return '%s %s %s' % (self.LETTER, self.faceTo, self.location)

class End(Piece):
	LETTER = 'E'
	def getFaceToPossibilities(self):
		if self.faceFrom is not None:
			raise RuntimeError('End has a faceFrom, cannot faceTo.')
		return list(Direction)


class Corner(Piece):
	LETTER = 'C'
	def getFaceToPossibilities(self):
		faceTos = set(Direction)
		faceTos.remove(self.faceFrom)
		faceTos.remove(GetOpposite(self.faceFrom))
		return list(faceTos)


class Straight(Piece):
	LETTER = 'S'
	def getFaceToPossibilities(self):
		return [GetOpposite(self.faceFrom)]


class Volume:
	def __init__(self):
		self.start = None
		self._availables = {}
		self._generateAvailables()

	def _generateAvailables(self):
		raise NotImplementedError()

	def getNumLocations(self):
		return len(self._availables)

	def getUniqueStartingLocations(self):
		raise NotImplementedError()

	def isAvailable(self, location):
		return self._availables.get(location, False)

	def takeLocation(self, location):
		if not self.isAvailable(location):
			raise RuntimeError(
				'Location not available to be taken: %s.'
				% location)
		self._availables[location] = False

	def releaseLocation(self, location):
		status = self._availables.get(location)
		if status is None:
			raise RuntimeError(
				'Location not in volume to be released: %s.'
				% location)
		elif status == True:
			raise RuntimeError(
				'Location not taken to be released: %s.'
				% location)
		self._availables[location] = True

	def isFilled(self):
		# TODO easy optimization waiting
		return not any(self._availables.values())

	def getSolution(self):
		if not self.isFilled():
			raise RuntimeError(
				'Volume not filled! No present solution.')
		piece = self.first
		strPieces = []
		while piece:
			strPieces.append(str(piece))
			piece = piece.next
		return ', '.join(strPieces)


class Cube(Volume):
	def _generateAvailables(self):
		for i in xrange(3):
			for j in xrange(3):
				for k in xrange(3):
					self._availables[(i,j,k)] = True

	def getUniqueStartingLocations(self):
		return (
			(0, 0, 0),	# a corner
			#(1, 0, 0),	# a middle of an edge (impossible)
			(1, 1, 0),	# a middle of a face
			#(1, 1, 1),	# the middle of the cube (impossible)
		)


class MinSquare(Volume):
	def _generateAvailables(self):
		k = 0
		for i in xrange(2):
			for j in xrange(2):
				self._availables[(i,j,k)] = True

	def getUniqueStartingLocations(self):
		return (
			(0, 0, 0),	# a corner
		)


volume = Cube()
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



"""Finds all snake puzzle piece orderings and their folding patterns.

This tries all possible sequences of pieces (small cubes; with two End pieces
and any mix of Straight and Corner pieces), and tries to fold them to fill a
volume (such as the canonical snake puzzle, which forms a 3x3x3 cube).

See README for elaboration.
"""

import argparse

from direction import Direction, GetOpposite
from pieces import Piece, End, Corner, Straight
from volumes import VolumeFromFile


def PlacePieceAndSearch(volume, prevPiece, piece, location, sequence):
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
			for solution in TryMorePieces(volume, piece, sequence):
				yield solution
	volume.releaseLocation(location)
	if prevPiece is not None:
		prevPiece.next = None


def TryMorePieces(volume, piece, sequence):
	if not sequence:
		raise RuntimeError('Need to try more pieces, but none left!')
	nextLocation = CalculateNextLocation(piece)
	nextPiece = sequence.pop()
	for solution in PlacePieceAndSearch(
			volume, piece, nextPiece, nextLocation, sequence):
		yield solution
	sequence.append(nextPiece)


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


def FindSolutions(volume, sequence):
	if len(sequence) != volume.getNumLocations():
		raise RuntimeError(
				'Volume %s has %d locations, cannot fit sequence with %d pieces.'
				% (volume.name, volume.getNumLocations(), len(sequence)))

	firstEnd = sequence.pop()
	volume.first = firstEnd
	for location in volume.getUniqueStartingLocations():
		for solution in PlacePieceAndSearch(
				volume, None, firstEnd, location, sequence):
			yield solution
	sequence.append(firstEnd)


def TrySequences(volume, partialSequence):
	n = len(partialSequence)
	if n == volume.getNumLocations():
		for solution in FindSolutions(volume, partialSequence):
			yield solution
		return

	if n == 0 or n == volume.getNumLocations() - 1:
		nextPieces = [End()]
	else:
		nextPieces = [Corner(), Straight()]
	for nextPiece in nextPieces:
		partialSequence.append(nextPiece)
		for solution in TrySequences(volume, partialSequence):
			yield solution
		partialSequence.pop()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('volumefile')
	args = parser.parse_args()

	volume = VolumeFromFile(args.volumefile)
	if volume.getNumLocations() < 2:
		raise RuntimeError(
				')o: %s has only %d locations!', volume.name, volume.getNumLocations())

	print 'Searching for all the solutions.'
	numSolutions = 0
	for solution in TrySequences(volume, []):
		numSolutions += 1
		print ', '.join(str(piece) for piece in solution)
	print 'found %d solutions for %s' % (numSolutions, volume.name)

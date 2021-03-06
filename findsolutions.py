"""Finds all snake puzzle piece orderings and their folding patterns.

This tries all possible sequences of pieces (small cubes; with two End pieces
and any mix of Straight and Corner pieces), and tries to fold them to fill a
volume (such as the canonical snake puzzle, which forms a 3x3x3 cube).

See README for elaboration.
"""

import argparse
import multiprocessing

from direction import Direction, GetOpposite
from pieces import Piece, End, Corner, Straight
from pieces import FormatSolution, FormatSequence
from volumes import VolumeFromFile


def FindSolutions(volume, sequence):
	"""Finds all ways the sequence of Pieces can be folded in the volume.

	This uses multiple processes. It uses a pool with as many processes as
	available CPUs, and will run one process to explore from each starting
	location in the volume. (If the volume has fewer starting locations than there
	are available CPUs, computing will be underutilized.)

	Args:
		volume: Constraining volume to occupy.
		sequence: A list of Pieces, representing a connected chain to fold.
	"""
	if len(sequence) != volume.getNumLocations():
		raise RuntimeError(
				'Volume %s has %d locations, cannot fit sequence with %d pieces.'
				% (volume.name, volume.getNumLocations(), len(sequence)))

	solutions = multiprocessing.Queue()
	searcherPool = multiprocessing.Pool(None, _SearchProcessInit, (solutions,))
	result = searcherPool.map_async(
		_SearchProcess,
		[(volume, sequence, loc) for loc in volume.getUniqueStartingLocations()])
	searcherPool.close()

	while not result.ready():
		if not solutions.empty():
			yield solutions.get()
	searcherPool.join()
	while not solutions.empty():
		yield solutions.get()


def _SearchProcessInit(solutions):
	"""Initializes a _SearchProcess with the queue to put solutions in."""
	_SearchProcess.solutions = solutions


def _SearchProcess((volume, sequence, startLocation)):
	"""Searches for solutions from one starting location."""
	firstEnd = sequence.pop()
	volume.first = firstEnd
	for solution in _PlacePieceAndSearch(
			volume, None, firstEnd, startLocation, sequence):
		_SearchProcess.solutions.put(solution)


def _PlacePieceAndSearch(volume, prevPiece, piece, location, sequence):
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
			for solution in _TryMorePieces(volume, piece, sequence):
				yield solution
	volume.releaseLocation(location)
	if prevPiece is not None:
		prevPiece.next = None


def _TryMorePieces(volume, piece, sequence):
	if not sequence:
		raise RuntimeError('Need to try more pieces, but none left!')
	nextLocation = _CalculateNextLocation(piece)
	nextPiece = sequence.pop()
	for solution in _PlacePieceAndSearch(
			volume, piece, nextPiece, nextLocation, sequence):
		yield solution
	sequence.append(nextPiece)


def _CalculateNextLocation(piece):
	"""
	Given the location and orientation of the given piece, determines where to
	place the next piece attached to it.

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


def _TrySequences(volume, partialSequence, tried):
	"""
	Recursively builds up all possible sequences of Straights and Corners and
	finds folding solutions for them.
	"""
	n = len(partialSequence)
	if n == volume.getNumLocations():
		seqStr = FormatSequence(partialSequence)
		if seqStr in tried or seqStr[::-1] in tried:
			return
		else:
			tried.add(seqStr)
		for solution in FindSolutions(volume, partialSequence):
			yield partialSequence, solution
		return

	if n == 0 or n == volume.getNumLocations() - 1:
		nextPieces = [End()]
	else:
		nextPieces = [Corner(), Straight()]
	for nextPiece in nextPieces:
		partialSequence.append(nextPiece)
		for sequence, solution in _TrySequences(volume, partialSequence, tried):
			yield partialSequence, solution
		partialSequence.pop()


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('volumefile')
	args = parser.parse_args()

	volume = VolumeFromFile(args.volumefile)
	if volume.getNumLocations() < 2:
		raise RuntimeError(
				')o: %s has only %d locations!', volume.name, volume.getNumLocations())

	print 'Searching for all the solutions.'
	numSolutions = 0
	lastSeq = None
	tried = set()
	for sequence, solution in _TrySequences(volume, [], tried):
		numSolutions += 1
		formattedSeq = FormatSequence(sequence)
		if lastSeq != formattedSeq:
			print formattedSeq
			lastSeq = formattedSeq
		print '  ', FormatSolution(solution)
	print (
			'found %d solutions for %s (tried %d sequences)'
			% (numSolutions, volume.name, len(tried)))

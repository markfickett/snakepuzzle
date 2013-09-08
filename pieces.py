from Direction import Direction
from Direction import GetOpposite


__all__ = [
	'Corner',
	'End',
	'Piece',
	'Straight',
]


class Piece():
	"""
	Abstract base for the cube pieces of the puzzle. Each piece has two
	holes, through which the string connects. One faces faceFrom, which
	determines what directions the other can face: faceTo. (For ends,
	one of faceTo and faceFrom will be None.)
	"""
	def __init__(self):
		self.faceFrom = None
		self.faceTo = None
		self.location = None
		self.next = None

	def __str__(self):
		return '%s %s %s' % (self.LETTER, self.faceTo, self.location)

	def getFaceToPossibilities(self):
		"""
		Based on the current faceFrom (and the type of Piece), what
		are the valid possibilities for faceTo? That is, given the way
		this Piece is connected to the one before it, how can it turn?
		"""
		raise NotImplementedError()


class End(Piece):
	LETTER = 'E'
	def getFaceToPossibilities(self):
		if self.faceFrom is not None:
			raise RuntimeError('End has a faceFrom, cannot faceTo.')
		return list(Direction)


class Straight(Piece):
	LETTER = 'S'
	def getFaceToPossibilities(self):
		return [GetOpposite(self.faceFrom)]


class Corner(Piece):
	LETTER = 'C'
	def getFaceToPossibilities(self):
		faceTos = set(Direction)
		faceTos.remove(self.faceFrom)
		faceTos.remove(GetOpposite(self.faceFrom))
		return list(faceTos)
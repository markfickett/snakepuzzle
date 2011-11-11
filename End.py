from Piece import Piece
from Direction import Direction

__all__ = [
	'End',
]

class End(Piece):
	LETTER = 'E'
	def getFaceToPossibilities(self):
		if self.faceFrom is not None:
			raise RuntimeError('End has a faceFrom, cannot faceTo.')
		return list(Direction)


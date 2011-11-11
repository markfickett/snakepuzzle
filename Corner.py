from Piece import Piece
from Direction import Direction, GetOpposite

__all__ = [
	'Corner',
]

class Corner(Piece):
	LETTER = 'C'
	def getFaceToPossibilities(self):
		faceTos = set(Direction)
		faceTos.remove(self.faceFrom)
		faceTos.remove(GetOpposite(self.faceFrom))
		return list(faceTos)


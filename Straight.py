from Piece import Piece
from Direction import GetOpposite

__all__ = [
	'Straight',
]

class Straight(Piece):
	LETTER = 'S'
	def getFaceToPossibilities(self):
		return [GetOpposite(self.faceFrom)]


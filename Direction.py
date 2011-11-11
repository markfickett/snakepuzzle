"""
Enumerate directions in 3-space, and calculate their opposites.
"""

__all__ = [
	'Direction',
	'GetOpposite',
]

try:
	from enum import Enum
except ImportError, e:
	print 'Get enum (one file) from: http://pypi.python.org/pypi/enum/0.4.3'
	raise e


Direction = Enum('down', 'up', 'left', 'right', 'front', 'back')


def GetOpposite(direction):
	pairIndex = direction.index
	inPairIndex = (1, 0)[direction.index % 2]
	return Direction[2*(pairIndex/2) + inPairIndex]


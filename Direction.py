"""
Enumerate directions in 3-space, and calculate their opposites.
"""

__all__ = [
	'Direction',
	'GetOpposite',
]

from enum import Enum


Direction = Enum('down', 'up', 'left', 'right', 'front', 'back')


def GetOpposite(direction):
	pairIndex = direction.index
	inPairIndex = (1, 0)[direction.index % 2]
	return Direction[2*(pairIndex/2) + inPairIndex]


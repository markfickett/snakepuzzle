"""Finds a way to connect cubes so, attached, they can be folded into a volume.

This is for a variation on the snake puzzle. In the snake puzzle, to solve the
puzzle the cubes are folded into a larger cube, 3 units on a side. For this
variation, the cubes may be folded into one or several volumes (such as an arch,
a toroid, etc).

Usage:
	findfoldings [sequence] [volume definition, ...]

Example:
	cube2.txt contains
		eo
		oo

		oo
		oo
	rect2x4.txt contains
		eeoo
		oooo

	Running the program as
		findfoldings ECCCCCCE volumefiles/cube2.txt volumefiles/rect2x4.txt
	prints the foldings that could satisfy both puzzles, like
		URDFULD
		URDFLUR
		...
		FRBUFLB
		cube2: 18

		URDRURD
		rect2x4: 1

Volume Files: Layers of the volume are separated by a newline. Cubes are
represented by "e" or "o", where "e" are the starting locations to try (that is,
the places at which to place one end of the chain).

Sequence: The order of the pices, given by single-letter abbreviations (End,
Corner, and Straight).

Output: The output is any number of solutions for each volume, as:
 * a line for each way to fold the sequence to satisfy the volume,
 * the name of the file which defined the volume (without the extension), and
 * the number of different foldings.
"""

import argparse

from findsolutions import FindSolutions
from volumes import VolumeFromFile
import pieces


_LETTER_TO_CLS = dict(
		(cls.LETTER, cls) for cls in (pieces.End, pieces.Corner, pieces.Straight))


def _FormatPiece(piece):
	if piece.faceTo:
		return str(piece.faceTo)[0].upper()
	else:
		return ''


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('sequence')
	parser.add_argument('volumefile', nargs='+')

	args = parser.parse_args()

	volumes = [VolumeFromFile(volumefile) for volumefile in args.volumefile]
	sequence = [_LETTER_TO_CLS[letter]() for letter in args.sequence]

	for volume in volumes:
		numSolutions = 0
		for solution in FindSolutions(volume, sequence):
			numSolutions += 1
			print ''.join(_FormatPiece(piece) for piece in solution)
		print '%s: %d\n' % (volume.name, numSolutions)

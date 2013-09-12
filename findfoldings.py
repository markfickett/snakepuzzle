"""Finds a way to connect cubes so, attached, they can be folded into a volume.

This is for a variation on the snake puzzle. In the snake puzzle, to solve the
puzzle the cubes are folded into a larger cube, 3 units on a side. For this
variation, the cubes may be folded into one or several volumes (such as an arch,
a toroid, etc).

Usage:
	findwalks [sequence] [volume definition, ...]

Example:
	cube.txt contains
		eo
		oo

		oo
		oo
	rect.txt contains
		eeoo
		oooo

	Running the program as
		findwalks ECCCCCCE cube.txt rect.txt
	prints the foldings that could satisfy both puzzles, like
		cube 1
		ORDLFURD
		rect 1
		ODRURDRU
		...

Volume Files: Layers of the volume are separated by a newline. Cubes are
represented by "e" or "o", where "e" are the starting locations to try (that is,
the places at which to place one end of the chain).

Sequence: The order of the pices, given by single-letter abbreviations (End,
Corner, and Straight).

Output: The output is any number of solutions for each volume, as:
 * the name of the file which defined the volume (without the extension),
 * the number of different foldings, and
 * a line for each way to fold the sequence to satisfy the volume.
"""

if __name__ == '__main__':
	raise NotImplementedError()

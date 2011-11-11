Snake Puzzle
============

This finds working configurations for pieces of the the [wooden snake puzzle](https://www.google.com/search?q=snake+cube+puzzle&tbm=isch) and solves their arrangement.

![broken snake puzzle with note about number of each type of piece](http://www.markfickett.com/stuff/code/snakepuzzle-brokenandnotes.jpg "The Original Motivation")

The goals of this implementation are understandability, correctness; and flexability, for example in solving arbitrary volumes or introducing new types of pieces such as a Y. Notably, it is not very fast.

For more analysis, see [Jaap's Puzzle Page](http://www.jaapsch.net/puzzles/snakecube.htm) and others.

Pseudocode
----------

Start with a pile of pieces (two ends, 16 corners, 9 straights), and an
empty volume (a 3x3 cube).

Take an end ends and put it the cube.
If that finished filling the cube, we're done.
	Yield the current sequence.
	Back up and try it in the next orientation.
If that didn't finish filling the cube,
	if it doesn't connect to another open spot,
		back up and try it in the next orientation.
	else it does connect to another spot, so
		pick another piece and put it (connected) in that spot.
Try another location/piece matching:
	if we were dealing with initial end piece,
		put it in the next spot.
	elif it was some subsequent piece,
		if there's another kind we haven't tried,
			pick another kind and put it (connected) in that spot.
		else we've tried all the possibilities, there,
			so back up and (in the previous spot)
			try another location/piece matching there.



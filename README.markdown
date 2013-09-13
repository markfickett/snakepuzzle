Snake Puzzle
============

This finds working configurations for pieces of the the [wooden snake puzzle](https://www.google.com/search?q=snake+cube+puzzle&tbm=isch) and solves their arrangement.

![broken snake puzzle with note about number of each type of piece](http://www.markfickett.com/stuff/code/snakepuzzle-brokenandnotes.jpg "The Original Motivation")

The goals of this implementation are understandability, correctness; and flexibility, for example in solving arbitrary volumes or introducing new types of pieces such as a Y. Notably, it is not very fast.

For more analysis, see [Jaap's Puzzle Page](http://www.jaapsch.net/puzzles/snakecube.htm) and others.

Examples
--------

Find out how to fold a given sequence of pieces:

	python findfoldings.py ESCCSCCSCCSCCSCCSCCSCCSCCSE volumefiles/cube3.txt
	UURDDRUUFDDLUULDDFUURDDRUU
	...
	FFRBBRFFUBBLFFLBBUFFRBBRFF
	cube3: 130

Find out all the possible sequences, and how to fold them:

	python findsolutions.py volumefiles/cube3.txt
	Searching for all the solutions.
	ECCCCCCCCCCCCCCCCCCCCCCSCSE
	   UURRDLDRFULDLFUBUFRBRFDLDR
	   UURRDLDRFULURFDLULBDFDBRFR
	   ...
	ECCCCCCCCCCCCCCCCCCCSCCSCSE
	   UURRFDDFULDLBRBRULFLFUBRFR
	   UURRFDDFLURULBDBRDLFLFUBUF
	   ...
	...
	found XXX solutions for cube3 (tried YYY sequences)

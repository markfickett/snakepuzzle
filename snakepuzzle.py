"""
This finds working configurations for pieces of the the wooden snake puzzle
and solves their arrangement.


Pseudocode:

Start with a pile of pieces (two ends, some corners, some straights), and an
empty volume (a 3x3 cube).

Take an end ends and put it (not facing an outside) in the cube.
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
"""


ends = two ends
corners = some corners
straights = some straights
volume = 3x3 cube

any piece can face (these are opposites):
	down, up
	left, right
	front, back
an end can either face (connect) to one direction, or from one direction
a straight or a corner can face (connect) from any direction
a straight always faces (connects) to the opposite
	of the direction it faces (connects) from
a corner can face (connect) to any direction
	except the direction it faces (connects) from, or the opposite ove that


place a piece at a location and search from there:
	put the piece at the location
	if there was a piece before this one,
		face this piece from the opposite of the direction
		that the last piece was faced to
	if the cube is now full,
		save that solution
	else try each of the directions the new piece can face towards:
		try each of the remaining types of pieces:
			figure out the location the next piece goes at
			place the next piece there and search from there
			then remove the next piece again


place the first end:
	face it towards the first direction
	as long as it's facing towards the outside of the cube,
		face it towards the next direction


figure out the location the next piece goes at:
	find the location of the previous piece
	find the direction the previous piece is facing (connecting) to
	this determines the location of the next piece


each of the remaining types of pieces:
	if we have corners,
		include a corner
	if we have straights,
		include a straight
	if we had neither,
		we should have the other end left
		so use the end


to start:
	use the first end
	at each location in the cube,
		place the first end at that location, and search from there,
		keeping track of all the solutions we save along the way
	then print out all the solutions



__all__ = [
	'CubeThreeByThree',
]

from Volume import Volume


class CubeThreeByThree(Volume):
	def _generateAvailables(self):
		for i in xrange(3):
			for j in xrange(3):
				for k in xrange(3):
					self._availables[(i,j,k)] = True

	def getUniqueStartingLocations(self):
		return (
			(0, 0, 0),	# a corner
			#(1, 0, 0),	# a middle of an edge (impossible)
			(1, 1, 0),	# a middle of a face
			#(1, 1, 1),	# the middle of the cube (impossible)
		)


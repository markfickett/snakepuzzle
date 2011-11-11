__all__ = [
	'CubeThreeByThree',
]

from Volume import Volume


class MinSquare(Volume):
	"""
	A minimal volume for testing.
	"""
	def _generateAvailables(self):
		k = 0
		for i in xrange(2):
			for j in xrange(2):
				self._availables[(i,j,k)] = True

	def getUniqueStartingLocations(self):
		return (
			(0, 0, 0),	# a corner
		)



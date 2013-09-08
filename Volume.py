class Volume:
	"""
	A coordinate 3-space into which to place and align Pieces. This tracks
	which locations are available, which are unique starting points, and
	(given one Piece as the starting Piece) follows the linked list to
	generate a solution string.
	"""
	def __init__(self):
		self.start = None
		self._availables = {}
		self._initAvailables()

	def _initAvailables(self):
		raise NotImplementedError()

	def getNumLocations(self):
		return len(self._availables)

	def getUniqueStartingLocations(self):
		raise NotImplementedError()

	def isAvailable(self, location):
		return self._availables.get(location, False)

	def takeLocation(self, location):
		if not self.isAvailable(location):
			raise RuntimeError(
				'Location not available to be taken: %s.'
				% location)
		self._availables[location] = False

	def releaseLocation(self, location):
		status = self._availables.get(location)
		if status is None:
			raise RuntimeError(
				'Location not in volume to be released: %s.'
				% location)
		elif status == True:
			raise RuntimeError(
				'Location not taken to be released: %s.'
				% location)
		self._availables[location] = True

	def isFilled(self):
		# TODO easy optimization waiting
		return not any(self._availables.values())

	def getSolution(self):
		if not self.isFilled():
			raise RuntimeError(
				'Volume not filled! No present solution.')
		piece = self.first
		strPieces = []
		while piece:
			strPieces.append(str(piece))
			piece = piece.next
		return ', '.join(strPieces)


import os

__all__ = [
	'Volume',
	'VolumeFromFile',
]

class Volume:
	"""
	A coordinate 3-space into which to place and align Pieces. This tracks
	which locations are available, which are unique starting points, and
	(given one Piece as the starting Piece) follows the linked list to
	generate a solution string.

	Attributes:
		start: A pieces.End which starts the pieces folded into this
			Volume.
		name: A descriptive name for this Volume, used in output.
		_availables: A dictionary of coordinate triples to booleans,
			specifying whether any given location in the Volume
			has been filled by a Piece yet.
	"""
	def __init__(self, name):
		self.start = None
		self.name = name
		self._availables = {}
		self._initAvailables()
		self._free = self.getNumLocations()

	def _initAvailables(self):
		"""Sets all the locations in the Volume to True."""
		raise NotImplementedError()

	def getNumLocations(self):
		return len(self._availables)

	def getUniqueStartingLocations(self):
		"""Returns a list of coordinate triples.

		These are the locations within the Volume to start building a
		folding solution from, some subset of all locations to filter
		out impossible starting locations or reflective equivalents.
		"""
		raise NotImplementedError()

	def isAvailable(self, location):
		return self._availables.get(location, False)

	def takeLocation(self, location):
		if not self.isAvailable(location):
			raise RuntimeError(
				'Location not available to be taken: %s.'
				% location)
		self._availables[location] = False
		self._free -= 1

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
		self._free += 1

	def isFilled(self):
		return self._free == 0

	def getSolution(self):
		if not self.isFilled():
			raise RuntimeError(
				'Volume not filled! No present solution.')
		piece = self.first.deepCopy()
		pieces = []
		while piece:
			pieces.append(piece)
			piece = piece.next
		return pieces


class VolumeFromFile(Volume):
	"""A Volume defined by a text file.

	Volume Files: Layers of the volume are separated by a newline. Cubes are
	represented by "e" or "o", where "e" are the starting locations to try
	(that is, the places at which to place one end of the chain).

	For example, a 2-cube would be:
		eo
		oo

		oo
		oo
	"""
	def __init__(self, path):
		self._path = path
		self._startingPoints = []
		name = os.path.splitext(os.path.basename(path))[0]
		Volume.__init__(self, name)

	def _initAvailables(self):
		with open(self._path) as file:
			y = z = 0
			for lineNum, line in enumerate(file, start=1):
				line = line.strip()
				if line:
					self._addLine(lineNum, z, y, line)
					y += 1
				else:
					y = 0
					z += 1

	def _addLine(self, lineNum, z, y, line):
		for x, c in enumerate(line):
			if c not in ('e', 'o', ' '):
				raise ValueError(
						'bad character %r on line %d, column %d' % (c, lineNum, x+1))
			if c == ' ':
				continue
			self._availables[(x, y, z)] = True
			if c == 'e':
				self._startingPoints.append((x, y, z))

	def getUniqueStartingLocations(self):
		return self._startingPoints

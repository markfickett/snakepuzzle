"""
Given a list of strings representing reversible sequences, count the number
that each occurs. Print a (count + sequence) list and summary stats.

Usage: countUniqueOrders.py sequencesInputFile uniqueSequencesOutputFile

Example input:
ECCCCCCCSCSCCSCSCSCSCSCSCSE
ECCCCCCSCSCSCCSCSCSCCSCSCSE
ECCCCCCSCSCSCSCSCSCSCCSCSCE
ECCCCCSCCSCCSCSCCSCSCSCSCSE
...
"""


if __name__ == '__main__':
	import sys
	if len(sys.argv) != 3:
		raise RuntimeError()
	sequencesFileName = sys.argv[1]
	uniquesFileName = sys.argv[2]

	sequences = {}
	with open(sequencesFileName) as sequencesFile:
		for sequenceLine in sequencesFile.readlines():
			sequence = sequenceLine.strip() # drop the newline
			rSequence = sequence[::-1] # stride of -1 == reverse
			count = sequences.get(sequence)
			if count is None:
				count = sequences.get(rSequence)
				if count is not None:
					sequence = rSequence
			if count is None:
				count = 0
			sequences[sequence] = count + 1

	with open(uniquesFileName, 'w') as uniquesFile:
		histogram = sorted([(c, s) for (s, c) in sequences.iteritems()])
		for count, sequence in histogram:
			uniquesFile.write('%5d\t%s\n' % (count, sequence))



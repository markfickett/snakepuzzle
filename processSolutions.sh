#!/bin/bash
# Process solutions from snakepuzzle.py to produce a list of unique orderings.

SOLUTIONS_BASE=solutions
SOLUTIONS=$SOLUTIONS_BASE.txt
SOLUTIONS_PIECES_ONLY=$SOLUTIONS_BASE-piecesonly.txt
SOLUTIONS_UNIQUE=$SOLUTIONS_BASE-unique.txt

if [ -f "$SOLUTIONS" ]
then
	echo "$SOLUTIONS exists (will not regenerate)"
else
	echo Generating $SOLUTIONS with "python snakepuzzle.py"
	time python snakepuzzle.py > $SOLUTIONS
fi

echo wc $SOLUTIONS
wc < $SOLUTIONS

sed -e 's/[^ECS]//g' < $SOLUTIONS | sort > $SOLUTIONS_PIECES_ONLY
echo wc $SOLUTIONS_PIECES_ONLY
echo "(order of pieces only)"
wc < $SOLUTIONS_PIECES_ONLY

python countUniqueOrders.py $SOLUTIONS_PIECES_ONLY $SOLUTIONS_UNIQUE
echo wc $SOLUTIONS_UNIQUE
echo "(combined repetitions and reversals)"
wc < $SOLUTIONS_UNIQUE


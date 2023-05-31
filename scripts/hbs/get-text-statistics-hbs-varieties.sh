#!/bin/sh

# Define the lang suffix
suffix=$1

# Count number of words in the new prevert file
echo "New number of words:"
egrep -v  "<p|<doc|</p|</doc" /data/monolingual/${suffix}-variety.prevert | wc -w

# Count number of docs in the new prevert file
echo "New number of documents:"
egrep "<doc" /data/monolingual/${suffix}-variety.prevert | wc -l
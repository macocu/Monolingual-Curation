#!/bin/sh

# Define the lang suffix
suffix=$1

# Define the path to the initial files
path=$2

# Check whether there are any escaped characters already in the initial file: in titles or text
gunzip -c ${path}|cut -f 2,4|egrep -o "&gt;|&lt;|&quot;|&amp;"|sort|uniq -c|sort -nr

#Count initial number of words
echo "Initial number of words:"
gunzip -c ${path}|cut -f 2|wc -w

# Count based on a function
python count_previous_docs_words.py ${path}

# Count number of words in the new prevert file
echo "New number of words:"
egrep -v  "<p|<doc|</p|</doc" /data/monolingual/${suffix}-pre-domain-removal.prevert | wc -w

# Count number of docs in the new prevert file
echo "New number of documents:"
egrep "<doc" /data/monolingual/${suffix}-pre-domain-removal.prevert | wc -l
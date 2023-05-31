#!/bin/sh

# Define the language suffix
suffix=$1

#Count number of words in TXT
echo "Number of words (source and target) in TXT:"
gunzip -c /data1/lpla/macocu-release-2-rc2-with-dsi-td-variety/en-${suffix}.deduped.txt.gz|tail -n +2|cut -f 3,4|wc -w

#Count number of lines (segments?) in TXT
echo "Number of lines in TXT:"
gunzip -c /data1/lpla/macocu-release-2-rc2-with-dsi-td-variety/en-${suffix}.deduped.txt.gz|tail -n +2|wc -l

#Count number of words in TXT
echo "Number of words (source and target) in TXT - sent.gz.biroamer file:"
gunzip -c /data1/lpla/macocu-release-2-rc2-with-dsi-td-variety/en-${suffix}.sent.gz.biroamer.dsi.td.variety.gz|tail -n +2|cut -f 3,4|wc -w

#Count number of lines (segments?) in TXT
echo "Number of lines in TXT - sent.gz.biroamer file:"
gunzip -c /data1/lpla/macocu-release-2-rc2-with-dsi-td-variety/en-${suffix}.sent.gz.biroamer.dsi.td.variety.gz|tail -n +2|wc -l

# Count number of segments (tui) in TMX
echo "Number of segments (TUI) in TMX:"
gunzip -c /data1/lpla/macocu-release-2-rc2-with-dsi-td-variety/en-${suffix}.deduped.tmx.gz|grep -o "<tu tuid="|sort|uniq -c|sort -nr

# Count number of docs in the new doc file
echo "Number of documents:"
gunzip -c /data1/lpla/macocu-release-2-rc2-with-dsi-td-variety/en-${suffix}.documents.withpred.variety.gz|tail -n +2| wc -l
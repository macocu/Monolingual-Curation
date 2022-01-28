# Brief Introduction of the Monotextor, Monofixer and Monocleaner tools
Monotextor splits the sentences (loomchild) -> Monofixer -> Monocleaner

What Monofixer does:
* character fixing: sentences with encoding issues (Mojibake), HTML entities issues, wrong alphabet characters and space or punctuation issues are fixed
* deletes spaces before the punctuations
* orthography fixing: words with frequent and straightforward typos are rewritten. It is currently available for Danish, German, English, Spanish, Dutch, Norwegian, Portuguese and Turkish
* duplicates identification: a hash identifier is calculated and added to each pair of sentences in order to identify both duplicate and, optionally, near-duplicate (i.e. ignoring casing, accents, diacritics and digits) parallel sentences. A score is calculated in order to decide the best near-duplicate to be chosen. We will apply both duplicate and near-duplicate marking in our experiments.

What Monocleaner does:
* discards sentences based on hard rules (Regex): if they are too short, if they are not in the target language (if FastText doesn’t identify the target language), if there are URLs
* if the sentences pass the rules, it calculates the score for quality for each sentence

## Changes to the pipeline

TO DO (January 28)
* improve sentence splitting rules (prof.)
* Taja will prepare Slovene-specific rules for Monofixor (don’t remove spaces before three dots), examples of missed UTF mappings (š,č,ž)
* Monofixer will be ran again, just without removing spaces, then we will check the diff again
* we would rather process on paragraph level (also language identification)
    * disable hard rules, calculate quality scores (scores for fluency) for paragraph level (do the processing on the paragraphs as if they are sentences)
* we want labels also for sentences -> do the processing again on sentences
* final format for monolingual data (to be discussed with the macocu group after it’s produced):    vertical format (kind of XML), remove the metadata from prevert format (langdiff, cfclass), two separate files:
    * with metadata for each paragraph (<p>)
    * with metadata for sentence elements (<s>)


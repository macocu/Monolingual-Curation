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


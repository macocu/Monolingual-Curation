import sys
import pandas as pd
from prevert import dataset
import json

# Import the corpus, changing it into a dataset object
dset=dataset('/data/monolingual/hbs-pre-domain-removal.prevert')

# Open the final file to which we will write the new corpus
final_file = open("/data/monolingual/hbs.prevert", "w")

# Load the list of porn domains, created with the porn_identifier_final.py 
with open("list-porn-domains-hbs.json") as porn_file:
    porn_list = json.load(porn_file)

# Load a list of domains manually annotated as bad
domain_list = pd.read_csv("SouthSlavic-bad-domains-list.txt", sep = "\t")
domain_list.columns = ["domain", "issue", "source_corpus"]

# Discard bad domains that are from the Slovene corpus
domain_list = domain_list[domain_list["source_corpus"] != "Slovene"]
set_bad_domains = set(domain_list.domain.unique())

# Join the two lists as sets
final_set_bad_domains = set(porn_list) | set_bad_domains

print(f"The number of domains on the list that will be removed: {len(final_set_bad_domains)}")

# Go through the corpus, saving only texts that are not from the domains on the list

doc_counter= 0
removed_doc_counter = 0
word_counter = 0
removed_word_counter = 0


for doc in dset: # iterating through documents of a dataset
    if doc.meta['domain'] not in final_set_bad_domains:
        doc_counter += 1
        word_counter+= len(str(doc).split())
        final_file.write(doc.to_prevert())
        #sys.stdout.write(doc.to_prevert()) # Write out the original text
    else:
        removed_doc_counter += 1
        removed_word_counter+= len(str(doc).split())
        # To print only removed domains instead (comment out the previous sys.stdout):
        #sys.stdout.write(doc.to_prevert())

final_file.close()

print(f"No. of removed texts: {removed_doc_counter} ({removed_doc_counter/(removed_doc_counter+doc_counter)}%), no. of removed words: {removed_word_counter} ({removed_word_counter/(removed_word_counter+word_counter)}%)\n No. of texts in the new corpus: {doc_counter}, no. of words: {word_counter}\n Prior number of texts: {removed_doc_counter+doc_counter}, number of words: {removed_word_counter+word_counter} ")
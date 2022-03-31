import re
import json

corpus=open('/data/monolingual/sl.vert',"r")

# Set min. percentage of non-short paragraphs without punctation - optimal 0.25
set_punct_ratio = 0.25

# Set the percentage of "bad" texts out of all texts in the domain - optimal 0.94
set_bad_text_ratio = 0.94

domain_re = re.compile('domain="(.+?)"')

# This is the code that solely identifies porn domains and saves a list of domains to be removed.
# To check what is getting caught, use the code porn_identifier_code_extended.py

# Create a domain dictionary with the domain as key
# and the following list as its value: [<number of bad texts in domain>, <number of ok texts in domain>]
domain_dict = {}

for line in corpus:
    # At the beginning of the document, restart paragraph counters and find the domain.
    if line.startswith("<doc"):
        wo_punct_counter = 0
        non_short_p_counter = 0
        p_counter = 0
        current_domain = domain_re.search(line).group(1)
    # At beginning of each paragraph, count it as with or without punctuation. Count also all non-short paragraphs.
    elif line.startswith("<p"):
        p_counter += 1
        if '_wo_punct" lm_score' in line:
            wo_punct_counter += 1
        if 'quality="short"' not in line:
            non_short_p_counter += 1
    # At the end of the document, calculate the ratio of paragraphs without punctuation and add this text
    # to the count of ok texts or bad texts in the domain
    elif line.startswith("</doc"):
        no_punct_ratio = wo_punct_counter/non_short_p_counter
        if current_domain not in domain_dict:
            domain_dict[current_domain] = [0,0]
        # Added a condition that the text contains more than 2 paragraphs
        if no_punct_ratio > set_punct_ratio and p_counter > 2:
            # Add the text to the count of bad texts in the domain.
            domain_dict[current_domain][0] += 1
        else:
            # Add the text to the count of ok texts in the domain.
            domain_dict[current_domain][1] += 1

# Find all domains with the ratio of bad texts per domain high enough.
# Create a list of lists. Each inner list constitutes of the following information:
# [<domain>, <ratio of bad texts per domain>, <no. of all texts in domain>]
removed_domains = []

removed_texts_counter = 0

#Create a final list of domains to be removed.
final_list = []

for domain in domain_dict:
    # Analyse only domains that have more than 5 texts.
    if domain_dict[domain][0]+domain_dict[domain][1] > 5:
        bad_ok_texts_ratio = domain_dict[domain][0]/(domain_dict[domain][0]+domain_dict[domain][1])
        if bad_ok_texts_ratio > set_bad_text_ratio:
            removed_texts_counter += domain_dict[domain][0]+domain_dict[domain][1]
            removed_domains.append([domain,bad_ok_texts_ratio, domain_dict[domain][0]+domain_dict[domain][1]])
            final_list.append(domain)

print(f"No. of domains that will be removed: {len(final_list)}, no. of removed texts: {removed_texts_counter}")

# Create a JSON file with a list of all domains to be removed:
with open("list-porn-domains.json", "w") as json_file:
    json.dump(final_list, json_file)

print("The list of porn domains to be removed (list-porn-domains.json) is saved.")

"""
# Compare the output with ground truth from the manual checkup
import pandas as pd

dataset = pd.read_csv("/home/tajak/Porn-Identifier/Slovene_Web_2021_domain_check_porn_vs_noporn.txt", sep = "\t")
dataset_df = dataset[["Web domain", "Porn"]]
dataset_df.columns = ["domain", "porn"]
positives = dataset_df[dataset_df["porn"] == "Y"].domain.to_list()
negatives = dataset_df[dataset_df["porn"] == "N"].domain.to_list()

true_positives = 0
false_positives = 0
true_negatives = len(negatives)

for element in removed_domains:
    domain = element[0]
    if domain in positives:
        true_positives += 1
    else:
        false_positives += 1
        true_negatives -= 1
        print(f"False positive domain (domain, percentage of bad texts, all texts): {element}")

"""
corpus.close()

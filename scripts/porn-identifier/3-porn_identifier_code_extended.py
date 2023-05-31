import re
import argparse
from knockknock import discord_sender


# Get notified once the code ends
webhook_url = open("discord_key.txt", "r").read()
@discord_sender(webhook_url=webhook_url)

def check_porn_domains():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("language", help="lang suffix code used in the files")
        args = parser.parse_args()

    language = args.language

    corpus=open('/data/monolingual/{}-pre-domain-removal.prevert'.format(language),"r")

    # Set min. percentage of non-short paragraphs without punctation
    set_punct_ratio = 0.25

    # Set the percentage of "bad" texts out of all texts in the domain
    set_bad_text_ratio = 0.94

    domain_re = re.compile('domain="(.+?)"')

    problematic_texts = {}

    domain_dict = {}

    for line in corpus:
        if line.startswith("<doc"):
            text = {}
            text_string = ""
            wo_punct_counter = 0
            non_short_p_counter = 0
            p_counter = 0
            current_domain = domain_re.search(line).group(1)
            text_string += line
        elif line.startswith("<p"):
            text_string += line
            p_counter += 1
            if '_wo_punct" lm_score' in line:
                wo_punct_counter += 1
            if 'quality="short"' not in line:
                non_short_p_counter += 1    
        elif line.startswith("</doc"):
            text_string += line
            no_punct_ratio = wo_punct_counter/non_short_p_counter
            if current_domain not in domain_dict:
                domain_dict[current_domain] = [0,0]
            # Added a condition that the document contains more than 2 paragraphs
            if no_punct_ratio > set_punct_ratio and p_counter > 2:
                if current_domain not in problematic_texts:
                    problematic_texts[current_domain] = []
                text["text"] = text_string
                text["wo_punct"] = wo_punct_counter
                text["nonshort_p"] = non_short_p_counter
                text["wo_punct_ratio"] = wo_punct_counter/non_short_p_counter
                domain_dict[current_domain][0] += 1
                problematic_texts[current_domain].append(text)           
            else:
                domain_dict[current_domain][1] += 1
        else:
            text_string += line

    print(f"No. of texts that have the percentage of paragraphs without punctuation higher than {set_punct_ratio}: {len(problematic_texts)}")

    removed_domains = []
    removed_texts_counter = 0
    less_than_5_text_counter = 0
    less_than_5_domain_counter = 0

    for domain in domain_dict:
        # Analyse only domains that have more than 5 texts.
        if domain_dict[domain][0]+domain_dict[domain][1] > 5:
            bad_ok_texts_ratio = domain_dict[domain][0]/(domain_dict[domain][0]+domain_dict[domain][1])
            if bad_ok_texts_ratio > set_bad_text_ratio:
                removed_texts_counter += domain_dict[domain][0]+domain_dict[domain][1]
                removed_domains.append([domain,bad_ok_texts_ratio, domain_dict[domain][0]+domain_dict[domain][1]])
        else:
            bad_ok_texts_ratio = domain_dict[domain][0]/(domain_dict[domain][0]+domain_dict[domain][1])
            if bad_ok_texts_ratio > set_bad_text_ratio:
                less_than_5_text_counter += domain_dict[domain][0]+domain_dict[domain][1]
                # Count how many caught domains have less than 5 texts
                less_than_5_domain_counter += 1

    print(f"Number of problematic domains with more than 5 texts: {len(removed_domains)}, no. of removed texts: {removed_texts_counter}.\nNo. of caught domains with less than 5 texts: {less_than_5_domain_counter}, no. of texts: {less_than_5_text_counter}.")

    # Print text from removed domains:

    for element in removed_domains:
        domain = element[0]
        print(problematic_texts[domain][0]["text"])
        print(problematic_texts[domain][0]["wo_punct_ratio"])
        print(problematic_texts[domain][-1]["text"])
        print(problematic_texts[domain][-1]["wo_punct_ratio"])

    corpus.close()

check_porn_domains()
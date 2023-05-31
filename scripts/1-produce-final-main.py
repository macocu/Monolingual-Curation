import gzip
import re
import html
from collections import Counter
import argparse
import os
import sys
import xml.sax.saxutils
from knockknock import discord_sender

# Get notified once the code ends
webhook_url = open("discord_key.txt", "r").read()
@discord_sender(webhook_url=webhook_url)

def monotextor_to_prevert():
    # Define the the suffix used in the files
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("suffix", help="suffix, used in the file name")
        args = parser.parse_args()

    suffix = args.suffix

    # Dictionary of allowed languages (specified with the lang_code) per each corpus (suffix)
    language_code =  {
        "sl": ["sl"],
        "hbs": ["hbs_lat", "hbs_cyr"],
        "mk": ["mk"],
        "bg": ["bg"],
        "tr": ["tr"],
        "mt": ["mt"],
        "is": ["is"],
        "sq": ["sq"],
        "ca": ["ca"], 
        "uk": ["uk"],
        "el":["el"]
        }

    paths = {
        "sl": "/data1/jzaragoza/processing_sl22/monotextor-sl22-cld2/sl.raw.paragraphs.gz",
        "hbs": "/data1/jzaragoza/processing_hbs22/monotextor-hbs22/hbs.raw.paragraphs.gz",
        "mk": "/data1/jzaragoza/processing_mk22/monotextor-mk22/mk.raw.paragraphs.gz",
        "mt": "/data1/jzaragoza/processing_mt/monotextor-mt22/mt.raw.paragraphs.gz",
        "sq": "/data1/jzaragoza/processing_sq/monotextor-sq22-cld2/sq.raw.paragraphs.gz",
        "tr": "/data1/jzaragoza/processing_tr/monotextor-tr22/tr.raw.paragraphs.gz",
        "bg": "/data1/jzaragoza/processing_bg22/monotextor-bg22/bg.raw.paragraphs.gz",
        "el": "/data1/jzaragoza/processing_el/monotextor-el23/el.raw.paragraphs.gz",
        "ca": "/data1/jzaragoza/processing_ca/monotextor-ca22/ca.raw.paragraphs.gz",
        "uk": "/data1/jzaragoza/processing_uk/monotextor-uk22/uk.raw.paragraphs.gz",
        "is": "/data1/jzaragoza/processing_is/monotextor-is2123/is.raw.paragraphs.gz"
        }

    mono_path = paths[suffix]

    languages = set(language_code[suffix])

    domain_re=re.compile(r'^https?://(?:www\.)?(.+?)[/$]')
    token_re=re.compile(r'\w+|\S',re.UNICODE)

    doc=[]
    langs=[]
    langs_nonshort=[]
    lm_scores=0.
    char_count=0.
    output=False

    global doc_counter
    global word_counter
    doc_counter=0
    word_counter=0

    # Calculate punctuation per word ratio
    def paragraph_punct_ratio(text):
        tokens=token_re.findall(text)
        punct=len([e for e in tokens if e in '.;,!?:'])
        if len(tokens)==0:
            return 1.
        return punct/len(tokens)

    # Function to create the final format

    def to_stdout():
        global doc_counter
        global word_counter
        lang_char_count=len(langs)
        # Calculate lang distr for all good paragraphs (good and good_wo_punct paragraphs): for each lang, we summed up length (in characters) of all text in the document. Distribution is calculated for each language by dividing the length by the total char. length of text in the doc
        lang_distr=[(k,round(v/lang_char_count,2)) for k,v in sorted(Counter(langs).items(),key=lambda x:-x[1])]
        # Lang distr for all non-short paragraphs (Same as above, but neargood paragraphs are included as well) - used for filtering out documents that are not in the target language. Also used in the "lang_distr" attribute in the final format, if there are no 'good' paragraphs and the lang_distr (above) would be 0.
        lang_nonshort_distr=[(k,v/len(langs_nonshort)) for k,v in sorted(Counter(langs_nonshort).items(),key=lambda x:-x[1])]
        if output:
            # If there are any non-short paragraphs - if the lang distribution over non-short paragraphs is not 0:
            if len(lang_nonshort_distr)!=0:
                # The first language in lang distr needs to be in the list of allowed languages
                if lang_nonshort_distr[0][0] in languages:
                    # If there are no good paragraphs, lang_distr will be empty -> take the information from the lang. distr. of non-short paragraphs
                    if len(lang_distr)==0:
                        lang_distr=[(lang_nonshort_distr[0][0],round(1.,2))]
                    doc_counter+=1
                    # Write out the <doc> tag with all metadata
                    sys.stdout.write('<doc id="macocu.'+suffix+'.'+str(doc_counter)+'" title="'+curr_title+'" crawl_date="'+curr_crawl_date.split(' ')[0]+'" lang_distr="'+str(lang_distr)+'" url="'+html.escape(curr_url)+'" domain="'+curr_domain+'" file_type="'+curr_file_type+'" lm_score="'+str(round(lm_scores/char_count,3))+'">\n')
                    p_counter=0
                    for par in doc:
                        # Skip empty paragraphs
                        if len(par['text'])==0:
                            continue
                        p_counter+=1
                        # Write out the <p> tag and metadata
                        sys.stdout.write('<p id="macocu.'+suffix+'.'+str(doc_counter)+'.'+str(p_counter)+'" quality="'+par['quality']+'" lm_score="'+par['lm_score'].strip()+'" sensitive="'+par['sensitive'].strip()+'"')
                        # Add lang metadata if par is not short
                        if par['quality']!='short':
                            sys.stdout.write(' lang="'+par['lang']+'"')
                        # Add heading metadata
                        if par['heading']=='yes':
                            sys.stdout.write(' heading="yes"')
                        # Write a new line with all the paragraph text
                        sys.stdout.write('>\n'+par['text']+'\n')
                        # Write the closing <p> tag
                        sys.stdout.write('</p>\n')
                        # Calculate par length
                        word_counter+=len(par['text'].split())
                    # Write the closing doc tag
                    sys.stdout.write('</doc>\n')

    # Open the file and process it
    monotextor = gzip.open(mono_path, "rt")

    # Loop through the lines in the gz file

    for line in monotextor:
        # get all the information which is separated by tabs
        url,text,pid,title,crawl_date,file_type,quality,heading,_,_,lang,lm_score,sensitive=line.split('\t')

        # At the first paragraph of the next document, write out the previous document and reset document information (langs, lm_scores etc.)
        #if pid=='0' and len(doc)>0:
        if pid[:2]=='1:' and len(doc)>0:
            to_stdout()
            # At each 10.000th document, write out the number of documents and no. of words in millions.
            if doc_counter%10000==0:
                sys.stderr.write(str(doc_counter)+'\t'+str(word_counter//1000000)+'M\n')
            doc=[]
            langs=[]
            langs_nonshort=[]
            lm_scores=0.
            char_count=0.
            output=False
        # At the first paragraph of the document, get all the relevant information for doc metadata
        #if pid=='0':
        if pid[:2]=='1:':
            curr_title=html.escape(title)
            curr_url= url
            curr_domain=html.escape(domain_re.search(url).group(1))
            curr_file_type=file_type
            curr_crawl_date=crawl_date

        # Filter out all texts that have &diff or action_edit in URL (they are diff files in wikipedia and similar sites)
        if "&diff=" in curr_url or "action=edit" in curr_url:
            continue

        # Get the text from each line
        #text=escape(text)
        text=xml.sax.saxutils.escape(text)

        # Filter out documents that consist of only short paragraphs
        if quality!='short':
            # While there is at least one non-short paragraph in the document,
            # "output" will be true and the doc is written out
            output=True

            # Add information about the lang distribution if the par is not short
            langs_nonshort.extend([lang]*len(text))

        # Add information on the language for only 'good' paragraphs (calculate no. of characters in the text for this language)
        if quality.startswith('good'):
            langs.extend([lang]*len(text))
        
        # Add information on the lm_scores (multiply score with the length of text (in chars))
        lm_scores+=float(lm_score)*len(text)

        # Add information on text length (in chars)
        char_count+=len(text)

        # If a paragraph is not short and the punct per word ratio is very low, add information to the paragraph quality
        if quality!='short' and paragraph_punct_ratio(text)<0.02:
            quality+='_wo_punct'
        
        # Add information into a list of paragraph dictionaries
        doc.append({'text':text,'quality':quality,'lang':lang,'lm_score':lm_score,'heading':heading, 'sensitive':sensitive})
    else:
        # Write out also the last document in the file
        if len(doc)>0:
            to_stdout()

monotextor_to_prevert()
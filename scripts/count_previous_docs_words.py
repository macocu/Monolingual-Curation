import gzip
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the initial files")
    args = parser.parse_args()

path = args.path

def count(path):
    # Go through the corpus, count no. of texts and words

    doc_counter= 0
    word_counter = 0

    monotextor=gzip.open(path,'rt')

    for line in monotextor:
        url,text,pid,title,crawl_date,file_type,quality,heading,_,_,lang,lm_score,sensitive=line.split('\t')

        word_counter += len(text.split())

        # Add one to doc counter, and also check whether there is any pid with id that is not "1:"" that has a different url which would indicate that two documents are merged
        if pid[:2] == '1:':
            doc_counter += 1
            curr_doc_url = url
        else:
            if url != curr_doc_url:
                print("Different url at non-first paragraph".format(line))



    print(path)
    print(f"Number of texts: {doc_counter}, number of words: {word_counter}")

count(path)


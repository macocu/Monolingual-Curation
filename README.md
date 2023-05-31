# Monolingual-Curation
The Repository for the Curation of Monolingual Data work package

For the initial overview of the tools, used in MaCoCu project, see the [Documentation](https://github.com/macocu/documentation) repository.

The pipeline for creation and curation of monolingual MaCoCu corpora:
1. crawling and some pre-processing: see [MaCoCu crawler](https://github.com/macocu/MaCoCu-crawler) repository for details on crawling. Main details on the pre-processing in these steps are included in this document, in section [Data Preparation and Filtering before the Monotextor and Bitextor pipelines](#data-preparation-and-filtering-before-the-monotextor-and-bitextor-pipelines)
2. applying Monotextor pipelines - cleaning crawled data (removing encoding errors) and applying a better language identification (Monotextor), and detecting disfluent sentences (Monocleaner): see the [Monotextor](https://github.com/bitextor/monotextor/) and [Monocleaner](https://github.com/bitextor/monocleaner) repositories - more specifically, [this version of Monotextor](https://github.com/bitextor/monotextor/releases/tag/v1.0) was used for the release of MaCoCu corpora
3. additional curation of data: see section [Post-processing-curation (after the Monotextor pipeline)](#post-processing-curation-after-the-monotextor-pipeline).
4. Conversion to the XML format, which can be queried with the [prevert iterator](https://pypi.org/project/prevert/), available as a python package.

See [final-format.md](final-format.md) for details on the final files structure and attributes.

This documentation covers the 1. and 3. step of the pipeline:  [Data Preparation and Filtering before the Monotextor and Bitextor pipelines](#data-preparation-and-filtering-before-the-monotextor-and-bitextor-pipelines) and [Post-processing-curation (after the Monotextor pipeline)](#post-processing-curation-after-the-monotextor-pipeline).

The repository consists of:
- `README.md`: main documentation on monolingual data collection and curation
- [`scripts`](scripts): scripts, used in step 3 of the pipeline - post-processing curation
- some additional information about the curation: [`merging-data.md`](merging-data.md) (merging data for the same language from two crawling batches), [`prevertical-format-validator.md`](prevertical-format-validator.md) (documentation on validation of the prevertical format)
- `additional-documentation`:
    - [`Slovene-UTF-encoding-issues-mapping.md`](additional-documentation/Slovene-UTF-encoding-issues-mapping.md): a list of mappings of Slovene UTF encoding errors, which was integrated to the Monotextor tool
    - [`SouthSlavic-bad-domains-list.txt`](additional-documentation/Slovene-UTF-encoding-issues-mapping.md): a list of domains, discovered to be of low quality based on a manual check-up (see [the manual check-up annotation guidelines](https://github.com/macocu/Manual-Checking-Web-Corpora-Guidelines)) and removed from Slovene, Croatian, Serbian, Bosnian and Montenegrin corpora
    - [`list-porn-domains-sl.json`](additional-documentation/list-porn-domains-sl.json), [`list-porn-domains-hbs.json`](additional-documentation/list-porn-domains-hbs.json): list of porn domains in Slovene and Croatian-Serbian-Bosnian corpora, automatically identified (see script `scripts/porn-identifier/4-porn_identifier_final.py`)
    - [`manual-checkup-report.md`](additional-documentation/manual-checkup-report.md): report on the results of a manual check-up of Slovene and Croatian web corpus (in release 1)

## Data Preparation and Filtering before the Monotextor and Bitextor pipelines

### Overview of steps
1. The data is obtained from the web using the crawler, documented here: https://github.com/macocu/MaCoCu-crawler (for CLARIN.SI internal use: https://github.com/clarinsi/MaCoCu-crawling-pipeline) -- the files are in the [prevertical format](https://www.sketchengine.eu/my_keywords/prevertical/).
2. The prevertical data is cleaned and a validator is used to check it meets XML-like and our additional requirements. See [Prevertical format validator](prevertical-format-validator.md) for more details. 
3. The prevertical data is tokenized and de-duplicated (near paragraphs) and a language identification is applied to keep text in primary target languages. Then the tokenization is discarded and the prevertical validator is applied again at this stage.
4. The tokenized data from the previous step is indexed by corpus manager Sketch Engine to allow manual inspection of the data, looking at the list of most frequent words and instances from the most frequent domains. Samples of the prevertical files are inspected too.
5. The prevertical data after step 2 is sent to Bitextor for further bilingual processing. The prevertical data after step 3 is sent to Monotextor for further monolingual processing.
6. Since additional Slovene data was found in crawl batch 2 and since Croatian is quite similar to Serbian, Slovene and Serbo-Croatian data from batch 1 (crawled in 2021) was merged with Slovene and Serbo-Croatian from batch 2 (crawled in 2022). See [merging-data.md](merging-data.md) for more details.

### Data cleaning before both Mono-/Bitextor pipelines (both monolingual and bilingual corpora)

The full process of cleaning before the Mono-/Bitextor pipeline is driven by a Makefile in the main directory of the crawl, e.g. `/data/crawling/bs_cnr_sr/Makefile`, or in a separate file in cases of merging multiple crawls: `/data/crawling/western_south_slavic_merged/Makefile` and `/data/crawling/is23/Makefile_merge_with_21`. The default crawl & postprocessing Makefile that can be adapted to any crawl is in the [Crawling pipeline repository](https://github.com/clarinsi/MaCoCu-crawling-pipeline/blob/main/Makefile). The most important steps are described below, in the order of the procedure driven by the Makefile (all paths are relative to the main directory of the crawl). The data in the prevertical format is located in subdirectory `prevert/`.

The prevertical output of the crawler -- target `prevert/src/%.prevert.gz`:
1. Exact duplicate removal (html and text, document level)

Documents with good paragraphs, still in the prevertical format -- target `prevert/out_good/%.prevert.gz` (i.e. `prevert/out_good/*.prevert.gz`):
1. The data is edited to pass a prevertical validation and the lengths of URLs and titles are made reasonable by
  - removing or replacing XML-invalid data,
  - merging or removing excess space,
  - joining all consecutive text lines into a single line,
  - trimming doc.url to 800 characters and doc.title to 500 characters,
  - discarding empty paragraphs and empty documents.
2. Documents from additionally identified bad domains (likely MT'ed) iliveok.com, icdself.com, everaoh.com are removed.
3. Documents less similar to sample data in the language identified by the trigram model than 3 % are removed. (This should deal with paragraphs containing some the majority of foreign or nonsense characters together with some ok text.)
4. Only good paragraphs (marked by tool [Justext](https://corpus.tools/wiki/Justext) by attribute class="good") are kept.
5. The language of documents and paragraphs is identified using CLD2. See [Language Identification](#filtering-based-on-language-identification) for more details.
6. The prevertical is validated at this stage. See [Prevertical format validator](#prevertical-format-validator) for more details.
**The result data after all steps above is sent to Bitextor for further bilingual processing.**

Notes:
- Near-duplicates were left in the data at this stage since bilingual processing may need to select translations from the near-duplicate data too.
- Texts in all target languages (i.e. CSBM and English for CSBM data; Albanian and English for Albanian data; etc.) were kept since all target languages are needed for the bilingual output through the bilingual processing.
- We collected data for Slovene, Serbo-Croatian and Icelandic in both crawling batches. See [merging-data.md](merging-data.md) for details on we merged the data from the two batches, before applying any cleaning procedures.

### Additional data cleaning before the Monotextor pipeline (only for monolingual corpora)

Documents with good de-duplicated paragraphs, in the target languages, in the vertical format -- targets `vert/hbs22_cyrillic.tok.lflt.dedup.gz`, `vert/hbs22_latin.tok.lflt.dedup.gz`, `vert/sq22.tok.lflt.dedup.gz`:
1. Language filtering at the document level: Documents more similar to secondary target languages (i.e. English) than to the primary target languages (i.e. CSBM for CSBM data; Albanian for Albanian data; etc.) according to the character tri-gram model and also with the language identified by CLD2 not among primary target languages (i.e. CSBM only for CSBM data; Albanian only for Albanian data; etc.) are discarded. See [Language Identification](#filtering-based-on-language-identification) for more details.
2. Character normalization: quotes, hyphens, dashes, newlines and unicode variants are converted to normal forms. There can be exceptions for certain scripts/languages. In this batch, quotes are kept in Ukrainian data since the apostrophe (’) is a valid character (e.g. пам'ятки).
3. Removal of not desired sequences of characters (e.g. [image]...[/image]) (see [more details on sed commands used](#removal-of-not-desired-sequences-of-characters)).
4. Basic tokenization is performed, thus making a vertical file (one token per line) from the prevertical. (This is required for near paragraph de-duplication and for checking the corpus in Sketch Engine.) Tokens longer than 100 characters are trimmed to 100 characters by concatenating the first 50 characters and the last 50 characters. (URLs or garbage are usually affected.)
5. HTML entities, except those required in a valid XML, are un-escaped.
6. Documents are sorted by source URL properties to keep the more "original" data first: 1. hostname length, 2. the count of slashes, 3. path length.
7. De-duplication of similar paragraphs using Onion: paragraphs with more than 90 % of 5-tuples of tokens seen previously in the input are removed.
8. The language of documents and paragraphs is identified using CLD2. (The previous identification is overwritten.) See [Language Identification](#filtering-based-on-language-identification) for more details.

The data in the vertical format is located in subdirectory `vert/`.

The previous data is converted in the prevertical format -- targets `prevert/dedup/%.prevert.gz` (e.g. `prevert/dedup/uk22.lflt.dedup.part01.prevert.gz`):
1. The tokenization of the output from above is discarded, i.e. the data is converted back to the prevertical format.
2. The output prevertical is validated. See [Prevertical format validator](prevertical-format-validator.md) for more details.
**The result data after all steps above is sent to Monotextor for further monolingual processing.**

#### Filtering based on language identification

We identified language in the crawling process based on 2 tools:
- Simple 3-gram model -- discerned just Serbo_Croatian_Latin, Serbo_Croatian_Cyrillic and English or just Albanian and English. This is the same method as used in crawl batch 1.
- Another means of language identification was added in batch 2: [CLD2](https://github.com/CLD2Owners/cld2), [Python bindings of the C++ library](https://pypi.org/project/pycld2/).

The crawler supports specifying the following sets of languages:
- Primary target languages: Websites yielding text in these languages are crawled. Example: Serbo-Croatian Cyrillic, Serbo-Croatian Latin.
- Secondary target languages: Websites yielding text in these languages are crawled while there is some data in primary target languages there too. Example: English.
- Other recognised languages: Languages similar to target languages that should not be crawled. Example: Russian.
All documents that passed through the simple 3-gram model OR through CLD2 were accepted by the crawler. (To pass means to be in target languages.)

After the crawling, the language of documents and paragraphs is identified two more times: For the first time before sending the data to bilingual processing and for the second time before sending the data to monolingual processing. We need to re-identify the language since the data is changed by the procedure (e.g. some tokens or whole paragraphs are removed) so the former identification may not be correct for the new output. (The previous identification is overwritten.)

Document attributes related to the lang ID:
- lang (e.g. "Serbo_Croatian_Cyrillic"): language, reported by the simple 3-gram model.
- lang_diff (e.g. "0.35"): means that the similarity of document's character 3-grams to Serbo_Croatian_Cyrillic sample 3-gram model is 1 – 0.35 = 0.65.
- cld_lang (e.g. "sr"): language, reported by CLD2. Empty or "unknown" value indicates the tool was not sure enough (empty details or isReliable=False returned by `cld2.detect()`), most likely the text was too short to decide ("CLD2 is not designed to do well on very short text, lists of proper names, part numbers, etc.").
- cld_perc (e.g. "sr:95, en:3"): means that CLD2 reports 95 % Serbian and 3 % English in the plaintext of the document.

Paragraph attributes related to the lang ID:
- cld_lang (the same meaning as for documents),
- cld_perc (the same meaning as for documents).

Since we are recall oriented in this part of data processing, no text is discarded based on its language, except documents in non-primary target languages in step 1 of "Additional data cleaning before the Monotextor pipeline". It is up to further processing to either use this information or identify the language another way.


#### Removal of not desired sequences of characters

- Markup replaced with the following sed commands:
```
sed -r -e 's#\[(image|img)[^]]*\].{0,300}\[/\1[^]]*\]##gi' \
       -e 's#\[/?(image|img|url|quote)[^]]{0,300}\]##gi' \
       -e 's#\[(b|u|i)\]([^[]{0,300})\[/\1\]#\2#gi' \
       -e 's#\[/?b\]##g' \
       -e 's#\{\{[^}]{0,50}\}\}##g' \
       -e 's,■,,g' \
       -e 's,  +, ,g'
```
  - [image] or [img], incl. end tag (end tag required) and all between
  - [image], [img], [url], [quote], incl. end tag but not the text between
  - [b], [u], [i], incl. end tag, only if the corresponding end tag is there
  - [b], incl. end tag
  - everything between `{{` and `}}` removed (e.g. `{{item_ratings['val' + i]}})`)
  - case insensitive search
- HTML entitites unescaped with `html.unescape()`

## Post-processing Curation (after the Monotextor pipeline)

The entire pipeline with exact steps to follow and the output files is described [here](scripts/README.md).

Steps (outline):
- create a prevert file from the monotextor file and filter out some data (like short texts - see more below)
- transform the prevert format into XML and validate it

### Data filtering

#### Document-level

- documents consisting only of `quality="short"` paragraphs removed
- documents with "&diff=" or "action=edit" in the URL (documents with Wiki Markup) removed
- documents with the non-target language as the predominant language (non-target language is in the first position in the `lang_distr` attribute; distribution is calculated based on the language detected in all non-short paragraphs - we chose non-short paragraphs instead of only good paragraphs because some documents might have no "good" paragraphs) removed. Allowed languages are the main languages of the corpora (SL: "sl", HBS: "hbs_lat", "hbs_cyr", etc.)
- the following characters are escaped in text, titles, URLs and domains: `<, >, &, ', ''` (to satisfy XML rules). In attribute values double quotes and ampersands are escaped. In the text only angle brackets (`<` and `>`) are escaped.

#### Domain-level

Additional filtering:
- porn (Slovene and HBS only): all domains for which more than 0.94% of texts in the domain have the ratio of paragraphs without punctuation per non-short paragraphs (non_punct/non_short_p) higher than 0.25%, with limitations applied that only the texts with more than 2 nonshort sentences are analysed, and only domains with more than 5 text are analysed. False positives were manually removed from the list of domains to be deleted.
- manually annotated bad domains (Slovene and HBCS) from the list in `additional-documentation/SouthSlavic-bad-domains-list.txt`

### Format preparation

- add information on punctuation ratio in paragraphs: `wo_punct` added to paragraphs for which no. of punctuation per no. of words is less than 0.2
- calculate lang_distr
- add the metadata, listed below

See [final-format.md](final-format.md) for details on the final files structure and attributes.


## Disclaimer
The contents of this document are the sole responsibility of the members of the MaCoCu consortium, and do not necessarily reflect the opinion of the European Union.
# Merging data

We collected data for Slovene, Serbo-Croatian and Icelandic in both crawling batches. Here, we document in details, how we merged the data from the two batches.

## Merging data from batch 1 with batch 2: Slovene and Serbo-Croatian

Slovene data from batch 1 (crawled in 2021) was merged with Slovene data from batch 2 (crawled in 2022). Serbo-Croatian data in Latin script from batch 1 was merged with Serbo-Croatian data in both Latin and Cyrillic scripts from batch 2. (Serbo-Croatian means all Croatian + Serbian + Bosnian + Montenegrin = CSBM.)

The conditions of separation of Serbo-Croatian from Slovene texts follow. Document level predictions, i.e. the trigram model (doc.lang) or CLD (doc.cld_lang), were used in the process.

Slovene bilingual data:
- TLD = ".si"
- or lang = "Slovene"
- or cld_lang = "sl"
- or there are at least 5 documents with lang = "Slovene" or cld_lang = "sl" in the same website (usually an English page in a web with Slovene pages too)

Serbo-Croatian (both scripts) bilingual data:
- TLD in {.ba, .hr, .me, .rs, .срб}
- or lang in {Croatian (rename to Serbo_Croatian_Latin), Serbo_Croatian_Cyrillic, Serbo_Croatian_Latin}
- or cld_lang in {'bs', 'hr', 'sr', 'sr-ME'}
- or there are at least 5 documents meeting the two language conditions above in the same website (usually an English page in a web with Serbo-Croatian pages too)

Slovene monolingual data: From Slovene bilingual data, keep only documents with
- lang = "Slovene"
- or cld_lang = "sl"

Serbo-Croatian Latin monolingual data: From Serbo-Croatian (both scripts) bilingual data, keep only documents with
- lang = "Serbo_Croatian_Latin"
- or cld_lang in {'bs', 'hr', 'sr', 'sr-ME'} and the majority of characters is not in Cyrillic

Serbo-Croatian Cyrillic monolingual data: From Serbo-Croatian (both scripts) bilingual data, keep only documents with
- lang = "Serbo_Croatian_Cyrillic"
- or cld_lang in {'bs', 'hr', 'sr', 'sr-ME'} and the majority of characters is in Cyrillic

The main directory: `/data/crawling/western_south_slavic_merged/`.

Prevertical data, after cleaning and validation, i.e. the data before Bitextor:
- Serbo-Croatian (CSBM, both scripts together): `/data/crawling/western_south_slavic_merged/prevert/out_good/serbocroatian_part*.prevert.gz`
- Slovene: `/data/crawling/western_south_slavic_merged/prevert/out_good/slovene_part*.prevert.gz`

Prevertical data, after language filtering at the document level and de-duplication (near paragraphs) and validation, i.e. the data before Monotextor:
- Serbo-Croatian (CSBM), Latin script: `/data/crawling/western_south_slavic_merged/prevert/serbocroatian_latin.lflt.dedup.part*.prevert.gz`
- Serbo-Croatian (CSBM), Cyrillic script: `/data/crawling/western_south_slavic_merged/prevert/serbocroatian_cyrillic.lflt.dedup.part*.prevert.gz`
- Slovene: `/data/crawling/western_south_slavic_merged/prevert/slovene.lflt.dedup.part*.prevert.gz`

The procedure is driven by `/data/crawling/western_south_slavic_merged/Makefile` and consists of these steps:
1. Re-process and validate the data from batch 1 the same way as the data from batch 2 ("Data cleaning before both Mono-/Bitextor pipelines").
2. Sort the documents by the crawling batch (2022 first, 2021 second), then by language (primary target first, trigrams or CLD2), then by TLD (national first).
3. Remove exact duplicate documents (URL or content) in the sort order from step 2. (Slovene: 63 % docs kept, 6 % duplicate URL, 31 % duplicate content. Serbo-Croatian: 64 % docs kept, 4 % duplicate URL, 33 % duplicate content.) The output prevertical is validated. **The output data is sent to Bitextor for further bilingual processing.**
4. Serbo-Croatian documents with the majority of non-space characters in Cyrillic script are separated to the Cyrillic branch of the data while the rest of documents is labelled as the Latin part.
5. Re-process and validate the data for the mono procedure the same way as the data from batch 2 ("Additional data cleaning before the Monotextor pipeline"). (That implies re-sorting documents (sorted in step 2) in the order that is done before near-paragraph de-duplication: 1. hostname length, 2. the count of slashes, 3. path length.) **The output data is sent to Monotextor for further monolingual processing.**

## Merging data from batch 1 with batch 2: Icelandic 2021 and Icelandic 2023

Data from both crawls were processed the same way. The improved procedure from the second batch was applied to a copy of the 2021 data to make it comparable to the new data. Then, 2021 and 2023 files were concatenated (in that order) and near-duplicate paragraphs were removed. The full procedure is stored in `/data/crawling/is23/Makefile_merge_with_21`. The merged data for further monolingual processing is in `/data/crawling/is23/merged/prevert/dedup/is2123*.prevert.gz`. In the case of bilingual processing, the data is separated in original locations, i.e. `/data/crawling/is/prevert/out_good/parts/*.prevert.gz` (2021) and `/data/crawling/is23/prevert/out_good/*.prevert.gz` (2023).

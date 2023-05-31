# Final format of monolingual data

### Document-level
- id `macocu.si.342`
- title
- crawl_date `2021-03-23'
- lang_distr (`"[('sl', 0.85), ('hbs', 0.15)]"` - distribution calculated based on the length of paragraphs that are `quality="good"` or `good_wo_punct`; if there are none, the distribution is calculated based on the length of all non-short paragraphs. While we filter out texts that are not in the target language based on the distribution over all non-short paragraphs, for the metadata, we output the distribution over only good paragraphs, because language identification of neargood paragraphs sometimes identifies random languages if the paragraph is too short (like in the case of headers) and we want to avoid having wrong lang. identification in metadata)
- url
- domain (`r'https?://(?:www\.)?(.+?)/'`)
- file_type
- lm_score (averaged and normalized by paragraph length)

### Paragraph-level
- id `macocu.si.342.2`
- heading `yes` (only added if `yes`)
- quality (ex cfclass) `short` `neargood` `good` `neargood_wo_punct` `good_wo_punct` (`wo_punct` added to paragraphs for which no. of punctuation per no. of words is less than 0.2).
- lang (`sl`, used only in paragraphs where not `quality="short"`; for Croatian, Serbian and Bosnian, `hbs` is used)
- lm_score
- sensitive (`yes` or `no`): whether there are any IPs, emails and phone numbers in the text

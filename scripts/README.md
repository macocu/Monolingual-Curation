# Pipeline for creating final files from the Monotextor output

## Pipeline

1. Step 1: Preparation of the final prevert format and filtering out data. Put the lang. suffix, used in the files as the argument (the same argument is used in the next steps as well).
	- Create a folder for the logs `mkdir sl`
	- Before running the code, check in `1-produce-final-main.py` the allowed languages on line 24 and the path to the monotextor file on line 38.
	- Run code with: `nohup python 1-produce-final-main.py "sl" 1> /data/monolingual/sl-pre-domain-removal.prevert 2> sl/create_final_prevert.log &`
		- output: */data/monolingual/sl-pre-domain-removal.prevert*
2. Get statistics on the previous and current files: `bash 2-get-text-statistics.sh "mk" "/data1/jzaragoza/processing_mk22/monotextor-mk22/mk.raw.paragraphs.gz" > mk/statistics.txt` (arguments are lang suffix and the path to monotextor file)
3. Inspect examples of domains that would be filtered with porn identifier: `python porn-identifier/3-porn_identifier_code_extended.py "sl" > sl/caught-porn.txt &`
    - inspect the examples - if any are not to be removed, delete these domains from the JSON file that you will produce in the next step
    - if there are no porn domains to be removed, skip step 4 and 5, and just rename the file into the final name: `mv /data/monolingual/mk-pre-domain-removal.prevert /data/monolingual/mk.prevert`
4. Create a JSON file with a list of porn domains to be removed: `python porn-identifier/4-porn_identifier_final.py "sl" &`
	- output: *porn-identifier/list-porn-domains-sl.json*
5. Remove porn domains (in case of HBS and SI, use a specific file for each language code, because we also have a list of manually annotated bad domains to consider: `remove-domains_hbs.py` and `remove-domains_sl.py`). First check the list with bad domains (previous output is in folder `porn-identifier`) `nohup python 5-remove-bad-domains.py "mk" > mk/bad-domain-removal.log &`
	- **final output**: */data/monolingual/sl.prevert*
6. Validate the format: `bash prevertical-validator.sh < /data/monolingual/sl.prevert 1> sl/validation.log 2> sl/xmllint-errors.log` (Valid => no output and return code 0, invalid => error message and nonzero return code.)
7. Transform the file in XML: `cat <(echo '<corpus id="MaCoCu-sl-2.0">')  /data/monolingual/sl.prevert <(echo '</corpus>') > /data/monolingual/MaCoCu-sl-2.0.xml`
8. Validate the final XML format: `xmllint --dtdvalid MaCoCu-monolingual.dtd --noout /data/monolingual/MaCoCu-sl-2.0.xml`
9. Check the final XML file with the prevert iterator: `check_final_file.ipynb`

For the HBS corpus (Croatian-Bosnian-Serbian-Montenegrin), we processed all the languages in one corpus and separated them after the final step. See `hbs/separate-hbs-into-varieties.ipynb`.

Calculating statistics for bilingual files:
`bash get-text-statistics-bilingual.sh "mk" > mk/bilingual-stats.log`

Note:
- If the XML validation outputs an error, connected with the FF (form feed) hex character (hex 0c), correct this by applying sed on the prevert file: `sed "s/\f//g" /data/monolingual/ca.prevert > /data/monolingual/ca-corrected.prevert`. Then compare the files, and if everything is okay, rename the ca-corrected.prevert into ca.prevert.
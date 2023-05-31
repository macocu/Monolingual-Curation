#!/bin/bash

#if [ $# -ne 1 ] || [ "$1" = "-h" ]
if [ "$1" = "-h" ]
then
    echo "Prevertical validator"
    echo "Usage: $0 file.prevert"
    echo "Input line number followed by a description or the content of the line is printed"
    echo "when an error is encountered. No line number is printed when there is no error."
    echo "The input is passed several times, checking a separate condition each time."
    exit
fi

echo "========================================================================================="
echo "XML validation: valid structures and their attributes; XML entities instead of &, < and \""
echo "========================================================================================="
(echo "<?xml version=\"1.0\"?>
<!DOCTYPE corpus [
<!ELEMENT corpus (doc+)>
<!ELEMENT doc (p+)>
<!ATTLIST doc id            CDATA #REQUIRED>
<!ATTLIST doc title         CDATA #REQUIRED>
<!ATTLIST doc crawl_date    CDATA #REQUIRED>
<!ATTLIST doc lang_distr          CDATA #REQUIRED>
<!ATTLIST doc url           CDATA #REQUIRED>
<!ATTLIST doc domain          CDATA #REQUIRED>
<!ATTLIST doc file_type     CDATA #REQUIRED>
<!ATTLIST doc lm_score      CDATA #REQUIRED>
<!ELEMENT p (#PCDATA)>
<!ATTLIST p id           CDATA #REQUIRED>
<!ATTLIST p heading         CDATA #IMPLIED>
<!ATTLIST p quality           CDATA #REQUIRED>
<!ATTLIST p lang         CDATA #IMPLIED>
<!ATTLIST p lm_score         CDATA #REQUIRED>
<!ATTLIST p sensitive        CDATA #REQUIRED>
]>
<corpus>";
cat $1;
echo "</corpus>") \
| xmllint --noout --valid -

echo
echo "========================================================================================="
echo "Checking there are ordinary blanks, no empty lines, no leading/trailing/repeated blanks"
echo "========================================================================================="
grep --text --line-number --perl-regexp '[\t\f\r\cK]' $1
grep --text --line-number '^$\|^ \|  \| $' $1

echo
echo "========================================================================================="
echo "Checking all structures are on separate lines"
echo "========================================================================================="
grep --text --line-number --perl-regexp '(?<!^)<|<(?!.*>$)' $1

echo
echo "========================================================================================="
echo "Checking there are no empty structures (incl. singleton tags)"
echo "========================================================================================="
awk '/^<\// {if(last ~ /^<[^\/]/) {print NR":"$0}} {last = $0}' $1
grep --text --line-number '^<.*/[[:blank:]]*>' $1

echo
echo "========================================================================================="
echo "Checking paragraph text is on a single line"
echo "========================================================================================="
awk '/^[^<]/ {if(last ~ /^[^<]/) {print NR":"$0}} {last = $0}' $1

echo
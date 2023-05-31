# Prevertical format validator

Bash script available here: `scripts/prevertical-validator.sh`

The validator wraps the prevertical data by adding:
- an XML header, 
- an XML DTD, 
- a root element `<corpus/>`
and sends all to xmllint which is an easy to use XML parser and validator.

The main requirements for validity are:
- root element,
- document elements `<doc/>` and paragraph elements `<p/>`,
- for structure attributes: `&` escaped to `&amp;`, `<` escaped to `&lt;`, `"` escaped to `&quot`;,
- and for text nodes: `&` escaped to `&amp;` and `<` escaped to `&lt;`,
- no empty structures (incl. singleton tags),
- space sequences are normalized to single ordinary blanks,
- all paragraph text is on a single line.

The DTD is there:
- to make sure all structures are well nested, e.g. `p` within `doc` and not vice versa, no `p` outside of `doc`, etc.
- to check all required attributes are there.
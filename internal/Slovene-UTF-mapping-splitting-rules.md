# Slovene-specific rules for Bifixer (punctuation)
* there is a space before the three dots (...)
* space before and after the – sign (em-dash) depends on the context ("1–3 days", "Slovenian–Croatian border" versus "onion – a tool for ..."), the same with the dash ("Lovro Kuhar - Prežihov Voranc" versus "e-poštni naslov"), and the : sign ("Real Madrid : FC Barcelona" versus "onion: a tool for ...")

**Note**: these rules are advanced grammar rules, there will still be many texts written by Slovene native speakers where for instance the three dots will be written without the space.

Additional Slovene-specific rules (if you are doing anything with that):
* there is a space before metric system unit abbreviations and other symbols (1 m, 1 €, 1 km/h, 1 + 1 = 2)
* comma and dot in numbers are used differently than in English (1.000 for thousand and 1,3 for decimal numbers)

# Examples of missed UTF mapping (š, č, ž)

```
{
    "ÄŤ": "č",
    "ĹĄ":"š",
    "Ĺ ":"š",
    "Ĺľ": ž,

}
```

Whole sentences:
* < " In kaj pol če nimaš :D ?
< " In ko je bila ravno na tem, da me ubije s pogledom, sem ji rekel Ĺˇe: "Mar me ne moreĹˇ ljubiti takĹˇnega kot sem, in ne zaradi stvari, ki ti jih kupujem?" Se mi je kar zdelo, da oÄŤitno tudi nocoj ne bo niÄŤ s seksom!
---
 " In kaj pol če nimaš:D?
 " In ko je bila ravno na tem, da me ubije s pogledom, sem ji rekel še: "Mar me ne moreš ljubiti takšnega kot sem, in ne zaradi stvari, ki ti jih kupujem?" Se mi je kar zdelo, da oÄŤitno tudi nocoj ne bo niÄŤ s seksom!

* < " " Pravijo, da Slovence od nekdaj vleÄ<U+008D>e na morje in da za Ĺ tajerce to ĹĄe posebej velja.
— (č corrected, š not)
 " " Pravijo, da Slovence od nekdaj vleče na morje in da za Ĺ tajerce to ĹĄe posebej velja. 

* < " A se vam gabi, ker sem jo enkrat ugriznila?" me oÄŤitajoÄŤe spraĹˇuje moj brezzobi boĹľiÄŤek?
— (š corrected, č not)
 " A se vam gabi, ker sem jo enkrat ugriznila?" me oÄŤitajoÄŤe sprašuje moj brezzobi boĹľiÄŤek?

* < " Tek vsakega od nas po svoje umirja in sproĹˇÄŤa, zmanjĹˇuje stres, dviga samodisciplino in krepi telo in tako dviguje kakovost naĹˇega Ĺľivljenja.
— (š, č corrected, ž not)
 " Tek vsakega od nas po svoje umirja in sprošča, zmanjšuje stres, dviga samodisciplino in krepi telo in tako dviguje kakovost našega Ĺľivljenja.

 

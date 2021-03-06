# Slovene-specific rules for Bifixer (punctuation)
* there is a space before the three dots (...)
* space before and after the – sign (em-dash) depends on the context ("1–3 days", "Slovenian–Croatian border" versus "onion – a tool for ..."), the same with the dash ("Lovro Kuhar - Prežihov Voranc" versus "e-poštni naslov"), and the : sign ("Real Madrid : FC Barcelona" versus "onion: a tool for ...")

**Note**: These rules are advanced grammar rules, there are surely many texts written by Slovene native speakers where for instance the three dots are written without the space.

Additional Slovene-specific rules (if you are doing anything with that):
* there is a space before metric system unit abbreviations and other symbols (1 m, 1 €, 1 km/h, 1 + 1 = 2)
* comma and dot in numbers are used differently than in English (1.000 for thousand and 1,3 for decimal numbers)

# Missed UTF mapping (š, č, ž)

**UPDATE**
List of missed UTF mappings updated (March 29, 2022)

```
{
    "ÄŤ": "č",
    "ДЌ": "č",
    "Д‡": "ć",
    "ÄŚ": "Č",
    "ĹĄ": "š",
    "ЕЎ": "š",
    "Ĺˇ": "š",
    "Å¡": "š",
    "Ĺ ": "Š",
    "Ĺľ": "ž",
    "Ĺž": "ž",
    "Ĺ˝": "Ž",
    "Å3⁄4": "ž",
}
```
### Previous issues (solved)
**I have noticed that in some instances, "ÄŤ" is changed to "č" (and similarly with other patterns) and in others examples it is not (see examples below).**

Examples:
* < " In ko je bila ravno na tem, da me ubije s pogledom, sem ji rekel Ĺˇe: "Mar me ne moreĹˇ ljubiti takĹˇnega kot sem, in ne zaradi stvari, ki ti jih kupujem?" Se mi je kar zdelo, da oÄŤitno tudi nocoj ne bo niÄŤ s seksom!
---
  " In ko je bila ravno na tem, da me ubije s pogledom, sem ji rekel še: "Mar me ne moreš ljubiti takšnega kot sem, in ne zaradi stvari, ki ti jih kupujem?" Se mi je kar zdelo, da oÄŤitno tudi nocoj ne bo niÄŤ s seksom!
 
* 2447c2450
< "A pri nas doma imamo takega petelina, ki poje Ĺľe navsezgodaj zjutraj, in sicer z veliko mo**ÄŤ**nejĹˇim glasom od tvojega.
---
 "A pri nas doma imamo takega petelina, ki poje Ĺľe navsezgodaj zjutraj, in sicer z veliko mo**č**nejšim glasom od tvojega.

**In the previous example, the ÄŤ was not replaced by "č", but here it was, while the "Ĺľe" ("š") here is not replaced.**
 
* 2291c2294
< "?eprav je bilo potrebno zgodbo razĹˇiriti in raztegniti, prav tako like, so v njej videli neskon?no moĹľnosti.
---
 "?eprav je bilo potrebno zgodbo razširiti in raztegniti, prav tako like, so v njej videli neskon?no moĹľnosti.

 **Here, č is replaced by ?**

* < " " Pravijo, da Slovence od nekdaj vleÄ<U+008D>e na morje in da za Ĺ tajerce to ĹĄe posebej velja.
---
 " " Pravijo, da Slovence od nekdaj vleče na morje in da za Ĺ tajerce to ĹĄe posebej velja. 

* < " A se vam gabi, ker sem jo enkrat ugriznila?" me oÄŤitajoÄŤe spraĹˇuje moj brezzobi boĹľiÄŤek?
---
 " A se vam gabi, ker sem jo enkrat ugriznila?" me oÄŤitajoÄŤe sprašuje moj brezzobi boĹľiÄŤek?

* < " Tek vsakega od nas po svoje umirja in sproĹˇÄŤa, zmanjĹˇuje stres, dviga samodisciplino in krepi telo in tako dviguje kakovost naĹˇega Ĺľivljenja.
---
 " Tek vsakega od nas po svoje umirja in sprošča, zmanjšuje stres, dviga samodisciplino in krepi telo in tako dviguje kakovost našega Ĺľivljenja.

* < " "V jeseni leta 1946 sem v Ä<U+008D>asopisu Vesnik (op. tako se je takrat imenoval danaĹĄnji VeÄ<U+008D>er) prebral oglas, da se vabijo ljubitelji radia, predvsem mladino v zaÄ<U+008D>etni A teÄ<U+008D>aj radiotehnike.
---
 " "V jeseni leta 1946 sem v časopisu Vesnik (op. tako se je takrat imenoval danaĹĄnji Večer) prebral oglas, da se vabijo ljubitelji radia, predvsem mladino v začetni A tečaj radiotehnike.
 
* 37c618
< " Nedvomno bodo to najboljĹˇe NorveĹľanke na ÄŤelu z Marit BjĂ¶rgen, Finki Kuitunenova in Saarinenova, Ĺ vedinja Charlotte Kalla, Nemka Evi Sachenbacher Stehle, Italijanka Arianna Follis Poljakinja Justyna Kowalczyk, raÄŤunamo pa lahko Ĺˇe na kakĹˇno Rusinjo," zakljuÄŤuje MajdiÄŤeva.
---
 " Nedvomno bodo to najboljše NorveĹľanke na ÄŤelu z Marit Björgen, Finki Kuitunenova in Saarinenova, Ĺ vedinja Charlotte Kalla, Nemka Evi Sachenbacher Stehle, Italijanka Arianna Follis Poljakinja Justyna Kowalczyk, raÄŤunamo pa lahko še na kakšno Rusinjo," zakljuÄŤuje MajdiÄŤeva.

* 1022c1003
< " Tako se je ta moja Ĺželja uresniÄ<U+008D>ila ĹĄele v obdobju 1948/49, ko sem v Ljubljani naredil B teÄ<U+008D>aj ob ĹĄtudiju na STĹ  elektro smeri.
---
 " Tako se je ta moja Ĺželja uresničila ĹĄele v obdobju 1948/49, ko sem v Ljubljani naredil B tečaj ob ĹĄtudiju na STĹ elektro smeri.

* 1647c1631
< " Ĺ˝ivordeÄŤega ÄŤilija res ne moreĹˇ zgreĹˇiti, a ne?"
---
 " Ĺ˝ivordeÄŤega ÄŤilija res ne moreš zgrešiti, a ne?"

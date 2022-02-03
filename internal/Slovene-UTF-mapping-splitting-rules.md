# Slovene-specific rules for Bifixer (punctuation)
* there is a space before the three dots (...)
* space before and after the – sign (em-dash) depends on the context ("1–3 days", "Slovenian–Croatian border" versus "onion – a tool for ..."), the same with the dash ("Lovro Kuhar - Prežihov Voranc" versus "e-poštni naslov"), and the : sign ("Real Madrid : FC Barcelona" versus "onion: a tool for ...")


* however, there is never a space on just on side of the dash -->  "grad- bišču" - this is wrong segmentation of the text (found in the diff file, probably the problem was already on the website), it could be corrected by deleting space if the dash has only space on one side (to "gradbišču") if you decide so


**Note**: These rules are advanced grammar rules, there are surely many texts written by Slovene native speakers where for instance the three dots are written without the space.

Additional Slovene-specific rules (if you are doing anything with that):
* there is a space before metric system unit abbreviations and other symbols (1 m, 1 €, 1 km/h, 1 + 1 = 2)
* comma and dot in numbers are used differently than in English (1.000 for thousand and 1,3 for decimal numbers)

# Examples of missed UTF mapping (š, č, ž)

**UPDATE**
99.9% of the instances were correctly mapped. I only find the following missed UTF mapping: {"ЕЎ": "š"}
* 5777c5778
< "Cilji so uvrstitev med ЕЎtiri najboljЕЎe dvojice in potem vidimo, kako bo ЕЎlo naprej.
---
"Cilji so uvrstitev med EЎtiri najboljEЎe dvojice in potem vidimo, kako bo EЎlo naprej.

* 6285c6286
< "Daj no Viv, boÅ¡ rekla, da si zagnala tak vik in krik za njegovo reÅ¡itev kar tako, seveda ne, Äe ga ne bi ljubila bi ti bilo prav figo mar, kaj se dogaja z njim.
---
 "Daj no Viv, boš rekla, da si zagnala tak vik in krik za njegovo rešitev kar tako, seveda ne, Äe ga ne bi ljubila bi ti bilo prav figo mar, kaj se dogaja z njim.

(here, we would need to change all Ä with č, which can be a bit tricky, not sure whether it's a good idea to change that, but mentioning it just in case)

Wrong segmentation (originating from the websites):

* 6173,6174c6174,6175
< "Da" je lahko na- paÄŤen, a ta ne zmanjĹˇa moje vrednosti in spoĹˇtovanja, ki sem ga dolĹľan sebi.
< "Da" je lahko trden v veÄŤji ali manjĹˇi meri.Odvisno od vsebine stvarnosti,za- radi katere je izreÄŤen.
---
 "Da" je lahko na- pačen, a ta ne zmanjša moje vrednosti in spoštovanja, ki sem ga dolžan sebi.
 "Da" je lahko trden v večji ali manjši meri.Odvisno od vsebine stvarnosti,za- radi katere je izrečen.

*6178c6179
< "Da" nima ena- ke teĹľe, ÄŤe potrjuje sodelovanju pri hiĹˇni zabavi, ali pa ÄŤe je potrditev zvestobe pri poroki.
---
 "Da" nima ena- ke teže, če potrjuje sodelovanju pri hišni zabavi, ali pa če je potrditev zvestobe pri poroki.


```
{
    "ÄŤ": "č",
    "ĹĄ":"š",
    "Ĺ ":"š",
    "Ĺľ": "ž",
    "Ĺˇ": "ž",
    "Ĺž": "ž",
    "Ĺ˝": "Ž"
}
```
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

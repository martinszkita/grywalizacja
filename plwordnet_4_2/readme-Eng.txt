plwnXML Format
--------------
This is an XML-based native format for plWordNet 4.2 and the only one (so far) 
that completely and faithfully encodes the data stored in plWordNet, e.g.:
* assignment of all lexical units to domains (lexicographic files),
* complete description of relations between lexical units and synsets,
* substitution tests for lexico-semantic relations.

The version in plwnXML format also contains full Princeton Wordnet 3.1 
(PWN) data (Princeton University (c)).
PWN lexical units can be distinguished by specially encoded part of speech names:
* rzeczownik pwn (nouns from PWN),
* czasownik pwn (verbs from PWN),
* przymiotnik pwn (adjectives from PWN),
* przysłówek pwn (adverbs from PWN).
PWN relations connect synsets containing only PWN lexical units.

The list of Polish Wordnet to Princeton Wordnet mapping relations:
* synonimia_międzyjęzykowa (interlingual synonymy)
    - Syn_plWN-PWN

* międzyjęzykowa_synonimia_częściowa (interlingual near synonymy)
    - międzyjęzykowa_synonimia_częściowa_plWN-PWN

* międzyjęzykowa_synonimia_międzyrejestrowa (interlingual inter-register synonymy)
    - synonimia_międzyrejestrowa_plWN-PWN

* hiperonimia_międzyjęzykowa (interlingual hypernymy)
    - Hiper_plWN-PWN

* hiponimia_międzyjęzykowa (interlingual hyponymy)
    - Hipo_plWN-PWN

* meronimia_międzyjęzykowa (interlingual meronymy)
    - mczęść_plWN-PWN   (I meronymy: part of subtype)
    - melement_plWN-PWN (I meronymy: element of collection)
    - mmateriał_plWN-PWN (I meronymy: material or substance)

* holonimia_międzyjęzykowa (interlingual holonymy)
    - hczęść_plWN-PWN (I holonymy: part of)
    - helement_plWN-PWN  (I holonymy: element of collection)
    - hmateriał_plWN-PWN (I holonymy: material or substance)

* międzyjęzykowa_synonimia_międzyparadygmatyczna (interlingual cross-categorial synonymy)
	-	międzyjęzykowa_synonimia_międzyparadygmatyczna_made_of_plWN-PWN (I cross-categorial synonymy: made of)
	-	międzyjęzykowa_synonimia_międzyparadygmatyczna_resembling_plWN-PWN (I cross-categorial synonymy: resembling)
	-	międzyjęzykowa_synonimia_międzyparadygmatyczna_related_to_plWN-PWN (I cross-categorial synonymy: related to)

In a commentary to a lexical unit the following markers are used:
##K: rejestr. <-- qualifier
##D: definicja. <-- shortened gloss
[##W: przykład.] <-- usage examples
{##L: http...] <-- link to a Wikipedia equivalent

Multiword lexical units:
---------------------------
<##DD>, <##DS>, <##aDD>, <##as1DD>, <##as2DD> <-- multiword lexical unit
<##s> <-- semantically compositional unit

Sentiment annotation:
---------------------------
##A1 <-- Annotator 1.
##A2 <-- Annotator 2.

basic emotions = {joy, trust, anticipation, sadness, anger, fear, disgust, surprise}
universal values = {usefulness, welfare, truth, knowledge, beauty, happiness, uselessness, injustice,
ignorance, fallacy, ugliness, misfortune} 
polarity = {- m, - s, 0, +s, +m}
- m <-- strong negative,
- s <-- weak negative,
0 <-- neutral,
+ s <-- weak positive,
+ m <-- strong positive
[ ] <-- usage examples

------------------------
Princeton WordNet Format - NOT SUPPORTED SINCE 2.9
PWN Format defines a number of labels for lexico-semantic relations. Not all 
of these relations have their counterparts in plWordNet and vice versa. PWN Format  
has been extended with relation labels for lexico-semantic relations that are 
specific for plWordNet. For relations that occur both in WordNet and plWordNet 
the labels have been preserved.

Synsets are assigned to domains (lexicographic files) in WordNet and all lexical 
units belonging to one synset share the same domain. In PlWordNet, each lexical 
unit is described by its domain. For the needs of export to PWN Format we assumed 
that the domain of a synset is equal to the domain of its first lexical unit 
(according to the database order). Domain labels have been mapped to the 
corresponding domain labels of PWN Format. Additionally, four new domains were 
introduced:
45 adj.quality JAK - qualitative adjectives
46 adj.grad GRAD de-adjectival adjectives (feature intensity)
47 sys SYS - systematics, 
48 not.set - domain not set
UTF-8 encoding was applied to all text data.
The database was tested in the NLTK package for Natural Language Processing.
In order to use it with NLTK all files from the folder plwordnet_2_*_pwn_format copy into the folder ~/nltk_data/corpora/wordnet
should be unpacked in the home folder of a user. 
Sample usage of wordnet by nltk in ipython console:

>>> from nltk.corpus import wordnet as wn
>>> wn.synsets('Politechnika')

Output:

[Synset('politechnika.n.01'), Synset('politechnika.n.02')]

Additional information concerning the usage of a wordnet 
in NLTK can be found in: http://nltk.googlecode.com/svn/trunk/doc/howto/wordnet.html.

VisDic Format
-------------
VisDic Format does not support relations between lexical units and thus plWordNet 
database stored in this format contains only relations between synsets.
In a similar way to PWN Format, synsets, not lexical units, are assigned to domains. 
This discrepancy has been solved in the same way as in the case of export 
to PWN Format (see above).
Because lexico-semantic relations and domains are overtly expressed in a text 
form in VisDic Format no additional mapping was necessary.


Format plwnXML
--------------
Jest to jedyny format zawierający pełny obraz Słowosieci 4.2.
Aktualnie jako jedyny zawiera: 
* pełne przypisanie dziedzin do jednostek,
* definicje relacji jednostek leksykalnych i synsetów,
* testy poprawności dla relacji.

Dystrybucja w formacie plwnXML zawiera również kompletny Princeton Wordnet 3.1 (PWN) (Princeton University (c)) wraz z rozszerzeniem o 8000 nowych angielskich jednostek leksykalnych (7 tys. lematów, 5,5 tys. synsetów).

Jednostki leksykalne z PWN mogą zostać odróżnione na podstawie nazw części mowy nazwanych w specjalny sposób:
* rzeczownik pwn (rzeczownik z Princeton WordNet),
* czasownik pwn (czasownik z Princeton WordNet),
* przymiotnik pwn (przymiotnik z Princeton WordNet),
* przysłówek pwn (przysłówek z Princeton WordNet).
Relacje z PWN łączą tylko synsety zawierające jednostki leksykalne z Princeton WordNet.

Lista relacji rzutujących Słowosieć na PWN:
* synonimia_międzyjęzykowa
    - Syn_plWN-PWN

* międzyjęzykowa_synonimia_częściowa
    - międzyjęzykowa_synonimia_częściowa_plWN-PWN

* międzyjęzykowa_synonimia_międzyrejestrowa 
    - synonimia_międzyrejestrowa_plWN-PWN

* hiperonimia_międzyjęzykowa 
    - Hiper_plWN-PWN

* hiponimia_międzyjęzykowa 
    - Hipo_plWN-PWN

* meronimia_międzyjęzykowa
    - mczęść_plWN-PWN
    - melement_plWN-PWN
    - mmateriał_plWN-PWN

* holonimia_międzyjęzykowa 
    - hczęść_plWN-PWN
    - helement_plWN-PWN
    - hmateriał_plWN-PWN

* międzyjęzykowa_synonimia_międzyparadygmatyczna
	-	międzyjęzykowa_synonimia_międzyparadygmatyczna_made_of_plWN-PWN
	-	międzyjęzykowa_synonimia_międzyparadygmatyczna_resembling_plWN-PWN
	-	międzyjęzykowa_synonimia_międzyparadygmatyczna_related_to_plWN-PWN


W komentarzu jednostek stosujemy następujące znaczniki:
##K: rejestr. <-- kwalifikator
##D: definicja. <-- skrócona definicja
[##W: przykład.] <-- przykłady użycia
{##L: http...] <-- link do odpowiednika z Wikipedii

Wielowyrazowe jednostki leksykalne
---------------------------
<##DD>, <##DS>, <##aDD>, <##as1DD>, <##as2DD> <-- leksykalna jednostka wielowyrazowa
<##s> <-- jednostka kompozycyjna semantycznie

Anotacja nastawieniem emocjonalnym
---------------------------
##A1 <-- anotator 1.
##A2 <-- anotator 2.

emocje podstawowe = {radość, zaufanie, cieszenie się na coś oczekiwanego, smutek, złość, strach, wstręt, zaskoczenie czymś nieprzewidywanym}
wartości uniwersalne = {użyteczność, dobro drugiego człowieka, prawda, wiedza, piękno, szczęście, nieużyteczność, krzywda, niewiedza, błąd, brzydota, nieszczęście}
nastawienie emocjonalne = {- m, - s, 0, +s, +m}
- m <-- mocno negatywne,
- s <-- słabo negatywne,
0 <-- neutralne,
+ s <-- słabo pozytywne,
+ m <-- mocno pozytywne
[ ] <-- nawias zawiera przykład użycia



Format Princeton Wordnet - FORMAT NIE jEST JUŻ WSPIERANY OD WERSJI 2.9
------------------------
Format PWN standardowo definiuje mnemoniki relacji synsetów i jednostek leksykalnych.
Nie wszystkie relacje mają swój odpowiednik w Słowosieci, jak również wiele relacji
występujących w Słowosieci nie ma odpowiednika w PWN. Format PWN został rozszerzony
o odpowiednie mnemoniki dla relacji występujących tylko w Słowosieci. Mnemoniki
dla odpowiadających sobie relacji ze Słowosieci i PWN zostały zachowane.
W formacie PWN synsety posiadają dziedziny, które są dziedziczone przez wszystkie
jednostki synsetu. W Słowosieci każda jednostka synsetu posiada swoją dziedzinę.
Podczas eksportu synsetom w formacie PWN zostaje nadana dziedzina pierwszej jednostki synsetu
Słowosieci.

Identyfikatory dziedzin zostały zrzutowane do odpowiadającym im w formacie PWN. Dodatkowo
zostały dodane cztery nowe dziedziny:
45 adj.quality JAK przymiotniki jakościowe
46 adj.grad GRAD przymiotniki odprzymiotnikowe (natężenie cechy)
47 sys SYS systematyka, klasyfikacja 
48 not.set dziedzina nie ustawiona
Polskie znaki zostały zapisane w kodowaniu UTF-8.
Baza została przetestowana w pakiecie do przetwarzania języka naturalnego NLTK.
W celu jej wykorzystania należy rozpakować wszystkie pliki z folderu plwordnet_2_*_pwn_format skopiować do podkatalogu ~/nltk_data/corpora/wordnet
w katalogu domowym użytkownika.
Przykładowe użycie za pomocą nltk w konsoli ipython:

>>> from nltk.corpus import wordnet as wn
>>> wn.synsets('Politechnika')

Wyjście:

[Synset('politechnika.n.01'), Synset('politechnika.n.02')]

Więcej informacji na tematy wykorzystania wordnetu w NLTK można znaleźć pod
adresem: http://nltk.googlecode.com/svn/trunk/doc/howto/wordnet.html.

Format VizDic
-------------
Format VizDic nie obsługuje relacji pomiędzy jednostkami leksykalnymi, dlatego baza
w tym formacie zawiera tylko relacje synsetów.
W formacie VizDic, podobnie jak w formacie PWN, synsety posiadają dziedziny. 
Problem ten został rozwiązany tak samo jak w przypadku eksportu do formatu PWN.
Ponieważ relacje jak i dziedziny synsetów definiowane są w postaci tekstowej to
rzutowanie nie jest konieczne.

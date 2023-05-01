# Dělění materiálu s minimálním odpadem

Tento projekt se skládá ze dvou hlavních skriptů. První skript implementuje algoritmus column generation pro řešení optimalizačních problémů. Column generation je efektivní technika pro řešení problémů s velkým počtem proměnných, kde lze omezit množství proměnných použitých v počátečním řešení a postupně přidávat další, pokud jsou potřeba. Druhý skript je grafické rozhraní, které umožňuje uživatelům snadno vytvářet a upravovat vstupní data a spouštět výpočet column generation. Tento projekt byl vytvořen v rámci předmětu Algoritmy umělé inteligence s cílem ukázat praktickou implementaci a využití algoritmů v oblasti optimalizace.


Algoritmy umělé inteligence jsou navrženy pro simulaci lidského myšlení a chování v oblastech, jako jsou rozpoznávání obrazu, řešení problémů a strojové učení. Tento druh algoritmů se snaží vytvořit inteligentní chování v počítači, které může řešit úlohy, které by normálně vyžadovaly lidskou interakci nebo rozhodování. Mezi nejznámější algoritmy umělé inteligence patří například expertní systémy, Bayesovské sítě, fuzzy logika, rozhodovací stromy, markovské modely a mnoho dalších. Tyto algoritmy jsou využívány v široké škále oblastí, včetně průmyslového inženýrství, medicíny, ekonomie, psychologie a dalších.

Motivací projektu Cutting Stock byla potřeba snížit množství odpadu, který vznikal při řezání trubek v továrně. Tato továrna vyrábí vozíky a regály pro interní použití a při řezání trubek vznikal velký množství odpadu. Cílem projektu bylo najít nejlepší možný způsob řezání trubek, aby bylo minimalizováno množství odpadu a byly využity všechny dostupné kusy polotovaru co nejefektivněji. Tímto způsobem se mohou snížit náklady na materiál a vylepšit výkonnost a efektivitu výrobního procesu.

## Instalace do virtuálního prostředí

```bash
pip install -r requirements.txt
```

### Hlavní použité knihovny

* [PyQT5](https://doc.qt.io/qtforpython-5/)
* [PuLP](https://coin-or.github.io/pulp/)
* [Matplotlib](https://matplotlib.org/)

## Popis souborů

* __gui.py__  obsahuje skript s grafickým rozhraním (GUI) pro aplikaci. GUI umožňuje uživatelům snadno interagovat s aplikací prostřednictvím grafických prvků, jako jsou tlačítka, textová pole a seznamy. V případě tohoto projektu umožňuje uživatelům zadávat vstupní data pro column generation a spouštět výpočet. GUI také poskytuje uživatelsky přívětivý způsob zobrazování výstupů algoritmu, jako jsou tabulky a grafy. Soubor __gui.py__ byl vytvořen pomocí knihovny PyQt5, která umožňuje snadnou tvorbu GUI v Pythonu.
* __column_generation.py__ obsahuje skript s implementací algoritmu column generation. Tento algoritmus je využíván pro řešení optimalizačních problémů s velkým počtem proměnných, kde lze omezit množství proměnných použitých v počátečním řešení a postupně přidávat další, pokud jsou potřeba. Skript umožňuje uživatelům definovat model, objektivní funkci a omezující podmínky a poté spustit výpočet. Výsledkem výpočtu je optimální řešení optimalizačního problému. Soubor __column_generation.py__ využívá knihovny jako je například numpy pro práci s maticemi a vektory a PuLP pro řešení lineárních programů. Tento skript je spouštěn prostřednictvím GUI v souboru __gui.py__
* __cutting_stock.py__ slouží pouze pro spuštění aplikace. Jeho účelem je inicializovat GUI aplikace a spustit ji. Pokud uživatelé chtějí spustit aplikaci, stačí spustit soubor __cutting_stock.py__. Ten následně zavolá soubor __gui.py__, který obsahuje skript s grafickým rozhraním aplikace. Uživatelé mohou poté používat GUI pro zadávání vstupních dat a spouštění výpočtu pomocí column generation.

### Vstupní data

Vstupní data pro aplikaci Cutting Stock jsou zadané uživatelem v tabulce. Uživatelé nejprve nastaví výchozí délku polotovaru a poté zadávají požadované řezy a jejich počty. Pro každý řez uvedený uživatelem se vypočítá počet řezů, které je nutné provést na zadané délce polotovaru a výsledek se zobrazí v tabulce. Tyto vypočítané řezy poté mohou být použity v algoritmu column generation pro výpočet optimálního řezání polotovaru.

### Výstupní data

V aplikaci Cutting Stock jsou k dispozici dva hlavní výstupy, které jsou zobrazeny v grafickém rozhraní. Prvním z těchto výstupů je graf s patterny řezů, který ukazuje, jak je daný materiál nejvýhodněji rozřezat na jednotlivé kusy. Druhým výstupem je okno s tabulkou, které ukazuje, kolik kusů polotovaru bude zhruba potřeba pro zadaný počet řezů a jaké jsou konkrétní délky a počty jednotlivých kusů polotovaru. Tyto výstupy jsou velmi užitečné pro výrobu a plánování skladování materiálu.

## Příklad použití

```bash
python cutting_stock.py
```

![Gui GIF]()

## Metoda CG

 Metoda column generation je optimalizační metoda, která se používá pro řešení kombinatorických optimalizačních problémů, jako je například problém cutting stock, který je řešen v projektu Cutting Stock. Hlavní myšlenkou metody column generation je vytváření nových sloupců (tj. nových řezů trubek) postupným řešením relaxované duální lineární programovací úlohy. Tyto nové sloupce jsou následně přidány do původního celočíselného lineárního programu, aby bylo dosaženo lepšího řešení. Metoda column generation je často používána v kombinaci s celočíselným lineárním programováním pro řešení složitých optimalizačních problémů.
 
 Metoda column generation se využívá při řešení celočíselného lineárního programování (ILP), které má za úkol najít optimální řešení s celočíselnými proměnnými. Tento typ úlohy je velmi obecný a lze ho použít na mnoho různých optimalizačních problémů, jako je například rozvrhování nebo optimalizace přiřazení zdrojů.

 V metodě column generation se nejprve vytvoří duální relaxovaná lineární programová úloha, která se řeší pomocí simplexové metody. Tento relaxovaný duální problém neobsahuje celočíselné proměnné a vede k optimální hodnotě duálního problému. Poté se vytvoří nové sloupce (řezy trubek) pro původní celočíselnou úlohu na základě nejvíce restriktivních omezení, které nebyly zahrnuty v původním modelu.

 Nové sloupce se poté přidávají do původního celočíselného programu, aby bylo dosaženo lepšího řešení. Tento proces se opakuje, dokud se nedosáhne optimálního řešení. Metoda column generation je velmi efektivní při řešení problémů s velkým počtem proměnných a omezení, protože umožňuje efektivně hledat nové sloupce, aniž by bylo nutné řešit celou úlohu znovu.

 V případě projektu Cutting Stock se metoda column generation využívá pro optimalizaci řezu trubek na polotovary a minimalizaci odpadu materiálu. Nové sloupce v této úloze představují nové řezy trubek a jejich přidání vede k lepšímu řešení optimalizační úlohy. [Více o metodě](https://optimization.cbe.cornell.edu/index.php?title=Column_generation_algorithms)

## Výsledky

V rámci projektu se podařilo úspěšně vytvořit grafické uživatelské rozhraní (GUI) v PyQT, které umožňuje uživateli zadat vstupní data a následně spustit výpočet pomocí metody column generation s využitím knihovny PuLP. Výsledky výpočtu jsou poté zobrazovány v GUI v podobě dvou oken - v jednom okně je zobrazen graf s jednotlivými patterny, tedy jak má být daný materiál řezán, a v druhém okně je zobrazena tabulka s přesným počtem kusů polotovaru potřebných pro daný výpočet. Celkově se podařilo úspěšně dosáhnout hlavního cíle projektu, kterým bylo snížení odpadu a optimalizace využití materiálu.

## Závěr 

Závěrem lze říci, že projekt s názvem Dělění materiálu s minimálním odpadem, který obsahuje dva hlavní skripty - jeden pro výpočet column generation metody a druhý s grafickým rozhraním vytvořeným v PyQt. Byla zmíněna motivace projektu, kterou bylo snížení odpadu při řezání trubek na vozíky nebo regály pro interní použití v továrně.

Výsledky projektu zahrnovaly úspěšné vytvoření grafického rozhraní, implementaci column generation metody s použitím knihovny Pulp, a zobrazování výsledků pomocí grafů a tabulek. Nabízí se také prostor pro vylepšení, například možnosti načítání vstupních dat ze souborů CSV a přehlednějším výpisu výsledků do tabulek. Byla také zmíněna potřeba upravit column generation metodu tak, aby počítala buď přesné množství přířezů nebo větší rovno.

Celkově lze říci, že projekt Dělění materiálu s minimálním odpadem představuje úspěšný krok směrem k efektivnějšímu řezání trubek v průmyslu a nabízí prostor pro další vylepšení a rozvoj.

## Autor

Jan Zmrzlý, zmrzlyjan@gmail.com
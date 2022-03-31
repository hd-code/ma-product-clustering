# Clusteranalyse

## Begriff und Einordnung

maschinelles Lernen (machine learning)

unüberwachtes Lernen (unsupervised learning)

Clusteranalyse (cluster analysis)

Vorgehen: CRISP Modell

## Distanz- und Ähnlichkeitsmaße

### Definition

Clustering erfolgt über Bestimmung der "Nähe" (engl. proximity) der Objekte zueinander. [vgl. @kaufman2009; Kap. 1.2 Types of Data and How to Handle Them]

Notation:

- Objekte oder Datenpunkte sind Vektoren aus numerischen und/oder nominalen Attributen: $x = (i | i \text{ is nominal or numerical attribute})$
- Zugriff auf Attribut-Wert eines Datenpunkts über Attribut-Index: $x_i$
- Menge aus Datenpunkten (= Datenset) mit Großbuchstaben angegeben z.B. $x \in X$ oder $y \in Y$
- Menge $N$ sind stets alle Datenpunkte also gesamtes Datenset
- mit $N_i$ wir die Menge aller Werte eines Attributs im Datenset beschrieben
- Cluster sind spezielle Teilgruppen $C \subset N$
- Cluster können andere Cluster oder Vektoren enthalten: $C = {x | x = C_i \vee x \in X}$
- leere Cluster gibt es nicht $C \neq \emptyset$
- i.d.R. $n=|N|$, $k=|C|$, $i=\text{Attribut-Index}$, $j=\text{zweiter Attribut-Index}$

Bestimmung der Nähe mittels Abstands- bzw. Distanzmaßen. Distanzmaß wird über Funktion $d$ dargestellt [vgl. @kaufman2009; Kap. 1.2 Types of Data and How to Handle Them]

||||
|-|--|----|
| 1. | $d(x,y) \geq 0$ | Distanzen sind steht positiv |
| 2. | $d(x,x) = 0$ | zwei gleiche Objekte haben immer einen Abstand von $0$ |
| 3. | $d(x,y) = d(y,x)$ | die Distanzfunktion ist kommutativ bzw. symmetrisch |
| 4. | $d(x,z) \leq d(x,y) + d(y,z)$ | Distanzen geben stets den kürzesten Weg an |

: Eigenschaften der Abstandfunktion $d$

Statt Distanzmaße auch Verwendung von Ähnlichkeitsmaßen $s(x,y)$ (engl. similarity) möglich. Ähnlichkeit i.d.R. im Interval $[0,1]$ angegeben, wobei $s(x,x)=1$. Wenn Distanz z.B. durch Normalisierung ebenfalls im Interval $[0,1]$ liegt, dann gilt: $d(x,y)=1-s(x,y)$ [vgl. @kaufman2009; Kap. 1.2 Types of Data and How to Handle Them]

Distanz und Ähnlichkeit dadurch beliebig austauschbar, deshalb diese Verwendung empfehlenswert.

(Frage: Erwähnung der Proximity Matrix? ist eigentlich nicht wichtig für diese Arbeit)

### Numerische Attribute

durch (rationale) Zahlen dargestellt [vgl. @kaufman2009; Kap. 1.2 Types of Data and How to Handle Them], mit stetigen (engl. continuous) Werten [vgl. @huang1998]. Umfasst damit sowohl Daten in Intervall- und Verhältnisskalen (engl. interval and ratio data) [vgl. @boslaugh2012; Kap. 1 Basic Concepts of Measurement]

#### Minkowski-Familie

Datenpunkte damit numerischen Vektoren also Punkte. Bestimmung des Abstand der Punkte => verschiedene Maße, gehören alle zur Minkowski-Familie [vgl. @cha2007; und @king2015; Kap. 1.2 Capturing the Clusters]:

| Name | $p$-Norm | Formell |
|-|-|---|
| Minkowski | allgemein | $d(x,y) = \sqrt[p]{\sum_{i=1}^n |x_i - y_i|^p}$ |
| Manhattan | $p=1$ | $d(x,y) = \sum_{i=1}^n |x_i - y_i|$ |
| euklidisch | $p=2$ | $d(x,y) = \sqrt{\sum_{i=1}^n |x_i - y_i|^2}$ |
| Chebyshev | $p=\infty$ | $d(x,y) = \max |x_i - y_i|$ |

: Übersicht gängiger Maße aus der Minkowski-Familie

höhere $p$-Norm bedeutet i.d.R. robustere Bestimmung des Abstands. Manhattan => Winkel zwischen zwei Punkten, euklidisch => Länger der Geraden durch die Punkte [vgl. @king2015; Kap. 12.3 Which Proximity Measure Should Be Used?]

verschiedenste Versionen und Abwandlungen dieser Maße [siehe @cha2007]

- aber die meisten basieren auf Minkowski-Familie
- oder lassen sich auf Minkowski abbilden (z.B. Maße basierend auf der Pearson Korrelation nutzen im Kern euklidischen Abstand zur Berechnung)
- liefern ähnliche Ergebnisse wie klassische Minkowski
- [siehe @cha2007] Clustering mit verschiedenen Maßen und dann Ergebnisse geclustert. (eigene Erkenntnis aus dem Paper) im Kern jeder Cluster Gruppe war auch ein Vertreter der Minkowski-Familie

#### Normalisierung

manche numerischen haben logarithmischen Zusammenhang (10 zu 20 ist gleichbedeutend mit 100 zu 200), dann $x_i' = \log x_i$ für gleichmäßige Abstände

Projektion auf $[0,1]$ => $x' = \frac{x - \textrm{avg }X}{\max X - \min X}$; empfehlenswert, wenn Attribute gleichgewichtet sein sollen

manchmal ist Normalisierung nicht sinnvoll, da dadurch verschiedene "Gewichtung" der Attribute bestimmtes Wissen dargestellt wird => erfordert Domänenwissen

Eventuell sogar arbeiten mit Gewichtsvektor für die Attribute => eher spezielle Anwendungsfälle

gesamter Abschnitt [vgl. @kaufman2009; Kap. 1.2 Types of Data and How to Handle Them]

### Kategorische Attribute

statt Zahlen bestehen Datenpunkte aus ihnen zugeordneten Kategorien oder Labels [vgl. @boslaugh2012; Kap. 5 Categorical Data]

Manchmal gibt es eine sinnvolle Reihenfolge der Labels (z.B. xs, s, m, l, xl), dennoch keine Aussage über Verhältnis oder Intervall zueinander möglich. mit Reihenfolge als ordinal bezeichnet, ohne als nominal [vgl. @boslaugh2012; Kap. 1 Basic Concepts of Measurement; Kap. 5 Categorical Data]

#### Ordinale Attribute

zwei Möglichkeiten:

Reihenfolge ignorieren und als nominal verarbeiten => siehe folgende Abschnitte

aber eher empfohlen: Umwandlung und Verarbeitung als numerische Attribute:

- Nummerierung der Labels nach ihrer Reihenfolge von $1$ bis $n$
- dann: $x'=\frac{x-1}{n-1}$
- dadurch im Interval $[0,1]$ in $n-1$ gleichmäßige Abschnitte eingeteilt

ganzer Abschnitt [vgl. @kaufman2009; Kap. 1.2 Types of Data and How to Handle Them]

#### Nominale Attribute

dieser Teil aus [vgl. @kaufman2009; Kap. 1.2.5 Nominal, Ordinal, and Ratio Variables]

Umwandlung in sog. binäre Attribute:

1. bei 2 Ausprägungen => $0=\text{erste Ausprägung}$, $1=\text{zweite Ausprägung}$ z.B. yes/no
2. ab 3 =>
  - entweder in 2 Ausprägungen komprimieren
  - oder ein neues Attribut pro Kategorie definieren: $0=\text{gehört nicht zur Kategorie}$, $1=\text{gehört zur Kategorie}$

folgende aus [@kaufman2009; Kap. 1.2.5 Binary Variables]

für 1. => sog. "symmetrische" binäre Attribute, 2. => "asymmetrische"; Verarbeitung mit speziellen Ähnlichkeitsmaßen:

##### Simple matching

$s(x,y)=\frac{|x \cap y| + |\bar{x} \cap \bar{y}| }{|x \cup \bar{x} \cup y \cup \bar{y}|}$

- jeder Match (beide Datenpunkte haben Label und beide Punkte haben ein Label **nicht**) wird gezählt
- nur für symmetrische geeignet
- gibt Varianten davon mit unterschiedlichen Gewichten für Matches usw. => lassen sich alle auf Simple matching abbilden

##### Jaccard-Koeffizent

$s(x,y) = \frac{|x \cap y|}{|x \cup y|}$

- nur die tatsächlich vorhandenen Attribute (mit 1 codiert) werden miteinander verglichen
- nicht-vorhandene Attribute bei beiden Datenpunkten werden ignoriert
- gleiches Bsp:
  - 3 Farben (rot, grün, blau)
  - x ist rot; y ist blau
  - Simple matching würde $\frac{1}{3}$ ergeben, weil ja beide gemeinsam haben **nicht** grün zu sein
  - Jaccard hingegen sagt Ähnlichkeit $\frac{0}{2}$, weil keines von zwei vorhandenen Attributen matched

### String-Attribute

freie Textfelder

#### Tokenization

!!!QUELLEN!!! [@cohen2003]

Bei nominalen Attributen mit vielen Ausprägungen (bsp Produkttitel => jeder ist anders)

- Zerlegen in einzelne Wörter => Tokenization
- Rückführung der Wörter auf ihren Stamm (z.B. Porter-Stemming)
- Entfernen von Füllwörtern => Stop-Word Removal

Am Ende erhalten wir eine feste Menge an Tokens oder Keywords => Menge kategorischen Daten => asymmetrisch binär verarbeiten

oder auch Überführung in Vektor-Space ...

#### String-Metrics (eventuell weglassen??)

!!!QUELLEN!!! [@cohen2003] [@rajalingam2011]

Alternativ kann Abstand auch mittels String-Metrics ermittelt werden.

String-Metrics messen die Ähnlichkeit zweier Strings

Bsp:

- Levenshtein: Anzahl an Buchstaben eingefügt/geändert/gelöscht um x auf y umzuwandeln
- Hamming: Anzahl an **ungleichen** Buchstaben => beide Strings müssen gleich lang sein
- Jaro: Verhältnis gleicher zu verschiedenen Buchstaben, performant mit guten Ergebnissen
- Jaro-Winkler: Erweiterung von Jaro mit höherem Gewicht auf den Anfang (Prefix) der Wörter

Verwendung:

- entweder String-Metrics selbst als Distanzmaß nutzen
- oder "ordinale" Reihenfolge mittels String-Metrics bestimmen und dann als ordinal betrachten

### Gemischte Attribute

[vgl. @kaufman2009; Kap. 1.2.6 Mixed Variables]

verschiedene Ansätze:

#### Umwandlung in numerische Werte

- siehe ordinal
- siehe nominal => String-Metrics

#### Umwandlung in kategorische Werte

- ordinal als nominal betrachten (siehe [Ordinale Attribute](#ordinale-attribute))
- numerisch Umwandeln durch Diskretisierung
  - Bildung von festen Bändern/Gruppen z.B. Alter => $10-19$, $20-29$ etc.

#### Separates Clustern je Attribut-Klasse und Subspace-Clustering

mehrmaliges Clustern mit jeweils nur Attributen eines Skalenniveaus

anschließend Vergleich der verschiedenen gebildeten Cluster

noch weitere komplexere Ansätze, wo verschiedenste Kombinationen an Attributen für das Clustern ausgewählt werden und verglichen werden => "Subspace-Clustering" [siehe @jia2017]

#### Kombinierte Distanzfunktion

Bewertung jedes Attributs mit geeignetem Distanzmaß. Anschließend zusammenrechnen mit Gleichgewichtung

ab hier aus [vgl. @huang1998]

z.B. bei [k-Prototype](#k-prototype) werden numerische und kategorische mit jeweils geeigneten Distanzmaßen verrechnet:

$d(x,y) = w d_numerical(x,y) + (1-w) d_categorical(x,y)$, also z.B. euklidisch und simple matching oder Manhattan und Jaccard etc.

$w$ soll eine Gleichgewichtung erzeugen also z.B. $\frac{Anzahl numerischer Attribute}{Anzahl aller Attribute}$

## Clustering-Verfahren

### Partitionierendes Clustering

#### Überblick

Minimierungsproblem: initiale Cluster-Zuordnungen (Partitionen), dann Veränderungen der Cluster-Zuordnungen bis ein lokales Minimum gefunden worden ist. [vgl. @king2015; Kap. 4.1 Introduction]

Verschiedene Algorithmen und Varianten: initiale Selection der Cluster, Wahl der Distanzmaße, Vorgehen während der Minimierung [vgl. @king2015; Kap. 4.1 Introduction] und für welche Arten von Attribute geeignet, dazu später mehr [siehe @huang1998]

Effizienz:

- neigt zu lokalen Minima => mehrmaliges Wiederholen des Clustering mit verschiedenen zufälligen Startpunkten
- dennoch sehr effizient lösbar: $\mathcal{O}(n \cdot k \cdot l)$
- $n$ Datenpunkte, $k$ Cluster, $l$ Wiederholungen des Clusterings
- $k$ und $l$ kleine Werte, viel kleiner als $n$
- also: $\mathcal{O}(n)$
- [vgl. @huang1998]

Aber: $k$ muss vorher bekannt sein => verschiedene $k$ probieren oder z.B. mit hierarchischem Verfahren $k$ abschätzen [vgl. @king2015; Kap. 4.1 Introduction]

#### k-Means

klassischster Vertreter des Clusterings und weit verbreitet und genutzt [vgl. @huang1998]

Jedes Cluster wird über einen Schwerpunkt (Mittelpunkt) repräsentiert [vgl. @steinbach2000]. Es gilt die Datenpunkte so den Clustern zuzuordnen, dass die Summe der Abstände der Datenpunkte zum Mittelpunkt so klein wie möglich sind. Schwerpunkt wird über Mittelwert (engl. mean) der Clustermitglieder bestimmt. [vgl. @king2015; Kap. 4.5 K-Means Algorithm]

Funktioniert daher nur mit numerischen Werten [vgl. @huang1998]

Ablauf [vgl. @king2015; Kap. 4.5 K-Means Algorithm]:

1. Wahl der initialen $k$ Startpunkte
2. Zuordnen aller Datenpunkte zum nächstliegenden Schwerpunkt
3. Neuberechnung der Schwerpunkte mittels Durchschnittswert (engl. mean) der Datenpunkte
4. ab 2. wiederholen, solange bis keine/kaum noch Änderungen der Schwerpunkte

Für Wahl der initialen Schwerpunkte [vgl. @king2015; Kap. 4.3 The Initial Partition]:

- ersten $k$ Datenpunkte
- oder gleichmäßig aus der gesamten Liste
- oder zufällig über gesamte Liste
- und weitere

z.B. mehrmals mit verschiedenen random Startpunkten durchführen und bestes Ergebnis nehmen => verteilte Berechnung möglich

Statt die Schwerpunkte nur einmal am Ende eines Durchlaufes neuberechnen (Forgy's Method) auch permanente Neuberechnung (mit jedem neu zugeordnetem Datenpunkt) möglich (MacQueen's Method) und weitere Abwandlungen [vgl. @king2015; Kap. 4.5 K-Means Algorithm]

#### k-Medoids

[@arora2016]

- Variante des k-Means
- median statt mean als Clusterschwerpunkte
- median Berechnung komplexer, da Abstand aller Punkte eines Clusters zueinander berechnet werden muss
- aber laut Autor bessere Ergebnisse, schnellere Konvergenz und dadurch trotzdem kürzere Rechenzeit

#### k-Modes

[@huang1998]

Variante des k-Means für kategorische (Attribute)

Änderungen zum k-Means:

- Simple matching als Distanzmaß (allerdings auch andere z.B. Jaccard möglich)
- statt Durchschnittswertes (engl. mean) wird Clusterschwerpunkt aus dem Modus (engl. mode) bestimmt
- Update der modes eines Clusters während des Clustering anhand ihrer Häufigkeit (Frequenz)

nach einem Durchlauf, Set erneut durchgehen und checken, ob einige Punkte nicht einem anderen Cluster zugeordnet werden müssen, da sich Modus des Datensets während des Clusterns ja häufig ändert. nach Reassign => Modus Frequenz in beiden Clustern anpassen

#### k-Prototype

[@huang1998]

Kombi aus k-means und k-modes für gemischte Datensets

nutzt ein Distanzmaß für numerische und eins für kategorische Werte + Gewicht zur gleichgewichtung der Attribute [siehe gemischte Attribute](#gemischte-attribute)

Schwerpunkt der numerische Attribute ist der Durchschnitt (mean) und der nominalen ist der Modus (mode) => also Kombi aus beiden

### Hierarchisches Clustering

#### Überblick

!!!QUELLEN!!!

schrittweise Zuordnung zu Clustern => top-down (divisive) oder bottom-up (agglomerative)

Visualisierung: Dendogramm

Vorteil: $k$ muss vorher nicht bekannt sein, sondern Hierarchie mit beliebiger Feinheit, Erkenntnisse aus Kind- und Vater-Clustern

Nachteile: einmal kombiniert/geteilt kein Reassignment der Cluster mehr, teilweise seltsame Ergebnisse, Fehler ziehen sich immer weiter durch

rechenintensiv: Vergleich von jedem Datenpunkt mit jedem anderen Datenpunkt, also mindestens $\mathcal{O}(n^2)$
meistens noch aufwendiger, da Datenset $k$ mal durchsucht werden muss. Da hierarchisch ist $k \approx n$, also meistens $\mathcal{O}(n^2 \log n)$ (mit Optimierungen) bzw. $\mathcal{O}(n^3)$

#### Agglomeratives Clustering (Bottom-Up)

!!!QUELLEN!!!

Ablauf:

1. alle Datenpunkte in einem eigenen Cluster
2. Ermittlung der beiden am nächsten gelegenen Cluster
3. Fusion dieser beiden Cluster zu einem größeren
4. ab 2. wiederholen bis alle Punkte in einem Cluster sind

Theoretisch könnte auch vorher abgebrochen werden, aber für den Anwender sind i.d.R. die obersten "größten" Cluster-Hierarchien am interessantesten

zentrale Frage: wie werden zwei Cluster mit mehreren Datenpunkten miteinander verglichen => Linkage

Bsp immer die beiden dichtesten Datenpunkt beider Cluster => Single-Link

| Name | Formell | Beschreibung | Eigenschaften |
|-|-|--|---|
| Single-Link | $d(X,Y) = \min d(x_i, y_j)$ | Abstand durch die beiden dichtesten Punkte definiert | neigt zur Bildung von langen Ketten (chaining effect), anfällig gegen Outlier |
| Complete-Link | $d(X,Y) = \max d(x_i, y_j)$ | Abstand durch die beiden am entferntesten liegenden Punkte definiert | neigt zur Bildung von vielen sehr kleinen Clustern, anfällig gegen Outlier |
| Average-Link | $d(X,Y) = \textrm{avg } d(x_i, y_j)$ | durchschnittlicher Abstand aller Punkte der beiden Cluster zueinander | ähnlich dem Mittelpunkt von k-Means, aber viel aufwendiger, da immerzu jeder Punkt eines Clusters mit jedem anderen Punkt der anderen Clustern verglichen werden muss |
| Mediod-Link | $d(X,Y) = ...$ | Median Punkt eines Cluster repräsentiert das Cluster | ähnliches Verhalten wie Average-Link, aber effizienter zu berechnen, da der Median eines neu gebildeten Clusters nur einmal bestimmt werden muss |
| k-Centroid-Link ??? | $d(X,Y) = ...$ | vergleicht den Durchschnitt der $k$ zentralsten Punkte der Cluster miteinander; allgemeine Form von Mediod-Link ($k=1$) und Average-Link ($k=|C|$) | liegt je nach $k$ irgendwo zwischen Average- und Mediod-Link; $k$ ist ein weiterer Parameter, der festgelegt werden muss |
| Ward-Method | $d(X,Y) = \frac{d(\bar{x}, \bar{y})^2}{\frac{1}{|X|} + \frac{1}{|Y|}}$ | berechnet die Varianz für jedem potenziellen Merge, Merge mit höchster Reduktion der Varianz wird ausgewählt | sehr aufwendig zu berechnen, da immer wieder jeder Punkt mit jedem anderen verrechnet werden muss |

Insgesamt alle sehr rechenintensiv. single- und complete-link bei guter Implementierung in $\mathcal{O}(n^2)$,
alle anderen mindestens in $\mathcal{O}(n^2 \log n)$ oder $\mathcal{O}(n^3)$ (vor allem bei Average-Link und Ward-Method)

#### Diversives Clustering (Top-Down)

##### Überblick

ergibt für Menschen intuitivere Cluster, da wir ebenfalls mental so vorgehen [vgl. @king2015; Kap. 3.3 Agglomerative versus Divisive Clustering]

theoretisch weniger aufwendig als agglomerativ, wenn nicht komplette Hierarchie generiert wird
=> weniger Durchläufe da i.d.R. $k < n-k$ (von 1 Cluster zu $k$ weniger Schritte als von $n$ zu $k$ Clustern)

Problem: erstes Cluster riesig groß mit theoretisch $2^{n-1}-1$ möglichen Arten des Splitterns (also $\mathcal{O}(2^n)$)

in der Praxis wird dieses Problem durch geschicktes Vorgehen umgangen:

##### DIANA

[vgl. @kaufman2009; Kap. Divisive Analysis (Program DIANA)]

klassisches, erstes Verfahren, wie Abspaltung bei einer Partei

Ablauf:

1. Start mit allen Punkten in einem großen Cluster
2. Berechnung der durchschnittlichen Abweichung aller Punkte voneinander
3. Punkt mit größter Abweichung => Startpunkt einer "Splittergruppe"
4. Berechnung der durchschnittlichen Abweichung ohne Punkt mit größter Abweichung
5. Differenz der beiden Abweichungen größer geworden und am größten => Punkt der "Splittergruppe" zuordnen
6. wiederholen 4. bis Differenzen nur noch negativ
7. Durchmesser der Cluster berechnen $\emptyset = \max d(x, y)$
8. Cluster mit größtem Durchmesser verwenden und ab 2. wiederholen, bis gewünschte Abbruchbedingung erreicht ist

Abbruchbedingung kann bestimmter Durchmesser sein oder ein festes $k$, spätestens Schluss, wenn $k=n$

Laufzeit (eigene Überlegung; kleiner Kommentar dazu in [@steinbach2000])

- Berechnung der durchschnittlichen Abweichung: jeder Punkt mit jedem anderen vergleichen => $\mathcal{O}(n^2)$
- da Cluster immer kleiner werden, wird Berechnung mit jedem Schritt einfacher

[@rajalingam2011] Versuche mit agglomerativ und divisive nach DIANA => DIANA immer doppelt so schnell fertig für das gesamte Datenset

##### Bisecting k-Means

[vgl. @steinbach2000]

zur Teilung des größten Clusters wird k-Means mit $k=2$ genutzt

- dadurch viel effizienter da k-Means in $\mathcal{O}(n)$
- k-Means wird zwar $k$ mal aufgerufen, aber gleichzeitig wird die Anzahl der Datenpunkte je Cluster mit jeder Teilung kleiner


## Cluster Validität

[@king2015; Kap. 8.1 Introduction] => fehlerbehaftet ... ???

unsupervised learning, dennoch Analyse, ob gefundene Cluster gut sind

[@rendon2011]

Clustering validation prüfen, ob Cluster eine gute/natürliche Partition sind, Prüfung durch indices

3 Ansätze:

1. Internal Indices: nur Verwendung der Daten des Datensets selbst
2. External Indices: Vergleich mit externen Daten z.B. extern festgelegten Clustern
3. Relative Indices: Vergleich der Ergebnisse verschiedener Clustering Durchläufe miteinander

[@king2015; Kap. 8.1 Introduction]

Wenn keine externen Daten verfügbar => z.B. Monte-Carlo-Simulationen zur Evaluation durchführen => nicht weiter betrachtet, da externe Daten vorhanden sind

### Internal Indices

[@steinbach2000]

- Overall Similarity  ...
- $\sum d(C_xi, C_xj) / |C|$
- oder $\textrm{cosine}()$ ?
- ...

[@rendon2011]

- Dunn index
- Silhouette index
- Bayesian Information Criterion
- ...

### External Indices

[@king2015; Kap. 8.4 Indices of Cluster Validity]

- Rand Index => ähnlich simple matching nur aus Sicht der Cluster
- Jaccard => nur aus Sicht der Cluster
- Abwandlungen davon ...

[@rendon2011]

- Purity => Gegenstück zur Entropy
- Normalized Mutual Information (NMI) Measure

[@rendon2011] & [@steinbach2000]

- Entropy => "Varianz der extern zugeordneten Klassen je Cluster"
- F-measure => Betrachtung der Cluster als "Such-Queries"

# Clusteranalyse

## Begriff und Einordnung

King definiert die *Clusteranalyse* als die "[...] Generierung eines Klassifizierungsschemas, welches Individuen in eine feste Anzahl an Gruppen einteilt, so dass sich die Individuen innerhalb einer Gruppe auf eine Art und Weise ähnlich sind und unähnlich denen in anderen Gruppen" [@king2015, Kap. 1.1 What Is a Cluster?]. Diese Gruppen werden auch als Cluster bezeichnet.

Dieser Prozess des Clustering ist eine Methode des *unüberwachten Lernens (unsupervised learning)* – einem Teilgebiet des maschinellen Lernens. Papp et al. schreiben dazu: "Machine Learning beschäftigt sich mit der Entwicklung von Methoden, die Modelle von Zusammenhängen aus Daten erlernen, anstatt sie *per Hand* zu implementieren" [@papp2019, Kap. 5 Statistik-Grundlagen]. Ferner geben sie an, dass die Unterschiede zur Statistik fließend sind [@papp2019, Kap. 5 Statistik-Grundlagen]. Unüberwachtes Lernen bedeutet dabei, dass die verwendeten Daten nicht im Vorhinein gekennzeichnet sind (Unlabeled Data). Stattdessen werden Ähnlichkeiten und Muster in den Daten selbst gesucht ohne eine vorgegebene Zielgröße. Häufig dienen diese Analysen als erste Schritte der *Data Exploration* aus denen im Anschluss neue Erkenntnisse und Anwendungen abgeleitet werden. [@papp2019, Kap. 5.2.3 Unüberwachtes Lernen]

Allgemein wird die Clusteranalyse als eine Form des Data Minings gesehen. Laut Bissantz und Hagedorn "beschreibt [Data Mining] die Extraktion implizit vorhandenen, nicht trivialen und nützlichen Wissens aus großen, dynamischen, relativ komplex strukturierten Datenbeständen" [@bissantz2009]. Mit "Wissen" meinen sie dabei in den Daten implizit enthaltene Muster, welche für den Anwender interessant sind und mit einer hinreichenden Wahrscheinlichkeit tatsächlich in den Daten existieren. [@bissantz2009]

## Notation

Bevor konkrete Algorithmen und Verfahren der Clusteranalyse vorgestellt werden, müssen einige grundlegende Sachverhalte und ihre mathematische Definition geklärt werden:

Die Objekte, welche es zu clustern gilt, werden in dieser Arbeit auch als *Datenpunkte* oder *Produkte* (da dies die Anwendung im Praxisteil ist) bezeichnet. Mathematisch werden sie i.d.R. mittels $x$ definiert.

Diese Produkte bestehen aus einer festen Menge an Attributen (z.B. Farbe, Gewicht etc.). Mathematisch ist so ein Datenpunkt als ein Vektor definiert und jedes Element im Vektor steht für die Ausprägung eines spezifischen Attributes $x=(a | a \text{is attribute})$. Mittels Superskript werden spezifische Attribute eines Datenpunktes angesprochen. $x^i$ bezeichnet also das $i$-te Attribut von $x$.

Die Produkte oder Datenpunkte sind Teil eines *Datensets* $X$. Hierbei handelt es sich um eine simple Menge dieser Datenpunkte $x \in X$. Mittels Subskript werden einzelne Punkte des Sets angesprochen (z.B. $x_1$, $x_2$ oder $x_i$). Wenn nicht anders angegeben gilt $n=|X|$.

Als *Cluster* $C$ wird nun eine Teilgruppen aus dem Datenset bezeichnet: $C \subset X$. Allerdings Cluster auch "hierarchisch" strukturiert sein. D.h. ein Cluster kann sowohl Datenpunkte als auch andere Cluster enthalten. $C = {e | e = C_i \vee x \in X}$.

Die *Menge aller Cluster* wird mit $K = {C_1, C_2, ...}$ bezeichnet. Dabei wird die Anzahl der Cluster mit $k = |K|$ angegeben.

Schlussendlich gibt es noch das *Clustering-Ergebnis* $Y$. Dies ist ein Vektor der Länge $n$, welches jeden Datenpunkt im Set einem entsprechenden Cluster zuordnet: $Y = (l | l_i = \text{ label for } x_i \in X)$

## Distanz- und Ähnlichkeitsmaße

### Definition

Die Forderung, dass Objekte in gleichen Clustern sich "ähnlich" sein sollen und unähnlich zu den Objekten in anderen Clustern, muss in irgendeiner Form quantifiziert werden. Dies erfolgt über die Berechnung der "Nähe" (engl. proximity) der Objekte zueinander. Dazu werden sog. Abstands- bzw. Distanzmaße verwendet. [@kaufman2009, Kap. 1.2 Types of Data and How to Handle Them]

Mathematisch wird dieses Distanzmaß mittels der Funktion $d(x_1,x_2)$ (engl. distance) definiert, welche die Distanz zwischen zwei Datenpunkten $x_1$ und $x_2$ als skalaren Wert zurückgibt. Zusätzlich geben Kaufmann und Rousseeuw folgende Eigenschaften für $d$ an [@kaufman2009, Kap. 1.2.1 Interval-Scaled Variables]:

||||
|-|---------------|-------------------|
| 1. | $d(x_1,x_2) \geq 0$ | Distanzen sind stets positiv |
| 2. | $d(x_1,x_1) = 0$ | zwei gleiche Objekte haben immer einen Abstand von $0$ |
| 3. | $d(x_1,x_2) = d(x_2,x_1)$ | die Distanzfunktion ist kommutativ bzw. symmetrisch |
| 4. | $d(x_1,x_3) \leq d(x_1,x_2) + d(x_2,x_3)$ | Distanzen geben stets den kürzesten Weg an |
: Eigenschaften der Abstandfunktion $d$

Anstatt des Abstandes kann alternativ auch die Ähnlichkeit zweier Objekte berechnet werden. Solche Ähnlichkeitsmaßes $s(x_1,x_2)$ (engl. similarity) sind häufig im Interval $[0;1]$ angegeben, wobei die $1$ maximale Ähnlichkeit angibt. Ist nun eine entsprechende Distanzfunktion z.B. durch Normalisierung ebenfalls im Interval $[0;1]$ definiert, so können Distanzen und Ähnlichkeiten einfach ineinander überführt werden [@kaufman2009, Kap. 1.2.3 Similarities]:

\begin{equation}
  d(x_1,x_2) = 1 - s(x_1,x_2)
\end{equation}

Distanzen und Ähnlichkeiten sind dadurch beliebig austauschbar. Daher ist dieses Vorgehen stets empfehlenswert.

Es existieren eine Vielzahl an Distanz- und Ähnlichkeitsmaßen. Welche zur Anwendung kommen, hängt maßgeblich von den Attributen und vor allem den Attribut-Typen ab, aus denen die Datenpunkte bestehen. [@kaufman2009, Kap. 1.2 Types of Data and How to Handle Them]

### Numerische Attribute

Numerische Attribute sind im Allgemeinen alle Arten von (rationale) Zahlen [@kaufman2009, Kap. 1.2 Types of Data and How to Handle Them] mit stetigen (engl. continuous) Werten [@huang1998]. Es kann sich dabei sowohl um Intervall- als auch um Verhältnisskalen handeln (engl. interval and ratio data). [@boslaugh2012, Kap. 1 Basic Concepts of Measurement]

Datenpunkte, die nur aus numerischen Attributen bestehen, sind die klassischste Form von Daten, mit denen Clusteranalyse durchgeführt wird. Die meisten Algorithmen und Verfahren sind damit speziell auf diesen Attribut-Typ ausgelegt. [@king2015, Kap. 1.2 Capturing the Clusters]

#### Minkowski-Familie

Der Abstand zwischen reinen numerischen Vektoren wird mittels Maßen aus der sog. Minkowski-Familie berechnet. Das älteste dieser Metriken ist der "euklidische" Abstand (auch pythagoreische Metrik genannt), welcher den Abstand zwischen zwei Punkten über eine gerade Linie zwischen diesen beiden bestimmt. Im 19. Jahrhundert verallgemeinerte Hermann Minkowski dieses Maß zu einer ganzen Familie. [@cha2007]

| Name | $p$-Norm | Formell |
|-|-|---|
| Minkowski | allgemein | $d(x,y) = \sqrt[p]{\sum_{i=1}^n |x_i - y_i|^p}$ |
| Manhattan | $p=1$ | $d(x,y) = \sum_{i=1}^n |x_i - y_i|$ |
| euklidisch | $p=2$ | $d(x,y) = \sqrt{\sum_{i=1}^n |x_i - y_i|^2}$ |
| Chebyshev | $p=\infty$ | $d(x,y) = \max |x_i - y_i|$ |
: Übersicht über die gängigen Maße aus der Minkowski-Familie [@cha2007]

Die allgemeine Form ist über den Ausdruck $p$ parametrisiert. Die konkreten Vertreter der Familie kommen nun durch ein spezifisch gewähltes $p$ zustande. Daher wird bei diesen Maßen auch von der sog. $p$-Norm gesprochen. Eine höhere $p$-Norm steht dabei im Allgemeinen für eine robustere bzw. eindeutigere Bestimmung des Abstandes. [@king2015, Kap. 12.3 Which Proximity Measure Should Be Used?]

Dies sind bei weitem nicht alle Arten von Maßen für numerische Attribute. Cha [@cha2007] hat eine Vielzahl solcher Maße zusammengetragen, analysiert und miteinander verglichen. Dabei kam er zu folgenden Erkenntnissen:

Die meisten dieser Maße sind Abwandlungen eines Vertreters aus der Minkowski-Familie bzw. lassen sich auf einen solchen abbilden (z.B. basieren einige Maße auf der Pearson-Korrelation, welche ihrerseits wieder auf dem euklidischen Abstand beruht). In seinen anschließenden Versuchen zeigte er, dass Maße, die auf einander basieren, auch stets ähnliche Abstände liefern. [@cha2007]

Daraus lässt sich ableiten, dass die Vertreter der Minkowski-Familie ausreichend sind, um den Abstand numerischer Vektoren zu bestimmen.

#### Standardisierung

Häufig macht eine Vorverarbeitung der numerischen Attribute Sinn, um bestimmte Probleme zu vermeiden. [@kaufman2009, Kap. 1.2.1 Interval-Scaled Variables]

Die Abstandsmaße der Minkowski-Familie gehen i.d.R. von linearen Verhältnissen der Zahlen zueinander aus (Punkte mit einem Abstand von $2$ sind doppelt so weit entfernt, wie Punkte mit einem Abstand von $1$). Es kann aber vorkommen, dass die vorliegenden Daten eigentlich einen logarithmischen Zusammenhang aufweisen (der Abstand von $10$ zu $20$ ist exakt gleichbedeutend mit dem Abstand von $100$ zu $200$). Damit die Abstandsmaße richtig arbeiten können, sollten solche Attribute vorher in eine lineare Abbildung überführt werden [@kaufman2009, Kap. 1.2.5 Nominal, Ordinal, and Ratio Variables]. Dies wird folgendermaßen bewerkstelligt:

\begin{equation}
  x^{i'} = \log x^i
\end{equation}

Weiterhin können Probleme entstehen, wenn die absoluten Werte in den verschiedenen Dimensionen der Vektoren stark voneinander abweichen. Angenommen das Datenset besteht aus zwei-dimensionalen Vektoren. Die Werte in der ersten Dimension liegen im Bereich $[0;1]$ und in der zweiten im Bereich $[100;200]$. Dadurch würden die Unterschiede zwischen den Werten in der zweiten Dimension viel stärker ins Gewicht fallen, da hier Differenzen von $100$ und mehr entstehen können. Um hier eine Gleichgewichtung zu erzeugen, sollten die Attribute jeweils auf das gleiche Interval abgebildet werden [@kaufman2009, Kap. 1.2.1 Interval-Scaled Variables].

Für diese *Standardisierung* empfehlen Kaufmann und Rousseeuw die Berechnung des sog. z-Scores, welcher sich wie folgt berechnet:

\begin{align}
  x^{i'} &= \frac{x^i - \textrm{avg }X^i}{mad(X^i)}
  mad(X^i) &= \frac{1}{n} \sum_j |x^i_j - \textrm{avg }X^i|
\end{align}

$X^i$ bezeichnet alle vorkommenden Werte des jeweiligen Attributes. $mad(X^i)$ ist die mittlere absolute Abweichung (engl. *mean absolute deviation*). Dieser z-Score zentriert die vorkommenden Werte um die $0$ im Interval $[-1;1]$. Zusätzlich dämpft er den Einfluss von Outliers, also Werten die sehr weit am Rande des Spektrums liegen. Diese würden sonst dazu führen, dass die meisten Werte in die Mitte des Intervals komprimiert werden, anstatt sie gleichmäßig über das gesamte Interval zu verteilen. [@kaufman2009, Kap. 1.2.1 Interval-Scaled Variables]

Kaufmann und Rousseeuw geben zu bedenken, dass die unterschiedlichen Gewichtungen der Werte echte Zusammenhänge der realen Welt widerspiegeln könnten. Durch Standardisierung gehen diese entsprechend verloren. Weiterhin ist sogar denkbar, bewusst einige Attribute stärker zu gewichten als anderen (indem sie mit entsprechenden Gewichten multipliziert werden). Dies sind allerdings eher speziellere Fälle, in denen im Vorfeld bereits Domänenwissen zum Datenset vorliegen muss. [@kaufman2009, Kap. 1.2.1 Interval-Scaled Variables]

### Kategorische Attribute

Kategorische Attribute bilden die zweite große Gruppe von Attribut-Typen. Sie zeichnen sich dadurch aus, dass als Wertausprägungen Labels verwendet werden, die verschiedene Kategorien repräsentieren. Diese Labels können in Form von Zeichenketten (z.B. "red", "green", "blue"), Bool-Werten ($true$/$false$, Ja/Nein, $0$/$1$) oder auch diskreten Ziffern auftreten. Es ist ein weitere Unterscheidung in die zwei Teilgruppen ordinale und nominale Attribute möglich. [@boslaugh2012, Kap. 5 Categorical Data]

#### Ordinale Attribute

Lassen sich die vorkommenden Labels eines Attributes in eine sinnvolle Reihenfolge bringen (z.B. "XS", "S", "M", "L", "XL"), so werden sie als *ordinal* bezeichnet. Wichtig dabei ist, dass nur eine sinnvolle Reihenfolge besteht. Eine Aussage über Intervalle zwischen den Labels ("XS" bis "S" ist genauso weit wie "M" zu "L") oder über deren quantitativen Verhältnisse ($3$"XS"$=2$"S") macht aber keinen Sinn. [@boslaugh2012, Kap. 1 Basic Concepts of Measurement]

Für die Berechnung das Abstandes gibt es grundsätzlich zwei Möglichkeiten: Zum einen können ordinale Attribute genauso wie nominale verarbeitet werden (siehe nächster Abschnitt). Zum anderen kann die Reihenfolge der Labels verwendet werden, um die Labels in numerische Werte umzuwandeln. Anschließend kann der Abstand mittels der Maße für numerische Attribute berechnet werden. [@kaufman2009, Kap. 1.2.5 Nominal, Ordinal, and Ratio Variables]

Die Umwandlung erfolgt dabei so, dass die Labels entsprechend ihrer natürlichen Reihenfolge beginnend mit $1$ nummeriert werden. Der finale numerische Wert berechnet sich dann wie folgt:

\begin{equation}
  x^{i'} = \frac{x^i - 1}{|{X^i}| - 1}
\end{equation}

$|{X^i}|$ ist dabei die Menge an auftretenden Labels. Dadurch liegen alle Werte erneut im Interval $[0;1]$, welches in $|{X^i}| - 1$ gleichmäßige Schritte unterteilt ist. [@kaufman2009, Kap. 1.2.5 Nominal, Ordinal, and Ratio Variables]

#### Nominale Attribute

dieser Teil aus [@kaufman2009, Kap. 1.2.5 Nominal, Ordinal, and Ratio Variables]

Umwandlung in sog. binäre Attribute:

1. bei 2 Ausprägungen => $0=\text{erste Ausprägung}$, $1=\text{zweite Ausprägung}$ z.B. yes/no
2. ab 3 =>
  - entweder in 2 Ausprägungen komprimieren
  - oder ein neues Attribut pro Kategorie definieren: $0=\text{gehört nicht zur Kategorie}$, $1=\text{gehört zur Kategorie}$

folgende aus [@kaufman2009, Kap. 1.2.5 Binary Variables]

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

[@cohen2003]

Bei nominalen Attributen mit vielen Ausprägungen (bsp Produkttitel => jeder ist anders)

- Zerlegen in einzelne Wörter => Tokenization
- Rückführung der Wörter auf ihren Stamm (z.B. Porter-Stemming)
- Entfernen von Füllwörtern => Stop-Word Removal

Am Ende erhalten wir eine feste Menge an Tokens oder Keywords => Menge kategorischen Daten => asymmetrisch binär verarbeiten

oder auch Überführung in Vektor-Space ...

#### String-Metrics

[@cohen2003] [@rajalingam2011]

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

[@kaufman2009, Kap. 1.2.6 Mixed Variables]

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

ab hier aus [@huang1998]

z.B. bei [k-Prototype](#k-prototype) werden numerische und kategorische mit jeweils geeigneten Distanzmaßen verrechnet:

$d(x,y) = w d_numerical(x,y) + (1-w) d_categorical(x,y)$, also z.B. euklidisch und simple matching oder Manhattan und Jaccard etc.

$w$ soll eine Gleichgewichtung erzeugen also z.B. $\frac{Anzahl numerischer Attribute}{Anzahl aller Attribute}$

## Clustering-Verfahren

### Partitionierendes Clustering

#### Überblick

Minimierungsproblem: initiale Cluster-Zuordnungen (Partitionen), dann Veränderungen der Cluster-Zuordnungen bis ein lokales Minimum gefunden worden ist. [@king2015, Kap. 4.1 Introduction]

Verschiedene Algorithmen und Varianten: initiale Selection der Cluster, Wahl der Distanzmaße, Vorgehen während der Minimierung [@king2015, Kap. 4.1 Introduction] und für welche Arten von Attribute geeignet, dazu später mehr [siehe @huang1998]

Effizienz:

- neigt zu lokalen Minima => mehrmaliges Wiederholen des Clustering mit verschiedenen zufälligen Startpunkten
- dennoch sehr effizient lösbar: $\mathcal{O}(n \cdot k \cdot l)$
- $n$ Datenpunkte, $k$ Cluster, $l$ Wiederholungen des Clusterings
- $k$ und $l$ kleine Werte, viel kleiner als $n$
- also: $\mathcal{O}(n)$
- [@huang1998]

Aber: $k$ muss vorher bekannt sein => verschiedene $k$ probieren oder z.B. mit hierarchischem Verfahren $k$ abschätzen [@king2015, Kap. 4.1 Introduction]

#### k-Means

klassischster Vertreter des Clusterings und weit verbreitet und genutzt [@huang1998]

Jedes Cluster wird über einen Schwerpunkt (Mittelpunkt) repräsentiert [@steinbach2000]. Es gilt die Datenpunkte so den Clustern zuzuordnen, dass die Summe der Abstände der Datenpunkte zum Mittelpunkt so klein wie möglich sind. Schwerpunkt wird über Mittelwert (engl. mean) der Clustermitglieder bestimmt. [@king2015, Kap. 4.5 K-Means Algorithm]

Funktioniert daher nur mit numerischen Werten [@huang1998]

Ablauf [@king2015, Kap. 4.5 K-Means Algorithm]:

1. Wahl der initialen $k$ Startpunkte
2. Zuordnen aller Datenpunkte zum nächstliegenden Schwerpunkt
3. Neuberechnung der Schwerpunkte mittels Durchschnittswert (engl. mean) der Datenpunkte
4. ab 2. wiederholen, solange bis keine/kaum noch Änderungen der Schwerpunkte

Für Wahl der initialen Schwerpunkte [@king2015, Kap. 4.3 The Initial Partition]:

- ersten $k$ Datenpunkte
- oder gleichmäßig aus der gesamten Liste
- oder zufällig über gesamte Liste
- und weitere

z.B. mehrmals mit verschiedenen random Startpunkten durchführen und bestes Ergebnis nehmen => verteilte Berechnung möglich

Statt die Schwerpunkte nur einmal am Ende eines Durchlaufes neuberechnen (Forgy's Method) auch permanente Neuberechnung (mit jedem neu zugeordnetem Datenpunkt) möglich (MacQueen's Method) und weitere Abwandlungen [@king2015, Kap. 4.5 K-Means Algorithm]

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

#### k-Prototypes

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

ergibt für Menschen intuitivere Cluster, da wir ebenfalls mental so vorgehen [@king2015, Kap. 3.3 Agglomerative versus Divisive Clustering]

theoretisch weniger aufwendig als agglomerativ, wenn nicht komplette Hierarchie generiert wird
=> weniger Durchläufe da i.d.R. $k < n-k$ (von 1 Cluster zu $k$ weniger Schritte als von $n$ zu $k$ Clustern)

Problem: erstes Cluster riesig groß mit theoretisch $2^{n-1}-1$ möglichen Arten des Splitterns (also $\mathcal{O}(2^n)$)

in der Praxis wird dieses Problem durch geschicktes Vorgehen umgangen:

##### DIANA

[@kaufman2009, Kap. Divisive Analysis (Program DIANA)]

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

[@steinbach2000]

zur Teilung des größten Clusters wird k-Means mit $k=2$ genutzt

- dadurch viel effizienter da k-Means in $\mathcal{O}(n)$
- k-Means wird zwar $k$ mal aufgerufen, aber gleichzeitig wird die Anzahl der Datenpunkte je Cluster mit jeder Teilung kleiner

## Cluster-Validität

### Überblick

Die Clusteranalyse selbst ist ein Verfahren des unüberwachten Lernens und findet interne Muster in Daten ohne Referenz zu externen Zuweisungen (Labels). Dennoch finden verschiedene Clusteringverfahren unterschiedliche Gruppenzuteilungen. Auch die verschiedenen Parameter, die für ein jeweiliges Clusteringverfahren gesetzt werden, beeinflussen das Ergebnis. Daher bedarf es Methoden zur Evaluation und Vergleich der Clusterings miteinander. [@rendon2011]

**Externe Indizes** (engl. External Indices) sind Metriken, welche die berechnete Gruppenzuteilung mit einer extern vorgegeben Zuteilung vergleicht. Das heißt, es gibt eine erwartete Art der Gruppierung, welche nicht Teil des Datensets selbst ist. Diese Indizes messen nun den Grad der Übereinstimmung zwischen berechnetem und gewünschten Clustering-Ergebnis. [@rendon2011]

**Interne Indizes** (engl. Internal Indices) messen die Qualität des Clusterings ohne externe Informationen. Die Cluster sollten möglichst "kompakt" gruppiert und die verschiedenen Gruppen "gut von einander getrennt" sein. Diese Indizes versuchen diese Anforderungen zu quantifizieren. [@rendon2011; und @king2015, Kap. 8.1. Cluster Validity – Introduction]

Die **Stabilität** ist ebenfalls ein wichtiger Faktor. Hierbei wird das Datenset mehrmals mit verschiedenen Modifikationen geclustert. Solche Modifikationen können die Änderung einzelner Werte oder das Weglassen ganzer Spalten sein. Ein "stabiles" Clustering erzeugt auch mit diesen Veränderungen ähnliche Ergebnisse. Für die konkrete Bewertung der Stabilität werden externe oder interne Indizes verwendet und ihre Ergebnisse über die verschiedenen Clusterings miteinander verglichen. [@king2015, Kap. 8.1. Cluster Validity – Introduction]

Manche Autoren (z.B. [@rendon2011] und auch [@king2015]) führen formal noch sog. **Relative Inidzes** an. Hiermit wird die Performance verschiedener Clustering-Verfahren und verschiedener Meta-Parameter der Clusterings über das gleiche Datenset verglichen. In der Praxis erfolgt dies aber stets über den Vergleich der externen oder internen Indizes der Clustering-Ergebnisse miteinander.

### External Indices

#### Überblick

Zur Bewertung der Übereinstimmung zweier Clustering-Ergebnisse können grundsätzlich Metriken aus dem Bereich der Klassifikation verwendet werden [@hubert1985]. Beispiele dafür wären Maße wie die Entropie oder ihr Gegensatz die Reinheit (engl. Purity), welche analysieren, wie viele falsche zu richtigen Zuordnungen innerhalb einer Klasse aufgetreten sind [@rendon2011]. Ebenso das F-Maß (engl. F-Measure), welches aus dem Bereich des Document Retrievals bekannt ist. Es simuliert durchgeführte "Suchen" und vergleicht die gefundenen mit den erwarteten Suchergebnissen [@rendon2011; und @steinbach2000].

Das Problem mit diesen Maßen ist, dass die Benennung der Labels im Ergebnis von entscheidender Bedeutung in der Bewertung ist. Nehmen wir an, wir haben ein Datenset $X$ mit vier Datenpunkten. Die berechnete Clusterzuordnung ist $Y = (0, 0, 1, 1)$ und die erwartete Zuordnung ist $Y' = (1, 1, 0, 0)$. Metriken der Klassifikation würden eine Übereinstimmung von null Prozent feststellen, da keines der Labels in $Y$ und $Y'$ den gleichen Klassen zugeordnet worden ist. Im Kontext der Clusteranalyse weisen $Y$ und $Y'$ aber eine perfekte Übereinstimmung auf, denn es geht alleine um die Zuordnung der Datenpunkte in die gleichen Gruppen. Wie diese Gruppen benannt werden (in diesem Beispiel $0$ und $1$), spielt dabei keine Rolle. Daher sind für die Clusteranalyse eigene Metriken entwickelt worden, welche unabhängig von der Benennung der Labels die Übereinstimmung zwischen den Zuordnungen berechnen können. [@rand1971; und @hubert1985]

#### Rand-Index

Der Rand-Index war einer der ersten Metriken, die speziell für die Clusteranalyse entwickelt worden sind [@king2015, Kap. 8.4 Indices of Cluster Validity]. William M. Rand veröffentlichte dieses Maß 1971 [@rand1971] und es ist immer noch eines der populärsten und weitverbreitetsten (bzw. vor allem die Verbesserungen dieses Indexes siehe nächster Abschnitt). [@hubert1985; und @steinley2004]

Um unabhängig von der Benennung der Labels zu werden, vergleicht man nicht wie in der Klassifikation die gefundenen Labels eins zu eins miteinander. Stattdessen werden alle möglichen Paarungen der Datenpunkte in $X$ betrachtet und die Zuordnung der Paare in $Y$ und $Y'$ miteinander verglichen. [@rand1971]

| $Y$ \\ $Y'$ | Paar im gleichen Cluster | Paar in anderem Cluster |
|-|:-:|:-:|
| Paar im gleichen Cluster | $a$ | $b$ |
| Paar in anderem Cluster | $c$ | $d$ |

: Kontingenz der Datenpunkt-Paare in $Y$ und $Y'$ [@steinley2004]

Die Tabelle zeigt die möglichen Fälle: Ein Paar aus Datenpunkten kann entweder dem gleichen Cluster oder zwei unterschiedlichen Clustern zugeordnet worden sein. Haben sowohl $Y$ als auch $Y'$ das Paar jeweils in das gleiche Cluster (mit dem gleichen Label wie auch immer dieses benannt ist) zugordnet, so wird dieses Paar zu $a$ gezählt. Haben beide jeweils ein unterschiedliches Cluster zugeordnet, so wird das Paar in $d$ gezählt usw. [@steinley2004]

\begin{equation}
  rand = \frac{a+d}{a+b+c+d} = \frac{a+d}{\binom{n}{2}}
\end{equation}

Der Rand-Index teilt nun die Menge an Paaren, welche die gleiche Zuordnung erhalten haben ($a$ und $d$) durch die Anzahl aller möglichen Paarungen. Das Ergebnis ist ein Wert zwischen $0$ (keine Übereinstimmung) und $1$ (perfekte Übereinstimmung). [@rand1971]

Der Rand-Index weist eine Reihe von Problemen auf, welche teilweise von Rand selbst erkannt oder später ermittelt worden sind:

- Je höher die Anzahl an Clustern ist, desto höher (näher an der $1$) liegt der Rand-Index standardmäßig. Das kommt daher, dass bei einer hohen Anzahl an Clustern, die meisten Paare unterschiedlichen Clustern zu gewiesen sein müssen. Das treibt den Index künstlich in die Höhe. [@steinley2004; teilweise zitiert nach @rand1971]
- Zum Vergleich verschiedener Clustering-Verfahren werden häufig Monte-Carlo-Simulationen mit großen Mengen an zufällig generierten Datensätzen und Clusterings verwendet. Werden zwei Zufalls-Zuordnung miteinander verglichen, so gibt der Rand-Index keine Werte nahe der $0$, was aber wünschenswert wäre. Das liegt daran, dass die Anzahl an zufälligen Übereinstimmungen nicht adequat herausgerechnet wird. [@hubert1985; und @king2015, Kap. 8.4 Indices of Cluster Validity]

#### Adjusted Rand-Index

Aus den genannten Problemen haben eine Vielzahl von Autoren versucht, eine bessere Variante des Rand-Indexes zu finden. Vor allem das "Herausrechnen" von angeblichen hohen Übereinstimmungen bei zufälligen Zuteilungen (engl. correction for chance) ist eines der Hauptanliegen gewesen [@hubert1985]. Von allen vorgestellten Lösungen scheint die Variante von Hubert und Arabie [@hubert1985] diejenige mit den wünschenwertesten Eigenschaften zu sein. (siehe die Versuche z.B. von Steinley [@steinley2004])

\begin{equation}
  arand = \frac{rand - rand_{expected}}{rand_{max} - rand_{expected}}
\end{equation}

Im Allgemeinen geht es darum, den Rand-Index zu berechnen und anschließend den "erwarteten Rand-Index" für zufällige Zuordnungen davon abzuziehen. Verschiedene Autoren haben nun unterschiedliche Methoden hergeleitet, um diesen "erwarteten Rand-Index" zu berechnen. [@hubert1985]

\begin{equation}
  arand = \frac{\binom{n}{2}(a+d)-[(a+b)(a+c)+(c+d)(b+d)]}{\binom{n}{2}^2 - [(a+b)(a+c)+(c+d)(b+d)]}
\end{equation}

Hubert und Arabie berechnen den "erwarteten Rand-Index" aus der Menge aller möglichen Permutationen der Paarungen und ihrer Übereinstimmung $\frac{(a+b)(a+c)+(c+d)(b+d)}{\binom{n}{2}}$. Die gegebene Formell zeigt eine breits vereinfachte Umstellung von Steinley. [@hubert1985; und vereinfachte Formell aus @steinley2004]

Dieser "Adjusted Rand-Index" liefert Werte zwischen $-1$ und $1$. Negative Ergebnisse oder Werte um die $0$ zeigen, dass die Übereinstimmung der beiden Clusterings der zu erwartenden Übereinstimmung aufgrund von Zufall entspricht (oder sogar deutlich darunter liegt) und damit nicht signifikant ist. Höhere Zahlen nahe der $1$ stehen nachwievor für eine perfekte Übereinstimmung, welche zusätzlich statistische Signifikanz aufweist. Auch der Bias zu hohen Werten bei einer hohen Anzahl an Clustern wird daurch ausgeglichen. [@hubert1985; und @steinley2004]

### Internal Indices

In der Literatur werden eine Vielzahl von Indizes beschrieben, welche die Qualität der gefundenen Cluster messen können. Einen Überblick dazu geben Rendón et al. [@rendon2011]. An dieser Stellen sollen nur ein paar Vertreter vorgestellt werden, welche für diese Arbeit von besonderer Relevanz sind.

#### Silhouettenkoeffizient

Der Silhouettenkoeffizient wurde von Peter J. Rousseeuw entwickelt [@rousseeuw1987] und ist ein häufig verwendetes Maß für die Qualität von Clusterings.

\begin{align}
  s(x) &= \frac{b(x) - a(x)}{\max{a(x), b(x)}} \\
  a(x) &= d(x, C_x) \\
  b(x) &= \min_{C_x \neq C_i} d(x, C_i)
\end{align}

Für jeden Datenpunkt $x$ im Datenset wird die Silhouetten-Weite $s(x)$ berechnet. Diese ergibt sich aus der Differenz zwischen dem durchschnittlichen Abstand zu allen Datenpunkten im selben Cluster ($a(x)$) und dem durchschnittlichen Abstand zu allen Datenpunkten im direkt benachbarten Cluster ($b(x)$). Anschließend wird der Wert zwischen $-1$ und $1$ normiert. [@rousseeuw1987]

- Eine negative Silhouetten-Weite gibt an, dass der Datenpunkt näher am benachbarten als an seinem eigenen Cluster liegt und somit falsch zugeordnet worden ist.
- Werte um die $0$ zeigen, dass der Datenpunkt fast mittig zwischen beiden Clustern platziert ist.
- Befindet sich die Weite nahe der $1$, so liegt der Datenpunkt mittig in seinem eigenen Cluster und das benachbarte Cluster ist ordentlich weit entfernt.

\begin{equation}
  sil = \frac{1}{n}\sum_{i=1}^n s(x_i)
\end{equation}

Der Koeffizient ergibt sich schließlich aus dem Durchschnitt aller Silhouetten-Weiten aller Datenpunkte. Werte nahe der $1$ deuten auf kompakte und wohl-separierte Cluster hin. [@rousseeuw1987]

In den Versuchen von Rendón et al [@rendon2011] erwies sich dieser Index als einer der besten Indikatoren für ein gutes Clustering-Ergebnis. Er ist die direkte mathematische Definition für die Anforderung, dass Datenpunkte im gleichen Cluster möglichst ähnlich und zu den Punkten der andere Cluster möglichst unähnlich sein sollen. Ein Nachteil dieses Indizes ist die quadratische Laufzeit, da jeder Punkt mit jedem anderen verglichen werden muss.

#### Davies-Bouldin Index

Der Davies-Bouldin Index wurde von seinen Namesgebern David L. Davies und Donald W. Bouldin [@davies1979] entwickelt. Ziel war es, eine Metrik zu konstruieren, welche die durchschnittliche Ähnlichkeit zwischen benachbarten Clustern berechnet.

\begin{equation}
  dbi = \frac{1}{k} \sum_{i=1}^{k} \max_{i \neq j}{\frac{d(c_i, C_i) + d(c_j, C_j)}{d(c_i, c_j)}}
\end{equation}

Die Ähnlichkeit zwischen den Clustern $K$ ($K$ steht hier für die Menge an gefundenen Clustern $C_i$) berechnet sich aus dem durchschnittlichen Abstand der Punkte eines Clusters zu ihrem Cluster-Mittelpunkt ($d(c_i, C_i)$ und $d(c_j, C_j)$) geteilt durch den Abstand der beiden Cluster-Mittelpunkte zueinander ($d(c_i, c_j)$). [@davies1979]

Je kleiner der Wert des Indexes, desto enger liegen die Datenpunkte um ihren Cluster-Mittelpunkt im Verhältnis zum benachbarten Cluster. Möglichst niedrige Werte nahe der $0$ sind also als optimal anzusehen. [@davies1979]

Der große Vorteil von diesem Verfahren ist die geringere Laufzeit, da die Punkte der Cluster nur mit ihrem Mittelpunkt verrechnet werden. Nachteilig ist, dass die Be- und Verechnung der Mittelpunkte primär nur für numerische Vektoren definiert ist. In den Versuchen von Rendón et al. [@rendon2011] schnitt dieser Index genauso gut ab wie der Silhouettenkoeffizient.

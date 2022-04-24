# Implementierung

## Überblick

Nach der Konzeption folgte die Umsetzung und Implementierung des Praxisteils. Für eine bessere Übersicht ist in der folgenden Grafik die Architektur in detaillierterer Form inklusive implementierter Klassen und sonstiger Software-Komponenten dargestellt.

![Detaillierte Architektur der praktischen Umsetzung](img/architecture-detail.png)

adesso stellte für diesen Teil einen Server bereit, welcher für das Hosting von Akeneo-PIM genutzt wurde. Anschließend erfolgte die Installation von Akeneo-PIM Community Edition Version 5.0 auf diesem Server. Dazu wurde die offizielle Installationsanleitung von Akeneo unter Verwendung der Containerization-Lösung Docker (<https://www.docker.com/>) befolgt [@akeneo2022install]. Zusätzlich wurde das Akeneo-Plugin *Akeneo Icecat Connector* Version 2.0.0 [@akeneo2022icecat] in die Instanz integriert. Das kostenpflichtige Plugin wurde von adesso gesponsert.

Nun musste Akeneo-PIM mit Produktdaten gefüllt werden, welche aus dem Online-Katalog Icecat stammen. Eine genaue Übersicht zur Auswahl der Produkte sowie der weiteren Aufbereitung innerhalb von Akeneo siehe Abschnitt [Datenset](#datenset).

Anschließend erfolgte die Implementierung diverser Klassen und Packages, welche das hergeleitete Konzept umsetzen oder wichtige Hilfsfunktionalitäten für die spätere Evaluation liefern. Alle diese Komponenten sind in der Programmiersprache Python (<https://www.python.org/>) implementiert worden. Python ist sehr weit verbreitet für Aufgaben der Datenanalyse bzw. Data Science allgemein. Das liegt daran, dass es eine Vielzahl nützlicher Bibliotheken für die Analyse und Aufbereitung von Daten gibt. Ebenso sind Implementierungen vieler Algorithmen und Verfahren in Python verfügbar [@papp2019, Kap. 2.4.2 Programmierung]. Zu den meisten umgesetzten Elementen ist ebenfalls grundlegendes Unit-Testing durchgeführt worden, um die korrekte Funktionalität zu prüfen.

Das Package `akeneo` liefert zwei Hauptkomponenten. Der `AkeneoClient` kommuniziert mit der REST-API von Akeneo zum Abrufen der hinterlegten Daten. Ebenso konnten damit verschiedene Aufgaben, wie das Zuordnen der Produkte zu ihren passenden Kategorien, teilweise automatisiert werden. Der `AkeneoCache` nutzt den `AkeneoClient`, um alle Endpunkte abzufragen, welche Daten zurückgeben. Die JSON-Responses dieser Anfragen werden anschließend in JSON-Dateien gespeichert. Die REST-Anfragen dauern mitunter recht lange (mehrere Sekunden), allerdings änderte sich das Datenset nach der Erstellung nicht mehr. Durch diese Zwischenspeicherung wurde die Evaluation erheblich beschleunigt, da die Daten direkt aus den Dateien gelesen werden konnten. Der `AkeneoCache` ist ebenso für das Laden der Daten zuständig. Dazu werden die JSON-Objekte in Python-Datenstrukturen überführt, wofür die Bibliothek `dacite` (<https://github.com/konradhalas/dacite>) zum Einsatz kam.

Zunächst wurde überprüft, ob externe Clustering-Bibliotheken in der Lage sind, das erarbeitete Konzept umzusetzen. Da keine Bibliothek den Anforderungen genügte, wurde im Package `clustering` eine generische Version des `KMeans` und `BisectingKMeans` implementiert. Sie nutzen ein allgemeines Interface `Centroid`, welches für eine konkrete Clustering-Anwendung vorher implementiert werden muss. Genauere Details dazu in Abschnitt [Clustering](#clustering).

Das Package `akeneo_clustering` bringt nun die beiden anderen Packages zusammen. Die Funktion `parse_products()` liest die Daten aus dem Cache aus und bereitet die Produkte für das Clustering auf. Dabei werden zum Beispiel die beschriebenen Vorverarbeitungen für numerische und String-Attribute durchgeführt. Die `Centroid`-Klasse implementiert das Interface für das `clustering`-Package. Hier ist die erarbeitete Distanzfunktion hinterlegt, ebenso der genaue Prozess, wie Mittelpunkte zu den jeweiligen Clustern berechnet werden. Weitere Details im Abschnitt [Clustering](#clustering)

Abschließend fand die Evaluation mithilfe von Jupyter Notebooks statt. Das sind Source-Code-Dateien, die in einzelne Code-Zellen unterteilt sind. Mithilfe eines Webfrontends, welches Jupyter mitliefert, können die Notebooks interaktiv verändert und beliebig einzelne oder mehrere Code-Zellen ausgeführt werden. Die Ausgaben der Zellen erscheinen direkt darunter. Dadurch eignet sich Jupyter für Analysen, in denen wiederholt Versuche und leichte Abwandlungen dieser durchgeführt werden. Die direkte Visualisierung beschleunigt den Evaluationsprozess [@papp2019, Kap. 2.4.2 Programmierung]. Um die Berechnung der Metriken möglichst fehlerfrei durchführen zu können, ist auf die umfangreiche Sammlung implementierter Metriken von `scikit-learn` zurückgegriffen worden. Näheres im Abschnitt [Evaluation](#evaluation).

## Datenset

### Attribute

Wie bereits beschrieben, müssen die Attribute in Akeneo zuerst existieren, bevor ein Produkt einen Wert darin aufweisen kann. Icecat definiert ebenfalls eine sehr umfangreiche Liste an Icecat-Attributen. Diese können über den Icecat-Importer ausgewählt und in Akeneo importiert werden. Dabei werden die Icecat-Typen entsprechend auf äquivalente Akeneo-Attributtypen abgebildet. Dieser Prozess läuft grundsätzlich automatisch über den Importer. Allerdings müssen dazu vorher per Hand in der Weboberfläche des Importers alle Attribute ausgewählt werden, welche es zu importieren gilt.

Icecat stellt für jede Produktkategorie eine eigene Taxonomie zur Verfügung, welche beschreibt, was für Attribute in den Produkten der jeweiligen Kategorie vorkommen können und ob sie erforderlich oder optional sind. Entsprechend sind die Taxonomien für "mobile_phone_cases" und "smartphones" heruntergeladen worden. Die Excel-Dateien finden sich im angehängt Git-Repository im Ordner `cluster-analysis > data > icecat-taxonomy`. Mittels dieser Dateien sind per Hand im Importer alle benötigten Attribute ausgewählt und importiert worden.

Anschließend sind nach dem Vorbild der Icecat-Taxonomien in Akeneo zwei "Families" (eine für die Hüllen und eine für die Smartphones) angelegt worden. Über die "Family" kann in Akeneo festgelegt werden, welche Attribute bei Produkten dieser Art vorkommen können sowie, ob sie erforderlich oder optional sind. Dieser Prozess ließ sich weitestgehend per Skript lösen. Im Repository im Ordner `cluster-analysis > reports > dataset` sind die ausgeführten Schritte samt Code hinterlegt.

Es folgten ein paare kleinere weitere Schritte, wie die Strukturierung der Attribute in Gruppen zur besseren Übersicht. Diese sind aber nicht weiter von Belang.

### Produkte

Als nächstes sind Produkte für den Import ausgewählt worden. In der kostenlosen Version von Icecat stehen nur Produkte von einigen wenigen Herstellern (sog. Sponsoren) zur Verfügung. Zu diesen Sponsoren zählen auch Samsung und einige Hersteller von Smartphone-Hüllen für Samsung-Smartphones. Über die Suchfunktion von Icecat sind nun Samsung-Smartphones der S-Reihe aus den Generationen S20, S21 und S22 gesucht und ausgewählt worden – ebenso zu den Modellen passende Hüllen. Im angehängten Git-Repository gibt es den Ordner `cluster-analysis > data > dataset`. Dieser enthält mehrere CSV-Dateien, welche verschiedene Daten enthalten, die später in Akeneo importiert wurden. Die Datei `products.csv` enthält alle ausgewählten Produkte mit ihrem jeweiligen Link zu Icecat. Die Produktfamilie (Hülle oder Smartphone) ist in der "Family" hinterlegt. Über die "Categories" wird das Smartphone-Modell des jeweiligen Produktes festgehalten. Ebenso ist mit entsprechenden Categories vermerkt, ob zwei Produkte Duplikate voneinander sind. Die folgende Tabelle gibt eine Übersicht über die 122 ausgewählten Produkte:

| Modell | Hüllen | Smartphones | davon Duplikate [^dups] |
|-|-:|-:|-:|
| S20       | 18 |  5 |  2 |
| S20+      | 14 |  5 |  0 |
| S20 Ultra | 11 |  4 |  2 |
| S20 FE    |  2 |  3 |  0 |
| S21       | 11 |  7 |  4 |
| S21+      | 10 |  4 |  2 |
| S21 Ultra |  5 |  6 |  2 |
| S21 FE    |  5 |  4 |  0 |
| S22       |  2 |  2 |  0 |
| S22+      |  1 |  1 |  0 |
| S22 Ultra |  1 |  1 |  0 |
| *gesamt:* |*80*|*42*|*12*|
: Importierte Produkte nach Smartphone-Modell

[^dups]: Es kommen nur Duplikate von Smartphones vor.

Schließlich ist aus der Icecat-URL die SKU und EAN der Produkte ausgelesen und per Skript in Akeneo jeweils als neues Produkt eingefügt worden. Danach wurde im Icecat-Importer der `EnrichProducts`-Job ausgeführt, welcher die restlichen noch leeren Attribute der Produkte mit den Daten aus Icecat füllt.

### Korrekturen

Nach dem Import der Attribute und Produkte wurden die Daten analysiert und auf Fehler geprüft. Dabei traten eine ganze Reihe von Problemen zutage:

- Alle 31 Attribute, welche in Icecat als Multi-Select definiert sind, wurden in Akeneo als Single-Select importiert. Unter den Labels des Attributs "Material" finden sich z.B. die Werte "Silicone, Thermoplastic polyurethane (TPU)" sowie "Thermoplastic polyurethane (TPU), Silicone". Also die gleiche Information als zwei verschiedene Labels.
- 22 numerische Attribute warfen beim Import Fehler, weshalb diese schließlich als Textzeilen importiert werden mussten.
- 10 Single-Selects sind automatisch als Textzeilen importiert worden.

Diese Fehler wurden anschließend per Skript gefixt. Dazu wurde jedes fehlerhafte Attribut ein zweites Mal in korrigierter Version in Akeneo angelegt. Anschließend wurde jedes Produkt durchgegangen und die Werte aus den fehlerhaften Attributen korrigiert und in den neuen Attributen gespeichert. Die Werte der Multi-Selects enthielten die verschiedenen Optionen als Komma-getrennte Liste, welche entsprechend aufgeteilt worden ist. Die fehlerhaften numerischen Attribute und Single-Selects konnten ohne Probleme direkt auf den richtigen Typ übertragen werden.

Zum Schluss sind alle fehlerhaften Attribute in eine Attributgruppe names "Faulty" sortiert worden. Dadurch können sie in der Evaluation direkt herausgefiltert werden, sodass nur die korrekten Attribute bei der Verarbeitung übrig bleiben.

Etwas später wurde noch offenkundig, dass alle numerischen Attribute mit einer "MeasurementUnit" ebenfalls fehlerhaft sind. Die Einheit ist falsch importiert worden, sodass bspw. die Smartphones zwischen 5 und 6 Kilogramm wiegen. Da dieser Fehler aber bei allen Attributen "konsistent" aufgetreten ist und die numerischen Attribute im Zuge der Vorverarbeitung sowieso normalisiert werden, kann dieser Fehler ignoriert werden.

| Attributklasse | Hüllen |  | Smartphones | | davon in beiden |
|--|-:|-:|-:|-:|-:|
| | *erforderlich* | *optional* | *erforderlich* | *optional* | |
| numerisch         | 1 | 22 | 10 | 106 | 10 |
| kategorisch       | 3 | 16 | 19 | 157 |  2 |
| multi-kategorisch | 1 |  4 |  3 |  26 |  3 |
| strings           | 5 |  5 |  6 |  27 |  9 |
| andere            | 5 |  0 |  4 |   2 |  4 |
: Anzahl an Attributen je Attributklasse und Produktfamilie

Die Tabelle zeigt die jeweilige Menge an Attributen für die Hüllen und die Smartphones nach der Durchführung der Korrekturen.

## Clustering

### Überblick zu externen Libraries

Für Python existieren eine ganze Reihe an Bibliotheken für das maschinelle Lernen. Diverse Verfahren, welche in der Literatur beschrieben wurden, sind darin praktisch implementiert. Daher ist zuerst geprüft worden, ob eine der existierenden Lösungen bereits für die Clustering-Aufgabe verwendet werden kann.

Die Bibliothek `PySpark` von Apache [@apache2022bikmeans] ist eine der wenigen, die eine Implementierung für den Bisecting K-Means-Algorithmus zur Verfügung stellt. Das originale Verfahren von Steinbach et al. [@steinbach2000] ist nur für numerische Attribute ausgelegt gewesen. Die Implementierung von Apache ist es ebenfalls. Auch die Verwendung von `null`-Values im Datenset funktioniert mit dieser Bibliothek nicht, sodass künstliche Werte eingefügt werden müssten, welche vor allem die Berechnung des Durchschnitts für den Centroid verzerren.

Für den K-Means und den K-Prototypes existieren ebenfalls Implementierungen, welche vielleicht als Grundlage für eine eigene Umsetzung in der "Bisecting-Variante" hätten dienen können.

Eine der größten Bibliotheken für das Machine Learning – `scikit-learn` – bietet nur den klassischen K-Means an und ist ebenfalls nicht in der Lage `null`-Values zu verarbeiten [@sklearn2022]. Für das Clustering der Produktdaten ist diese Bibliothek also ebenfalls ungeeignet. Allerdings ermöglicht sie zusätzlich die Berechnung diverser Metriken wie den Adjusted-Rand-Index oder den Silhouettenkoeffizienten. Diese sind für die Evaluation verwendet worden.

Die einzige gepflegte Implementierung des K-Prototypes stammt von Nico de Vos [@nicodv2022]. Wie alle Verfahren, kann auch diese Variante nicht mit `null`-Values umgehen. Da die Distanzfunktionen per Parameter übergeben werden, hätte die erarbeitete Berechnung der multi-kategorischen Attribute mit dieser Bibliothek wahrscheinlich umgesetzt werden können. Auf die Ermittlung des Mittelpunktes kann aber im Gegensatz dazu kein Einfluss genommen werden. Schlussendlich wurde auch diese Lösung verworfen.

Das Clustering wurde daraufhin selbst auf eine möglichst generische Art und Weise implementiert. Dabei dienten vor allem `scikit-learn` und die Implementierung von Nico de Vos als Vorbild.

### Clustering-Library

#### `Centroid`-Interface

Das Ziel bei der Implementierung war es, eine möglichst flexible Lösung zu bauen, sodass in der Auswertung beliebige Varianten des Clusterings ausprobiert werden können. Der grundlegende Ablauf des K-Means ändert sich eigentlich nicht. Unterschiede treten vor allem in der Distanzfunktion auf und wie aus den Datenpunkten ein Mittelpunkt errechnet wird. Dadurch entstand die Idee, das Verfahren so umzusetzen, dass diese Aspekte beliebig ausgetauscht werden können. Der Rahmenablauf bleibt bestehen.

Es entstand das `Centroid`-Interface, was eine komplett abstrakte Definition eines einzelnen Centroids darstellt. Das Interface verlangt die Implementierung von zwei Methoden:

- `calc_distance(dp: Datapoint) -> float` berechnet den Abstand zwischen dem Centroid und einem Datenpunkt. Auch dieser Datenpunkt ist lediglich als "TypeVariable" definiert. Es obliegt also der Centroid-Implementierung, welches Format die Datenpunkte haben müssen.
- `on_add_point(dp: Datapoint)` wird aufgerufen, wenn ein neuer Datenpunkt zum Cluster dieses Centroid hinzugefügt wird. Die Methode sollte den internen State des Centroid aktualisieren, sodass die `calc_distance`-Methode nach dem Hinzufügen eines Datenpunktes andere Ergebnisse liefert, da sich der Centroid verschoben hat.

Die tatsächliche Implementierung dieses Interfaces liegt auf der Seite des Anwenders. So könnte eine Variante für ausschließlich numerische Attribute implementiert werden, welche den euklidischen Abstand für die Distanzberechnung benutzt. Eine andere Implementierung könnte sowohl numerische als auch kategorische Attribute verarbeiten, unterstützt aber keine `null`-Values usw.

#### Generisches K-Means

Die umgesetzte Version des K-Means nutzt also das `Centroid`-Interface für das Clustering. Dadurch ist es streng genommen kein reiner K-Means mehr, sondern abhängig von der `Centroid`-Klasse eventuell ein K-Modes, ein K-Prototypes oder etwas komplett anderes. Aus Gründen der Einfachheit wird stets vom (generischen) K-Means die Rede sein.

Die Umsetzung ähnelt der Version von `scikit-learn`. `KMeans` ist eine Klasse, welche direkt bei der Instanziierung das Datenset, die implementierte `Centroid`-Klasse und eventuelle weitere Parameter übergeben bekommt. Mit der Instanziierung wird sofort das Clustering ausgeführt. Die Ergebnisse können anschließend über die Attribute der Instanz abgerufen werden.

Es können sehr ähnliche Parameter wie in der `scikit-learn`-Implementierung für das Clustering gesetzt werden. So kann mit dem Parameter `n_init` festgelegt werden, wie häufig sich der K-Means selbst initialisiert, um anschließend den besten Durchlauf auszuwählen. Über `random_state` lässt sich ein Seed für die zufällige Wahl der initialen Startpunkte festlegen usw. [@sklearn2022]

Im angehängten Git-Repository liegt im Ordner `cluster-analysis > reports > clustering` eine Datei namens `0-algorithm-check.html`. Sie enthält den Export eines Jupyter Notebooks, in welchem die Implementierung von `scikit-learn`, Nico de Vos und des Autors dieser Arbeit miteinander verglichen werden. Die Verfahren werden mit ähnlichen Parametern aufgerufen und liefern sehr ähnliche Ergebnisse über das gleiche Datenset.

#### Generisches Bisecting K-Means

Mithilfe des generischen K-Means wurde schließlich die generische Bisecting K-Means-Version implementiert. Auch `BisectingKMeans` ist eine Klasse, welche direkt mit der Initialisierung das hierarchische Clustering mithilfe des generischen K-Means ausführt. Der Abruf der Ergebnisse erfolgt ebenfalls über Attribute der Klasse. Das folgende Listing zeigt eine mögliche Darstellungsform des Clustering-Ergebnisses:

```python
# ...
BisectingKMeans(dataset, Centroid).labels
# Ausgabe:
[
    {0, 1, 2},  # Datenpunkt 1
    {0, 1},     # Datenpunkt 2
    {0},        # Datenpunkt 3
    {0, 3, 4},  # Datenpunkt 4
    {0, 3},     # Datenpunkt 5
]
```

In dem Beispiel wurde ein Clustering über ein Datenset mit fünf Punkten durchgeführt. Jede Zeile listet die Cluster-Zuordnungen für jeweils einen Datenpunkt. Datenpunkt 1 gehört bspw. den Clustern 0, 1 und 2 an. Da es sich um ein Top-down-Clustering handelt, starten alle Datenpunkte entsprechend initial im Cluster $0$. Der erste Split trennte die ersten beiden Punkte vom Rest. Als nächstes wurden Punkt 1 und 2 ebenfalls voneinander getrennt usw.

Es gibt in der Klasse auch eine Methode names `labels_flat(k: int)`. Hiermit können die Cluster-Zuordnungen für ein spezifisches $k$ abgerufen werden.

```python
# ...
BisectingKMeans(dataset, Centroid).labels_flat(2)
# Ausgabe:
[ 1, 1, 0, 0, 0 ]
# ...
BisectingKMeans(dataset, Centroid).labels_flat(4)
# Ausgabe:
[ 2, 1, 0, 3, 3 ]
```

Aus einer `BisectingKMeans`-Instanz kann also die Cluster-Zuordnung für jede beliebige Hierarchieebene abgerufen werden.

### Weitere Implementierungen

#### `Centroid`-Klasse

Mit der Implementierung des `Centroid`-Interfaces konnte nun das hergeleitete Konzept aus Kapitel 3 umgesetzt werden. Die Klasse verarbeitet Datenpunkte in Form einer Hash-Map, welche die "codes" der Attribute aus Akeneo einem numerischen, kategorischen oder multi-kategorischen Wert zuordnet. Das folgende Listing zeigt die Typdefinition eines solchen Datenpunktes in Python.

```python
Datapoint = dict[str, float|str|set[str]]
```

Damit weisen die Datenpunkte eine sehr ähnliche Struktur zu den "ProductValues" in Akeneo auf und bedürfen nur noch geringfügiger Vorverarbeitung.

Die `calc_distance`-Funktion konnte fast eins-zu-eins zu der serialisierten Formel in Kapitel 3 implementiert werden. `on_add_point` aktualisiert den Centroid in den numerischen Werten über den Durchschnitt und in den kategorischen und multi-kategorischen Werten über den Modus. `null`-Values (welche dadurch zustande kommen, dass ein Produkt einige Attribute nicht in seiner Hash-Map aufweist) werden, wie beschrieben, behandelt.

#### Datenvorverarbeitung

Im Rahmen der Vorverarbeitung müssen die "Products" aus Akeneo-PIM in die Form des definierten `Datapoint` gebracht werden. Dies geschieht mit Hilfe der `parse_products()`-Funktion. Sie extrahiert die "ProductValues" und bereitet sie entsprechend auf. Je nach Attributtyp werden hier verschiedene Schritte durchgeführt:

- Numerische Attribute werden entsprechend der Tabelle in Kapitel 3.3.2 verarbeitet und normalisiert.
- Kategorische Attribute bleiben wie sie sind, denn die serialisierte Version der Distanzfunktion bedarf keiner vorherigen Umwandlung in binäre Attribute.
- Multi-kategorische Attribute sind ebenfalls bereits in der richtigen Form
- Textzeilen werden entsprechend mithilfe der Python-Bibliothek `nltk` (<https://www.nltk.org/>), welche auf das Natural Language Processing spezialisiert ist, tokenisiert.
- Alle anderen Arten von Attributen werden entfernt.

In dem `akeneo_clustering`-Package existieren noch weitere Hilfsfunktionen, welche hier aber nicht weiter von Belang sind.

Damit sind alle Vorbereitungen für die Evaluation getroffen.

## Evaluation

Die Evaluation erfolgt, wie in der Konzeption festgelegt, zuerst nur mit den Hüllen, danach nur mit den Smartphones und schließlich mit allen Produkten zusammen. Die Jupyter Notebooks, welche die Versuche enthalten, sind im angehängten Git-Repository unter `cluster-analysis > notebooks > clustering` zu finden. Zusätzlich wurden die Notebooks auch nochmal als HTML-Dateien exportiert. Diese befinden sich in Repository unter `cluster-analysis > reports > clustering`.

Die Versuche laufen stets nach einem ähnlichen Muster ab: Zuerst werden die jeweiligen Produkte aus Akeneo geladen und vorverarbeitet (wie beschrieben mittels der `parse_products()`-Funktion und weiteren). Dann findet eine kurze Analyse der tatsächlich vorkommenden Attribute statt. Anschließend werden immer verschiedene Kombinationen an Attributen ausgewählt und das Clustering wird mit dieser Auswahl durchgeführt. Zu den Clustering-Ergebnissen werden die Metriken für die Stabilität, Qualität und Erkennungsfähigkeit berechnet und ausgegeben. Daran können sich entsprechend weiterführende Analysen anschließen.

Die genaue Berechnung der Metriken funktioniert dabei wie folgt:

- Die *Stabilität* wird berechnet, indem das Clustering mit den gewählten Attributen zehn Mal durchgeführt wird, jedes mal mit einem anderen Seed für die Zufallsinitialisierung. Dann werden die Cluster-Zuordnungen des ersten Durchlaufes nacheinander mit den neun folgenden Durchläufen verglichen. Der Vergleich erfolgt so, dass mittels der `labels_flat`-Methode des `BisectingKMeans` nacheinander alle Hierarchieebenen von $2$ bis $n-1$ abgerufen werden. Für die Cluster-Zuordnung von zwei verschiedenen Initialisierungen wird nun der Adjusted-Rand-Index (Implementierung aus `scikit-learn`) berechnet, welche die Übereinstimmung beider Clustering-Ergebnisse misst. Man erhält also $9 \cdot (n-2)$ verschiedene Ergebnisse. Aus all diesen Werten wird der Durchschnitt berechnet. Die Stabilität ist also der durchschnittliche Adjusted-Rand-Index (Ähnlichkeit) über alle sinnvollen Hierarchieebenen von einem Clustering zu neun weiteren Durchläufen mit exakt den gleichen Parametern.
- Die *Qualität* wird über den Silhouettenkoeffizienten ermittelt. Die Implementierung in `scikit-learn` erlaubt die Verwendung dieses Koeffizienten mit eigenen Distanzfunktionen, weswegen diese Metrik dem Davies-Bouldin-Index vorgezogen worden ist. Ähnlich wie bei der Stabilität wird ebenfalls die `labels_flat`-Methode benutzt, um alle Cluster-Zuordnungen über die verschiedenen sinnvollen Hierarchiestufen ($2 \leq k \leq n-1$) zu erhalten. Für jede Stufe wird nun der Silhouettenkoeffizient berechnet. Anschließend wird der Durchschnitt aller Koeffizienten über alle Ebenen gebildet. D.h. die Qualität ist der durchschnittliche Silhouettenkoeffizient eines Clustering-Durchlaufes über alle sinnvollen Hierarchieebenen.
- Die *Erkennungsfähigkeit* wird über den Vergleich der Ähnlichkeit mit den "Akeneo-Categories" durchgeführt, in denen die Smartphone-Generationen und Modelle hinterlegt sind. Über die `labels_flat`-Methode wird die Zuordnung für die jeweilige Stufe abgefragt (i.d.R. Generationen: $k=3$, Modelle: $k=11$). Anschließend wird der Adjusted-Rand-Index zwischen den berechneten und den erwarteten Zuteilungen ermittelt. Hier werden für jeden Versuch also in der Regel zwei Werte für die jeweiligen $k$s gegeben sein.
- Speziell in den Smartphones kommen zusätzlich noch die Duplikate vor, welche eine Sonderform für die Erkennungsfähigkeit darstellen. Hier ist die Erwartung, dass die Produkte, welche Duplikate von einander sind, über alle Hierarchieebenen (minus der letzten) stets in die gleichen Cluster zugeteilt sein müssten. Wie bereits erklärt, kann aus der `BisectingKMeans`-Klasse zu jedem Datenpunkt die Zugehörigkeit zu allen Clustern im Verlaufe des Prozesses abgerufen werden. Die Menge $y_1$ sind also alle Cluster, denen der Punkt $x_1$ angehört und $y_2$ entsprechend alle Cluster, denen $x_2$ angehört. Mit Hilfe eines abgewandelten Jaccard-Koeffizienten kann nun berechnet werden, ob beide Punkte häufig denselben Clustern zugeordnet worden sind:

\begin{equation}
    \frac{|y_1 \cap y_2| - 1}{|y_1 \cup y_2| - 1}
\end{equation}

Da die Duplikate im letzten Split ebenfalls in verschiedenen Clustern landen, wird im Zähler und im Nenner entsprechend die $1$ für diesen finalen Split abgezogen. Sind beide Datenpunkte, wie erwartet, stets in den gleichen Clustern gewesen, so liegt der Wert des Koeffizienten bei $1$. Wurden sie früher getrennt (also andere Produkte wurden als ähnlicher klassifiziert als die Duplikate), liegt der Wert entsprechend niedriger.

Für alle vorkommenden Duplikate wird dieser modifizierte Jaccard-Koeffizient berechnet und anschließend der Durchschnitt aus diesen Koeffizienten gebildet. Der Spezialwert *Duplikate* in der Erkennungsfähigkeit ist also die durchschnittliche Übereinstimmung der Cluster-Zuteilung aller Duplikate.

Alle Metriken liegen damit im Bereich $[-1;1]$ (außer die Duplikaterkennung: $[0;1]$) und Werte nahe der $1$ stellen das beste Ergebnis dar. Werte um die $0$ oder sogar tiefer sind entsprechend negativ für den jeweiligen Versuch zu werten.

Außerdem ist wichtig zu erwähnen, dass die Werte der Stabilität nahe der $1$ liegen sollten. Andernfalls ist das Clustering nicht deterministisch und die Distanzfunktion trennt die Produkte nicht ausreichend voneinander. Die Qualität sollte auf jeden Fall positiv sein, allerdings ist es ganz normal, dass die Qualität auf bestimmten Hierarchieebenen höher ist und auf anderen niedriger, wodurch im Durchschnitt eher mittelmäßige Werte in dieser Metrik entstehen. Die Erkennungsfähigkeit sollte so hoch wie möglich liegen, da dies ja der intuitiven Einteilung der Produkte durch Menschen entspricht. Liegen die Werte hier unter $0.5$, ist die Verwendung in der Praxis wohl eher ausgeschlossen.

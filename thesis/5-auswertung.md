# Auswertung

## Datenset "Smartphone-Hüllen"

### Überblick

Das hergeleitete Clustering-Verfahren wurde zuerst auf die Smartphone-Hüllen des Datensets angewendet. Es enthält 80 verschiedene Produkte von 4 verschiedenen Herstellern. Die nachfolgende Tabelle zeigte einige Informationen zu den Attributen dieser Produktkategorie.

| Typ | erforderlich | Anzahl | Ø non-`null` | Ø unique |
|-|-|-:|-:|-:|
| numerisch   | ja   | $1$ | $76.0$ |  $7.0$ |
| numerisch   | nein | $5$ | $19.4$ |  $9.2$ |
| kategorisch | ja   | $3$ | $78.3$ |  $2.7$ |
| kategorisch | nein | $8$ | $28.5$ |  $1.4$ |
| multi-kat.  | ja   | $1$ | $57.0$ | $10.0$ |
| string      | ja   | $4$ | $79.2$ | $69.2$ |
: Übersicht zu den Attributen der Smartphone-Hüllen

Die Smartphone-Hüllen zeichnen sich vor allem durch eine überschaubare Anzahl an Attributen aus. Die Tabelle zeigt, wie viele Attribute je Typ und Erforderlichkeit im Datenset vorkommen. Attribute, in denen keine einzige Wertausprägung vorkommen, sind hier bereits entfernt, ebenso alle Attribute, die nicht mir den hergeleiteten Verfahren verarbeitet werden können.

Für die multi-kategorischen und String-Attribute kommen ausschließlich erforderlich Attribute in diesen Produkten vor. Nur für die numerischen und kategorischen Werte existieren auch optionale Attribute.

Die Spalte "Ø non-`null`" gibt an, wie viele der $80$ Produkte im Schnitt in dieser Attribut-Art einen Wert ausweisen (also nicht `null` sind). Erforderliche Attribute liegen hier stets bei etwas unter $80$ mit Ausnahme des einen multi-kategorischen Attributs. Das heißt, dass die erforderlichen Attribute tatsächlich meistens mit Werten gefüllt sind – wenn auch nicht immer.

Die Spalte "Ø unique" gibt an, wie viele unterschiedliche Wertausprägungen im Schnitt in der jeweiligen Attribut-Art vorkommen. Besonders die String-Attribute weisen in praktisch jedem Produkt einen anderen Wert auf, was aber auch in der Natur dieser Attribut-Art liegt.

### Verarbeitung multi-kategorischer Attribute

Da in der klassischen Clusteranalyse keine multi-kategorischen Attribute beschrieben sind, ist ein spezielles Verfahren zur Verarbeitung dieser Attribute erarbeitet worden. Diese Verarbeitung wird nun mit einem alternativen Ansatz verglichen. Dazu ist das Clustering mit dem einen multi-kategorischen Attribut (Material) im Datenset durchgeführt worden. Das erste Mal wurde die hergeleitete Verarbeitung verwendet. Beim zweiten Durchlauf sind alle multi-kategorischen Werte in kategorische umgewandelt worden (durch einfache Komma-separierte Verkettung). Die folgende Tabelle zeigt die berechneten Metriken zu beiden Clusterings:

| Verarbeitung | Stabilität | Qualität | Erkennung | |
|-|-:|-:|-:|-:|-:|
| | | | *Generation* | *Modell* |
| multi-kategorisch    | $0.71$ | $0.44$ | $0.02$ | $0.04$ |
| (single) kategorisch | $0.61$ | $0.44$ | $0.00$ | $0.04$ |
: Clustering der Hüllen mit multi-kategorischem Attribut

Die Ergebnisse beider Clusterings unterscheiden sich kaum voneinander. Lediglich die Stabilität ist mit der hergeleiteten Verarbeitungsart etwas höher. Insgesamt liegt die Stabilität aber recht niedrig, was daran liegen könnte, dass nur ein einziges Attribut für das Clustering verwendet worden ist mit ungefähr $10$ verschiedenen Wertausprägungen. Entsprechend sind viele Produkte komplett identisch zueinander, was zu einer schlechteren Stabilität führt. Die Qualität liegt auf einem mittleren Niveau und ist in beiden Versuchen identisch gewesen. Die Erkennung der Smartphone-Generation ($k=3$) und des -Modells ($k=11$) liegt faktisch bei $0$. Bei dem einen multi-kategorischen Attribut, welches hier verwendet wurde, handelt es sich um das Material. Das ist augenscheinlich kein gutes Attribut, um festzustellen, zu welchem Smartphone die entsprechende Hülle passt.

Als nächstes ist der gleiche Versuch mit den String-Attributen durchgeführt worden. Die nächste Tabelle zeigt die Metriken zu den Ergebnissen:

| Name | Stabilität | Qualität | Erkennung | |
|-|-:|-:|-:|-:|-:|
| | | | *Generation* | *Modell* |
| Strings als multi-kat.  | $0.87$ | $0.20$ | $0.54$ | $0.16$ |
| Strings als single-kat. | $0.64$ | $0.15$ | $0.03$ |$-0.01$ |
: Clustering der Hüllen mit String-Attributen

Für die Strings macht die Verarbeitung als "multi-kategorische" Attribute einen enormen Unterschied. Alle Metriken verbessern sich drastisch durch die hergeleitete Art der Verarbeitung. Das Aufteilen der Strings in Tokens und der anschließende Vergleich der Ähnlichkeit der auftretenden Tokens steigert vor allem die Erkennung der Smartphone-Generation. Bei den vier Attributen handelt sich um "Name", "Titel", "Short Description", "Short Summary". "Name" enthält eher willkürlich vergebene Zahlen- und Buchstabenkombinationen, die keinem erkennbaren Muster folgen. In den drei anderen Attributen steckt aber stets die jeweilige Smartphone-Generation, für die die Hülle ausgelegt ist (also die Token "s20", "s21" und "s22"), was die hohe Erkennung erklärt.

Vor allem der zweite Versuch mit den String-Attributen legt nahe, dass das hergeleitete Verfahren für die Verarbeitung multi-kategorischer Attribute, sinnvolle Ergebnisse für die Clusteranalyse bringen und einen alternativen Ansatz für die Verarbeitung von String-Werten darstellen kann.

### Attribut-Auswahl

Als nächstes geht es darum, dass hergeleitete Clustering-Verfahren als ganzes zu bewerten. Dabei geht es auch darum, herauszufinden, ob das Verfahren besser arbeitet, wenn nur bestimmte Attribute verwendet werden anstatt allen, die verarbeitet werden können etc.

#### Vergleich nach Datentypen

Zuerst ist geprüft worden, ob bestimmte Typen von Attributen und Typen-Kombinationen besser für das Clustern des Datensets geeignet sind als andere. Insgesamt gibt es ja vier verschiedene Typen (numerisch, kategorisch, multi-kategorisch und Strings, welche ja ebenfalls multi-kategorisch verarbeitet werden). Das Clustering wurde nun in allen möglichen Kombinationen an Attribut-Typen durchgeführt. Also zuerst wurden nur die numerischen Attribute geclustert, dann die kategorischen usw. Im letzten Durchlauf wurden schließlich alle möglichen Attribute verwendet. Die folgende Tabelle zeigt eine Auswahl dieser Versuche (i.d.R. diejenigen, welche den besten Wert in einer der Metriken errungen haben):

| Typen | Stabilität | Qualität | Erkennung | |
|-|-:|-:|-:|-:|-:|
| | | | *Generation* | *Modell* |
| numerisch   | 0.85 | 0.43 | 0.15 | 0.45 |
| string      | 0.87 | 0.20 | **0.54** | 0.16 |
| num+kat     | 0.88 | **0.52** | 0.09 | 0.26 |
| num+str     | 0.86 | 0.20 | 0.14 | **0.46** |
| kat+str     | **0.94** | 0.27 | 0.10 | 0.14 |
| kat+mul+str | **0.94** | 0.29 | 0.09 | 0.10 |
| alle        | 0.92 | 0.29 | 0.12 | 0.25 |
: Clustering der Hüllen mit verschiedenen Kombinationen an Attribut-Typen

Interessant ist, dass es keine "überlegene Auswahl" an Attributen gibt, sondern je nach Metrik eine andere Kombination am besten abschneidet. So führt das Weglassen der numerischen Attribute zu den beiden stabilsten Clusterings. Die Kombination numerisch und kategorisch erreicht die höchste Qualität. Wie vorher beschrieben, werden mit den String-Attributen die zu den Hüllen gehörende Smartphone-Generationen am besten erkannt. Nutzt man Strings und numerische Werte zusammen, können die Modelle recht gut zugeordnet werden, aber die Erkennung der Generationen sinkt wieder deutlich ab.

Insgesamt sind die Werte für die Erkennung sehr schlecht. Das kann daran liegen, dass viele Attribute keine Informationen enthalten, welche die zu den Hüllen passenden Smartphones beschreiben. Unter den Attributen gibt es lediglich "Brand compatibility" (wobei hier nur "Samsung" als einziger Wert auftritt), "Maximum Screen Size" und eventuell "Height", "Width", "Depth", welche Rückschlüsse zu den passenden Smartphones bieten. Andere Attribute wie das beschriebene "Material" oder "Number of Card Pockets" bilden hingegen ganz andere Eigenschaften ab. Die erwartet Clusterzuteilung nach Smartphone-Generation bzw. -Modell ist u.U. keine sinnvolle Einteilung für die Smartphone-Hüllen. Daher wird dieser Metrik im Folgenden keine Bedeutung mehr beigemessen.

Damit bleiben noch die Stabilität und die Qualität in Form des Silhouetten-Koeffizienten zur Bewertung der Clusterings. Dazu werden diese Metriken jetzt für die gegebenen Typ-Kombinationen über die verschiedenen Hierarchie-Ebenen miteinander verglichen.

![Stabilität der Clusterings nach Typen über alle $k$s \label{fig:casesstab}](img/cases-types-stability.png)

Grafik \ref{fig:casesstab} zeigt die Stabilität der verschiedenen Typ-Kombinationen über die verschiedenen Hierarchie-Ebenen ($k$s) des Clusterings.

Es ist zu erkennen, dass die numerischen und kategorischen Attribut-Kombinationen bei geringeren Werten für $k$ tendenziell stabiler sind und gegen Ende der Hierarchie stärker schwanken. Das ist dadurch zu erklären, dass es in diesen Attributen viel weniger verschiedene Wertausprägungen gibt. Dadurch ist die Teilung in Cluster am Anfang, wenn die Cluster noch recht groß sind, eindeutiger als gegen Ende.

Kombinationen, welche auch String-Attribute verwenden, verhalten sich gegenteilig. Gerade bei geringen $k$s liegt die Stabilität hier recht niedrig. Mit zunehmender Menge an Clustern, sind die Ergebnisse stabiler, was auch der höheren Anzahl an verschiedenen Wertausprägungen dieser Attribute zuzuschreiben ist.

Die Verwendung aller vier Attribut-Typen weist durch alle Ebenen eine adäquate Stabilität auf.

![Qualität der Clusterings nach Typen über alle $k$s \label{fig:casesqual}](img/cases-types-quality.png)

Grafik \ref{fig:casesqual} zeigt die Qualität (also den Silhouetten-Koeffizienten) der Clusterings über die verschiedenen $k$s. Bei sehr hohen Anzahlen an Clustern sinkt der Koeffizient bei allen Versuchen ab, um auf der letzten Stufe fast bei $0$ zu landen. Das liegt daran, dass viele Punkte sehr nahe zueinander liegen, aber dennoch in unterschiedliche Cluster sortiert werden müssen (aufgrund des hierarchischen Verfahrens). Bei geringen Clusterzahlen steigt der Wert zunächst an, um anschließend gegen $0$ zu laufen. Der Hochpunkt zeigt dabei die "optimale" Clusterzahl an, bei der das Datenset am schärfsten getrennt ist. Dieser Hochpunkt kann z.B. genutzt werden, um die optimale Clusterzahl für ein partitionierendes Verfahren zu finden. Das aber nur am Rande.

Alle Clusterings, welche String-Attribute enthalten, weisen eine sehr niedrige Qualität auf, bevor die gegen Ende komplett absinken. Die Verwendung ausschließlich numerischer sowie numerischer und kategorischer Attribute zusammen erreicht für die mittleren Hierarchie-Ebenen sehr hohe Werte. Die numerischen erreichen ihren Höchststand zwischen $k=9$ und $k=23$. Auch die Clusterzahl für die passenden Smartphone-Modelle ($k=11$) liegt in diesem Bereich. Die numerischen Werte bestehen aus Attributen wie "Maximum Screen Size", "Width" und "Height", welche tatsächlich Informationen für die Zuordnung zu den geeigneten Smartphone-Modellen enthalten (die verschiedenen Modelle von Samsung zeichnen sich u.a. durch unterschiedliche Bildschirm-Diagonalen und -Größen aus).

Die Kombination aus numerischen und kategorischen Attributen erreicht die höchste Qualität über das gesamte Spektrum. Die höchsten Werte liegen hier zwischen $k=20$ und $k=40$. Die optimale Clustereinteilung scheint also eher in diesem Bereich zu liegen.

Dadurch kam eine Vermutung auf: Vielleicht liegen die Ergebnisse für die Erkennung der Smartphone-Generation und -Modelle so niedrig, weil sich die Hüllen verschiedener Hersteller für das gleiche Gerät zu stark unterscheiden. Vielleicht ist es sinnvoller die Hüllen zuerst nach Hersteller zu sortieren und anschließend das Clustering auf die Generationen und Modelle zu prüfen. Die folgende Tabelle zeigt genau diesen Versuch:

| Typen | Hersteller | Generation | Modell |
|-|-:|-:|-:|
| | $k=4$ | $k=8$ | $k=25$ |
| numerisch   | 0.32 | 0.17 | 0.27 |
| kategorisch | 0.71 | 0.61 | 0.31 |
| multi-kat.  | 0.26 | 0.35 | 0.16 |
| string      | 0.04 | 0.43 | 0.48 |
| num+kat     | 0.76 | 0.65 | 0.61 |
| num+kat+str | 0.75 | 0.76 | 0.55 |
| alle        | 0.69 | 0.63 | 0.55 |
: Adjusted-Rand-Index für die Einteilung der Cluster nach Hersteller

Es sind wieder einige ausgewählte Kombinationen an Attribut-Typen dargestellt. Der Adjusted-Rand-Index wurde genutzt, um die Übereinstimmung zwischen den Clusterings und den Produkten gruppiert nach Hersteller ($k=4$), gruppiert nach Hersteller und Smartphone-Generation ($k=8$) sowie gruppiert nach Hersteller und Smartphone-Modell ($k=25$) zu berechnen.

Die Werte liegen nun deutlich höher als vorher. Vor allem das Clustering mit numerischen und kategorischen Attributen gleichzeitig liefert auf allen Stufen sehr hohe Übereinstimmungen. Ebenso liefert die Verwendung aller Attribute recht hohe Übereinstimmungen, wenn auch nicht die besten Werte.

Insgesamt lässt sich feststellen, dass die Kombination aus numerischen und kategorischen Attributen im Schnitt die besten Ergebnisse liefern. Das eine multi-kategorische Attribute (Material) hat, wie bereits beschrieben, keinen sinnvollen Einfluss auf das Clustering. Sehr ambivalent ist der Einfluss von String-Attributen zu werten. Für sich alleine genommen, können sie die Erkennung der Smartphone-Generation, für die eine Hülle geeignet ist, positiv unterstützen. Allerdings senken sie in Kombination mit anderen Attributen die Qualität des Clusterings erheblich ab.

#### Vergleich nach Erforderlichkeit

| Typen | Auswahl | Stabilität | Qualität | Erkennung | |
|-|-|-:|-:|-:|-:|-:|
| | | | | *Generation* | *Modell* |
| numerisch   | alle | 0.85 | 0.43 | 0.15 | 0.45 |
|             | erf. | 0.79 | 0.43 | 0.10 | 0.61 |
| kategorisch | alle | 0.44 | 0.39 | 0.08 | 0.12 |
|             | erf. | 0.45 | 0.40 | 0.04 | 0.04 |
| num+kat     | alle | 0.88 | 0.52 | 0.09 | 0.26 |
|             | erf. | 0.90 | 0.48 | 0.11 | 0.25 |
| alle        | alle | 0.92 | 0.29 | 0.12 | 0.25 |
|             | erf. | 0.80 | 0.26 | 0.13 | 0.15 |
: Clustering der Hüllen mit erforderlichen und optionalen Attributen

#### Vergleich nach menschlicher Auswahl

### Attribut-Gewichtung

### Zusammenfassung

## Datenset "Smartphones"

### Überblick

| Typ | erforderlich | Anzahl | Ø non-`null` | Ø unique |
|-|-|-:|-:|-:|
| numerisch   | ja   |  $8$ | $41.1$ |  $5.4$ |
| numerisch   | nein | $48$ | $18.5$ |  $3.5$ |
| kategorisch | ja   | $19$ | $37.9$ |  $1.6$ |
| kategorisch | nein | $87$ | $26.1$ |  $1.2$ |
| multi-kat.  | ja   |  $3$ | $38.7$ |  $7.0$ |
| multi-kat.  | nein | $19$ | $23.1$ |  $2.9$ |
| string      | ja   |  $5$ | $40.8$ | $24.0$ |
| string      | nein |  $6$ | $18.0$ |  $4.8$ |
: Übersicht zu den Attributen der Smartphones

### Verarbeitung multi-kategorischer Attribute

| Verarbeitung | Stabilität | Qualität | Erkennung | | |
|-|-:|-:|-:|-:|-:|-:|
| | | | *Generation* | *Modell* | *Duplikate* |
| multi-kategorisch    | 0.91 | 0.39 | 0.40 | 0.45 | 0.89 |
| (single) kategorisch | 0.85 | 0.38 | 0.12 | 0.30 | 0.88 |
: Clustering der Smartphones mit multi-kategorischen Attributen

=> alle multi-kat

| Verarbeitung | Stabilität | Qualität | Erkennung | | |
|-|-:|-:|-:|-:|-:|-:|
| | | | *Generation* | *Modell* | *Duplikate* |
| Strings als multi-kat.  | 0.91 | 0.34 | 0.64 | 0.87 | 1.00 |
| Strings als single-kat. | 0.80 | 0.23 | 0.14 | 0.58 | 1.00 |
: Clustering der Smartphones mit String-Attributen

### Attribut-Auswahl

#### Vergleich nach Datentypen

| Typen | Stabilität | Qualität | Erkennung | | |
|-|-:|-:|-:|-:|-:|-:|
| | | | *Generation* | *Modell* | *Duplikate* |
| numerical   | 0.88 | 0.43 | 0.01 | 0.75 | 0.96 |
| categorical | 0.96 | **0.45** | **0.65** | 0.49 | 0.81 |
| multi       | 0.91 | 0.39 | 0.40 | 0.45 | 0.89 |
| string      | 0.91 | 0.34 | 0.64 | 0.87 | **1.00** |
| num+cat     | 0.98 | 0.43 | **0.65** | 0.71 | 0.96 |
| num+mul     | 0.94 | 0.39 | 0.16 | 0.70 | **1.00** |
| num+str     | 0.93 | 0.38 | 0.01 | 0.67 | 0.97 |
| cat+mul     | 0.89 | 0.39 | 0.11 | 0.49 | 0.92 |
| cat+str     | **0.99** | 0.40 | **0.65** | 0.42 | 0.94 |
| mul+str     | 0.85 | 0.32 | 0.37 | 0.49 | 1.00 |
| num+cat+mul | 0.98 | 0.41 | 0.16 | 0.70 | 0.97 |
| num+cat+str | 0.98 | 0.41 | **0.65** | 0.66 | 0.96 |
| num+mul+str | 0.92 | 0.37 | 0.16 | 0.70 | **1.00** |
| cat+mul+str | 0.95 | 0.37 | 0.11 | 0.45 | 0.96 |
| alle        | 0.92 | 0.39 | 0.16 | 0.70 | **1.00** |
: Clustering der Smartphones mit verschiedenen Kombinationen an Attribut-Typen

#### Vergleich nach Erforderlichkeit

| Typen | Auswahl | Stabilität | Qualität | Erkennung | | |
|-|-:|-:|-:|-:|-:|-:|
| | | | | *Generation* | *Modell* | *Duplikate* |
| numerisch   | alle | 0.88 | 0.43 | 0.01 | 0.75 | 0.96 |
|             | erf. | 0.96 | 0.48 |-0.04 | 0.48 | 0.97 |
| kategorisch | alle | 0.96 | 0.45 | 0.65 | 0.49 | 0.81 |
|             | erf. | 0.76 | 0.44 | 0.55 | 0.46 | 0.75 |
| multi-kat.  | alle | 0.91 | 0.39 | 0.40 | 0.45 | 0.89 |
|             | erf. | 0.70 | 0.38 | 0.51 | 0.24 | 0.86 |
| string      | alle | 0.91 | 0.34 | 0.64 | 0.87 | 1.00 |
|             | erf. | 0.94 | 0.37 | 0.17 | 0.53 | 0.96 |
| num+kat     | alle | 0.98 | 0.43 | 0.65 | 0.71 | 0.96 |
|             | erf. | 0.91 | 0.42 |-0.04 | 0.61 | 0.89 |
| alle        | alle | 0.92 | 0.39 | 0.16 | 0.70 | 1.00 |
|             | erf. | 0.89 | 0.34 | 0.30 | 0.71 | 0.96 |
: Clustering der Smartphones mit erforderlichen und optionalen Attributen

#### Vergleich nach menschlicher Auswahl

### Attribut-Gewichtung

## Kombiniertes Datenset

### Verwendung aller Attribute

### Verwendung gemeinsamer Attribute

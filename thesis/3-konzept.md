# Konzeption

## Überblick

- möglichst realistische Datenquellen => Akeneo-PIM + Icecat Datenkatalog
- Clustering mittels möglichst effizienten Verfahren
  - dabei verschiedene Attribute, Datentypen, Gewichtungen probieren
  - möglichst ohne "externe" Informationen clustern können
- Evaluation => ist clustering sinnvoll => Was ist sinnvoll?
- Überblick über das Vorgehen

## Datenquellen und -sets

### Akeneo-PIM

#### Überblick

- open source PIM-System
- weite Verbreitung
- typischer Funktionsumfang
- große Menge an Addons/Plugins (u.a. Icecat Importer)

#### Systemübersicht

- Microservice Cluster
- Frontend UI
- Rest-Api

#### Datenstrukturen

- viele Verschiedene: AUFZÄHLUNG...
- nur einige relevant => genauerer Blick

##### Product & Product Values

- Meta-Values
- "values" Eintrag ist Mapping: attribute.code => product_value

##### Category

- Baumstruktur für Kategorisierung

##### Family

- definiert Attribute pro Family und required/optional

##### Attribute & Attribute Group

- verschiedene Typen + Constraints

##### Channel, Currency, Locale

- alles lokalisierbar (Sprache und Währung)
- zusätzlich noch scopes => verschiedene Werte für gleiche Locale z.B. Web und Mobile

##### Measurement Family

- Maßeinheiten mit Umrechnung

### Icecat Produkt-Katalog

- offener Katalog mit XXXXXXXX Produktdaten
- einigermaßen standardisiert nach UNSPEC-Taxonomy

### Datenset

#### Anforderungen

- Produkte mit wenigen Attributen
- Produkte mit vielen Attributen
- unterschiedliche aber naheliegende Kategorien
- Produkte mit Variationen und verschiedenen Generationen
- Duplikate

#### Umsetzung

- Smartphone-Hüllen speziell für Samsung Galaxy Reihe
- Smartphones aus Samsung Galaxy Reihe S20 und S21 + Versionen und Farben
- evtl. noch weitere Smartphones
- evtl. ein paar Tablets
- evtl. noch was ganz anderes wie Ladegeräte o.ä.

## Clustering

### Clustering-Verfahren

Anforderungen:

- hierarchisch wünschenswert
  - mehr Informationen ableitbar
  - Anzahl an Clustern dynamisch ableitbar
- gute Laufzeit => potenziell hohe Menge an Produkten
- Verarbeitung verschiedenster Datentypen in den Attributen

Ansatz: Bisecting K-Prototypes mit Custom-Varianten von Distanzfunktionen

### Distanzfunktion

#### Anforderungen

- Berechnung der Distanz + Berechnung des Mittelpunkts
- Kombi von verschiedenen Datentypen
- viele Null-Values

| Datentyp | Akeneo-Typ | Distanzmaß | Centroid |
|--|---|-|-|
| numerisch | Number, Metric, Price, Date | Minkowski | mean |
| kategorisch | Bool, SelectSingle, ReferenceDataSingle | Jaccard | mode |
| multi-kategorisch | SelectMulti, ReferenceDataMulti | Jaccard+ | mode |
| strings | Text, Textarea | ? | ? |
| Datei | File, Image | - | - |
| Id | Identifier | - | - |

: Verarbeitung der Akeneo-Attribut-Typen

#### Herleitung der Funktion

- $d(p_1, p_2) = \frac{v+n+c+m+?}{|p_1^{attr} \cup p_2^{attr}|}$
- $v = | p_1^{attr} \setminus p_2^{attr} \cup p_2^{attr} \setminus p_1^{attr} |$
- $n = \sum_{x \in p_1^{num_i} , \ y \in p_2^{num_i}} |x-y|$
- $c = \sum_{x \in p_1^{cat_i},\ y \in p_2^{cat_i}} q(x,y)$
- $q(x,y)= \begin{cases}
  0, & x = y \\
  1, & x \neq y
\end{cases}$
- $m = \sum_{x \in p_1^{mul_i},\ y \in p_2^{mul_i}} 1 - \frac{|x \cap y|}{|x \cup y|}$

...weitere Erklärungen etc...

Umgang mit verschiedenen Versionen der Funktion?

## Evaluation

- Ziel: sinnvolle Cluster finden => Was heißt das?

### Stabilität der Cluster

- Hintergrund:
  - Clustering ist wertlos, wenn Zuordnung zufällig erfolgt
  - Clustering sollte stabil, reproduzierbar & weitestgehend deterministisch sein
- mehrmaliges Clustern (gleiche Settings):
  - K-Means mit random init => evtl. unterschiedliche Ergebnisse bei verschiedenen Durchläufen
  - gute Distanzfunktion => klare Separierung der Produkte
  - je größer die Ähnlichkeit zwischen zwei Clusterings, desto stabiler
  - Bewertung der Ähnlichkeit mittels Jaccard-Koeffizient
- Analyse der Auswirkung Settings
  - Clustern mit verschiedenen Attributen/Gewichtungen
  - Bewertung der Ähnlichkeit der Clusterings
  - ebenfalls Jaccard-Koeffizient

### Internal Indices

- allgemeine Stats zum Clustering:
  - durchschnittlicher Error
  - Entwicklung über Hierarchien
  - Anzahl an Produkten

=> eher untergeordnete Rolle, eventuell weglassen ???

### External Indices

- Hintergrund:
  - bisher nur Aussage wie ähnliche/verschieden die Clusterings sind
  - Frage ist noch: Wenn Clusterings unähnlich,welches ist "besser"
  - Ansatz => Inspiration aus möglichen Anwendungen:
    - Auto-Kategorisierung
    - Einordnung neuer Produkte zu bestehenden (transitive Erkenntnisse)
    - Finden von Alternativ-Produkten mit gleichen Eigenschaften
    - Finden von Duplikaten
- Vergleich mit Akeneo Families und Akeneo Categories
  - Families: ähnliche Attribute, sollten sich ähnlich sein, eher technischer Check
  - Categories: menschengemachte Labels, spiegeln die intuitive Zuordnung wieder
  - Analyse der Ähnlichkeit zwischen Clustering und Families/Categories
- speziellere Checks:
  - bewusst eingefügte Duplikate => solange wie möglich im gleichen Cluster (top-down  clustering)
  - Produkte unterschiedlicher Kategorien, aber mit Bezug (z.B. Smartphone plus Hülle) => bleiben sie länger im gleichen Cluster als andere Produkte dieser Kategorien?

## Vorgehen / Versuche ?

### Set "Samsung Galaxy Cases"

- Smartphone Hüllen für Samsung Galaxy Reihe sowohl 
- überschaubar wenig Attribute

Versuch: Basis-Prozess, Fehler finden

- clustern nach einander mit numerisch + kategorisch (+ multi-kategorisch)
- Prozess und "Pipeline" aufsetzen

Versuch: gleiche Modelle

- Clustering soll Hüllen für gleiches Smartphone-Modell finden
- werden in Akeneo Categories vorher hinterlegt, Vergleich damit
- numerisch & kategorisch => einzeln und zusammen
- (multi-kategorisch => hier noch nicht möglich, da solche keine Attribute)
- gleich-gewichtet vs menschen-gewichtet

### Set "Samsung Galaxy S 20er-Reihen"

- Smartphones Samsung Galaxy S 20 und 21 Modelle
- verschiedenen Versionen (Größen) und Farben
- sehr viel Attribute
- enthält Duplikate

Versuch: gleiche Modelle finden

- Clustering soll gleiche Modelle/Baureihen finden
- werden in Akeneo Categories vorher hinterlegt, Vergleich damit
- vor allem interessant: nur required Attribute vs optionale hinzunehmen => wird es dadurch besser oder schlechter?
- multi-kategorisch ebenfalls auswerten => macht es einen Unterschied?
- gleich-gewichtet vs menschen-gewichtet

Versuch: Duplikate finden

- Duplikate sollten sehr lange im gleichen Cluster sein
- eventuell zusammen mit dem vorherigen Versuch evaluieren ???
- Hauptfrage: gleiche Settings für beide Aufgaben nutzbar?

### Set "Samsung Galaxy Smartphones und Hüllen"

- Kombi beider Sets
- Clustering mit gefundenen Konfig(s)
- Frage: Assoziation zwischen Modellen sichtbar?

...

### weiteres ?

- weitere Versuche?
- eventuell durch Hinzunehmen von Smartphones und Hüllen anderer Hersteller ?
- weitere Produktgruppe – ähnlich aber schon anders z.B. Tablets?
- weitere Produktgruppe – ganz anders z.B. andere Elektroartikel?

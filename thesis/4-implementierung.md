# Implementierung

## Überblick

- Akeneo-PIM Instanz auf adesso VM
- AKeneo Client und Cache
- Import von Daten aus Icecat
- Implementierung Clustering-Bibliothek + weitere (z.B. Datenaufbereitung)
- Durchführung des Clusterings selbst

## Akeneo-PIM

### Installation und Deployment

- Überblick zur Projekt-Initialisierung
- Installation auf adesso VM
- Icecat Importer
- Anlegen verschiedener Basis-Attribute für Icecat

### Akeneo-Client und -Cache

- Klasse zur Interaktion mit Akeneo-Api, behandelt Authentifizierung, Auflösung von Listen etc.
- Requests dauern mit unter einige Sekunden
- Cache fragt alle wichtigen Endpunkte ab und speichert JSON-payload in JSON-Dateien
- Abfrage von Daten aus dem Cache (lädt und parsed JSON-Dateien in Python-Datenstrukturen "dacite" Package)

## Datenset

- Icecat Taxonomy => Import der Attribute
- händische Auswahl aller zu importierenden Attribute
- Suche nach Produkten auf icecat.biz
- Beschränkung auf Sponsoren-Vendors
- Import der Produkte mittels SKU und EAN; dann Icecat Importer "Enrich Products"
- Analyse der Daten und Korrektur verschiedener Fehler:
  - Multi-Select werden als Single-Select importiert
  - einige Single-Selects als Text
  - Import diverser "number" Attribute schlägt fehl => Import als Text und anschließend Umwandlung
  - Fix: Attribut dupliziert mit suffix "_fixed" und korrektem Typ
  - Außerdem: fehlerhafter Import diverser metrischer Attribute (wahrscheinlich Unit nicht richtig erkannt), aber ist bei allen gleich fehlerhaft importiert => wird eh normalisiert, daher ignoriert

- Statistiken zu Datenset: Attribute, Categories, Families, Produkte

## Clustering

### Überblick zu externen Libraries

- sklearn, nicovk
- erlauben keine null-Values !
- Umsetzung von Multi-Selects nicht möglich
- Orientierung an diesen Bibliotheken, aber keine Verwendung

### Clustering-Package

- KMeans & Bisecting KMeans mit generischer Centroid-Klasse
- Centroid-Klasse erklären
- KMeans => Überblick
- Bisecting KMeans => Überblick

### Distanzfunktionen

- Implementierung der Centroid-Klasse
- Map aus Attribut-Code zu Wert in Datentypen: float, string, set of strings
- Verarbeitung des Typs entsprechend
- Tracking des Means und der Modes je nach Attribut => Generierung eines künstlichen Datenpunktes für Distanzfunktion
- Gewichtung der Attribute möglich

### Datenvorbereitung

- Produkte parsen:
- mit Filtern
- Normalisierung von float
- Tokenization von strings => Umwandlung in set of strings, genauso wie Multi-Selects

## Evaluation

- Verwendung von metrics Funktionen aus SKLearn
- Durchführung mit Python-Packages in Jupyter-Notebooks
- Generierung aller möglichen Versuche
- Stabilität => 10 mal wiederholen da KMeans mit random-init, Vergleich mit adj_rand_index
- Qualität => Silhouettenkoeffizient, da in SKLearn am flexibelsten einsetzbar
- Korrektheit => Vergleich mit Categories (Smartphone Serien und Modellen) mit adj_rand_index

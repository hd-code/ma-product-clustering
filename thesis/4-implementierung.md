# Implementierung

## Überblick

Nach der Konzeption folgte die Umsetzung und Implementierung des Praxisteils. Für eine bessere Übersicht ist in der folgenden Grafik die Architektur in detaillierterer Form inklusive implementierter Klassen und sonstigen Software-Komponenten dargestellt.

![Detaillierte Architektur der praktischen Umsetzung](img/architecture-detail.png)

adesso stellte für diesen Teil einen Server bereit, welcher für das Hosting von Akeneo-PIM genutzt wurde. Anschließend erfolgte die Installation von Akeneo-PIM Community Edition Version 5.0 auf diesem Server. Dazu wurde die offizielle Installationsanleitung von Akeneo unter Verwendung der Containerization-Lösung Docker (<https://www.docker.com/>) befolgt [@akeneo2022install]. Zusätzlich wurde das Akeneo-Plugin "Akeneo Icecat Connector" Version 2.0.0 [@akeneo2022icecat] in die Instanz integriert. Das kostenpflichtige Plugin wurde von adesso gesponsert.

Nun musste Akeneo-PIM mit Produktdaten gefüllt werden, welche aus dem Online-Katalog Icecat stammen. Eine genaue Übersicht zur Auswahl der Produkte sowie der weiteren Aufbereitung innerhalb von Akeneo siehe Abschnitt [Datenset](#datenset).

Anschließend erfolgte die Implementierung diverser Klassen und Packages, welche das hergeleitete Konzept umsetzen oder wichtige Hilfsfunktionalitäten für die spätere Evaluation liefern. Alle diese Komponenten sind in der Programmiersprache Python (<https://www.python.org/>) implementiert worden. Python ist sehr weit verbreitet für Aufgaben der Datenanalyse bzw. Data Science allgemein. Das liegt daran, dass es eine Vielzahl nützlicher Bibliotheken für die Analyse und Aufbereitung von Daten gibt. Ebenso sind Implementierungen vieler Algorithmen und Verfahren in Python verfügbar [@papp2019, Kap. 2.4.2 Programmierung]. Zu den meisten umgesetzten Elementen ist ebenfalls grundlegendes Unit-Testing durchgeführt worden, um die korrekte Funktionalität zu prüfen.

Das Package `akeneo` liefert zwei Hauptkomponenten. Der `AkeneoClient` kommuniziert mit der REST-API von Akeneo zum Abrufen der hinterlegten Daten. Ebenso konnten damit verschiedene Aufgaben, wie das Zuordnen der Produkte zu ihren passenden Kategorien teilweise automatisiert werden. Der `AkeneoCache` nutzt den `AkeneoClient`, um alle Endpunkte, welche Daten zurückgeben, abzufragen. Die `JSON`-Payloads dieser Anfragen werden anschließend in `JSON`-Dateien gespeichert. Die REST-Anfragen dauern mit unter recht lange (mehrere Sekunden), allerdings änderte sich das Datenset nach der Erstellung nicht mehr. Durch diese Zwischenspeicherung wurde die Evaluation erheblich beschleunigt, da die Daten direkt aus den Dateien gelesen werden konnten. Der `AkeneoCache` kann die gespeicherten Daten ebenfalls laden und zur Verfügung stellen. Dazu werden die `JSON`-Objekte in Python-Datenstrukturen umgewandelt. Dazu kam das Tool `dacite` (<https://github.com/konradhalas/dacite>) zum Einsatz.

Zunächst wurde überprüft, ob externe Clustering-Bibliotheken in der Lage sind, das erarbeitete Konzept umzusetzen. Da keine Bibliothek den Anforderungen genügte, wurde im Package `clustering` eine generische Version des `KMeans` und `BisectingKMeans` implementiert. Sie nutzen ein allgemeines Interface `Centroid`, welches für eine konkrete Clustering-Anwendung vorher implementiert werden muss. Genauere Details dazu in Abschnitt [Clustering](#clustering).

Das Package `akeneo_clustering` bringt nun die beiden anderen Packages zusammen. Die Funktion `parse_products()` liest die Daten aus dem Cache aus und bereitet die Produkte für das Clustering auf. Dabei werden zum Beispiel die beschriebenen Vorverarbeitungen für numerische und String-Attribute durchgeführt. Die `Centroid`-Klasse implementiert das Interface für das `clustering`-Package. Hier ist die erarbeitete Distanzfunktion hinterlegt, ebenso der genaue Prozess, wie Mittelpunkte zu den jeweiligen Clustern berechnet werden. Weitere Details im Abschnitt [Clustering](#clustering)

Abschließend fand die Evaluation mithilfe von Jupyter-Notebooks statt. Das sind Source-Code-Dateien, die in einzelne Code-Zellen unterteilt sind. Mithilfe eines Webfrontends, welches Jupyter mitliefert, können die Notebooks interaktiv verändert und beliebig einzelne oder mehrere Code-Zellen ausgeführt werden. Die Ausgaben der Zellen erscheinen direkt darunter. Dadurch eignet sich Jupyter für Analysen, in denen wiederholt Versuche und leichte Abwandlungen dieser durchgeführt werden. Die direkte Visualisierung beschleunigt den Evaluationsprozess [@papp2019, Kap. 2.4.2 Programmierung]. Die genauen Schritte der Evaluation und welche Tools zur Berechnung der Metriken zum Einsatz kamen, ist im Abschnitt [Evaluation](#evaluation) beschrieben.

## Datenset

### Auswahl und Import

### Analyse und Korrektur

### Übersicht

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

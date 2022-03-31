# Implementierung

- Akeneo-PIM:
  - auf Server von adesso
  - Akeneo Icecat Connector
  - Import der Daten
- Python Modules:
  - Akeneo Client => holt Daten aus Akeneo-PIM und dumpt in json Dateien => "raw data"
  - Akeneo Parser => parsing von json in Python-Strukturen (dataclasses) => "cleaned data"
  - Akeneo Clustering => Filtern der Attribute, Vorverarbeitung fürs Clustering
  - Clustering => eigene Implementierung des Bisecting K-Means mit generischen Datenstrukturen
  - Evaluation => Hilfsmethoden zur Auswertung der Ergebnisse
- Jupyter Notebooks:
  - Akeneo Rest Api Exploration
  - Clustering Basis Example (2d Vektoren)
  - verschiedene Iterationen des Clusterings und Distanzfunktionen

...

# BESS Trading Optimizer

Optimierungsmodell zur Erlösmaximierung eines Großbatteriespeichers (BESS) am deutschen Strom- und Regelleistungsmarkt, entwickelt mit Python und Pyomo.

Das Projekt entstand im Rahmen meiner Bachelorarbeit an der HTW Berlin (Note 1,0):
*„Entwicklung und Auswertung eines numerischen Modells zur Maximierung des Profits von Großbatteriespeichern am deutschen Strom- und Regelleistungsmarkt“*

## Worum geht es?

Ein Batteriespeicher kann seine Leistung in jedem Zeitpunkt nur einmal vermarkten: entweder im Energiehandel (Day-Ahead, Intraday) oder als Regelleistung (PRL/FCR, SRL/aFRR). Das Modell bestimmt für historische Marktdaten, welche Vermarktung zu welchem Zeitpunkt den höchsten Gewinn bringt, unter Berücksichtigung der technischen Grenzen und der Alterung der Batterie.

## Modell im Überblick

**Ansatz:** Gemischt-ganzzahlige lineare Optimierung (MILP) mit Perfect Foresight, gelöst mit Gurobi.

**Zielfunktion:** Maximierung des Gewinns = Markterlöse − Alterungskosten − Steuern

**Märkte**
- Day-Ahead- und Intraday-Auktion (15-Minuten-Auflösung)
- Primärregelleistung (PRL/FCR) in 4-Stunden-Blöcken
- Sekundärregelleistung (SRL/aFRR), Leistungs- und Arbeitspreis, positiv und negativ
- Marktwahl je Zeitintervall über Binärvariablen (gegenseitiger Ausschluss)

**Technische Modellierung**
- Ladezustand, Lade-/Entladeleistung und Systemwirkungsgrad (Batterie, Wechselrichter, Trafo, Kühlung, Verteilung)
- Kapazitätsdegradation, kalendarisch und zyklisch, abhängig von Ladezustand und C-Rate
- Wirkungsgraddegradation über die Lebensdauer
- Äquivalente Vollzyklen mit SoC-abhängiger Gewichtung, optional Zyklenbegrenzung pro Tag

**Wirtschaftliche Modellierung**
- CAPEX und OPEX, spezifische Alterungskosten pro Zyklus
- Steuern und Abschreibung

**Simulation über die Lebensdauer:** Die Optimierung läuft monatsweise. Batteriekapazität, Wirkungsgrad, Zyklenzahl und Ladezustand werden jeweils in den nächsten Monat übernommen, bis die Restkapazität 80 % (End of Life) erreicht.

## Projektstruktur

```
├── api/                 # Datenabruf über die ENTSO-E-Transparenzplattform
├── dataloader/          # Einlesen und Aufbereiten der Marktdaten
├── model/
│   ├── constraints/     # Nebenbedingungen (Märkte, PRL, SRL, Zyklen, Degradation …)
│   ├── expressions/     # Erlöse, Alterungskosten, Steuern …
│   ├── model_builder.py # Aufbau und Lösen des Pyomo-Modells
│   └── objective.py     # Zielfunktion
├── params/              # Szenario-Konfiguration (Batterie, Kosten, Märkte)
├── result_processing/   # Extraktion und Export der Ergebnisse
├── scripts/             # Pipelines: Daten laden, optimieren, visualisieren
├── visualization/       # Auswertungsgrafiken
├── config_degradation.py
└── cost_calculator.py
```

Namenskonventionen für Variablen, Parameter und Constraints sind in [NAMING.md](NAMING.md) beschrieben.

## Ergebnisse

<!-- Hier 1–2 Grafiken einfügen, z. B. Erlöse je Markt pro Monat:
![Erlöse je Markt](docs/erloese_maerkte.png)
Und 2–3 Sätze zu den wichtigsten Erkenntnissen der Arbeit. -->

## Nutzung

```bash
pip install -r requirements.txt
```

Voraussetzungen:
- Gurobi mit gültiger Lizenz (für Studierende kostenlos)
- Marktdaten im Ordner `data/` (nicht im Repository enthalten, siehe unten)
- Für den Datenabruf: ENTSO-E-API-Key als Umgebungsvariable `ENTSOE_API_KEY`

Szenario in `params/scenario_config.py` anpassen, dann:

```bash
python -m scripts.optimisation_backtest
python -m scripts.visualisation_pipeline
```

## Datenquellen

Die Rohdaten sind aus Lizenz- und Größengründen nicht im Repository enthalten. Verwendet wurden:
- Day-Ahead- und Intraday-Preise: Energy-Charts (Fraunhofer ISE)
- PRL- und SRL-Ausschreibungsergebnisse: regelleistung.net
- SRL-Arbeitspreise (aFRR): ENTSO-E-Transparenzplattform
- SRL-Sollwerte: Netztransparenz.de

## Technologien

Python · Pyomo · Gurobi · pandas · NumPy · matplotlib · seaborn · entsoe-py

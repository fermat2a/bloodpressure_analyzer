# Blood Pressure Analyzer

Ein Python-Programm zur Analyse und Visualisierung von Blutdruckdaten aus CSV-Dateien.

## Funktionen

- Lädt Blutdruckdaten aus CSV-Dateien
- Filtert Daten nach Zeiträumen
- Erstellt separate Listen für Morgen- und Abendmessungen
- Generiert Liniendiagramme für alle Datensätze
- Erstellt Durchschnitts- und Standardabweichungsdiagramme
- Generiert einen umfassenden PDF-Bericht mit Tabellen und Diagrammen

## Verwendung

### Einfache Ausführung mit dem Bash-Skript:

```bash
./run_analyzer.sh <CSV-Datei> [--start "YYYY-MM-DD HH:MM:SS"] [--end "YYYY-MM-DD HH:MM:SS"]
```

### Beispiele:

```bash
# Alle Daten analysieren
./run_analyzer.sh bloodPressure.csv

# Mit der Beispieldatei
./run_analyzer.sh bloodpressure_example.csv

# Daten ab einem bestimmten Zeitpunkt
./run_analyzer.sh bloodPressure.csv --start "2025-09-25 00:00:00"

# Daten in einem bestimmten Zeitraum
./run_analyzer.sh bloodPressure.csv --start "2025-09-25 00:00:00" --end "2025-09-30 23:59:59"
```

### Direkte Python-Ausführung:

```bash
python3 blood_pressure_analyzer.py <CSV-Datei> [--start "YYYY-MM-DD HH:MM:SS"] [--end "YYYY-MM-DD HH:MM:SS"]
```

## CSV-Format

Die CSV-Datei muss folgende Spalten enthalten:
- `Date`: Zeitstempel im ISO-Format (z.B. 2025-09-23T21:00:51.000+02:00)
- `SYS`: Systolischer Blutdruck
- `DIA`: Diastolischer Blutdruck  
- `BPM`: Puls (Beats per Minute)

Beispiel:
```csv
Date,SYS,DIA,BPM
2025-09-23T21:00:51.000+02:00,137,80,66
2025-09-24T10:05:37.000+02:00,119,70,65
```

### Testdaten

Eine Beispieldatei `bloodpressure_example.csv` ist enthalten mit:
- 34 realistische Blutdruckmessungen
- Zeitraum: 1.-17. Oktober 2025
- Morgen- und Abendmessungen
- Variation in den Werten für aussagekräftige Diagramme

## Ausgabedateien

Das Programm erstellt folgende Dateien:

### SVG-Diagramme:
- `bloddpressure_complee.svg`: Liniendiagramm aller Daten
- `bloodpressure_morning.svg`: Liniendiagramm der Morgenmessungen
- `bloodpressure_evening.svg`: Liniendiagramm der Abendmessungen  
- `bloodpressure_moning_evening.svg`: Kombiniertes Diagramm von Morgen- und Abendmessungen
- `bloodpressure_average.svg`: Durchschnittswerte mit Standardabweichung

### PDF-Bericht:
- `bloodpressure.pdf`: Umfassender Bericht mit:
  - Titelseite mit Zeitraum (DIN A4 Querformat)
  - Diagramm aller Blutdruckdaten (DIN A4 Querformat)
  - Kombiniertes Morgen-Abend-Vergleichsdiagramm (DIN A4 Querformat)
  - Durchschnittsdiagramm mit Standardabweichung (DIN A4 Querformat)
  - Datentabelle mit Farbkodierung (DIN A4 Querformat)
  - Legende für Farben

## Datenfilterung

### Morgendaten (`bloodpressure_morning`):
- Erste Messung des Tages
- Zeitraum: 04:00 - 12:00 Uhr

### Abenddaten (`bloodpressure_evening`):
- Letzte Messung des Tages
- Zeitraum: ab 18:00 Uhr

### Farbkodierung in der Tabelle:
- **Gelb**: Morgenmessungen
- **Orange**: Abendmessungen

## Systemanforderungen

- Python 3.7 oder höher
- pip (Python Package Installer)

### Automatisch installierte Python-Pakete:
- matplotlib >= 3.5.0
- pandas >= 1.3.0
- numpy >= 1.21.0

## Setup

Das Bash-Skript `run_analyzer.sh` führt automatisch folgende Schritte aus:

1. Erstellt ein Python Virtual Environment (falls nicht vorhanden)
2. Aktiviert das Virtual Environment
3. Installiert alle benötigten Pakete
4. Führt das Analyseprogramm aus

## PDF-Format

Alle Seiten im PDF-Dokument verwenden das **DIN A4 Querformat** (11.69 × 8.27 Zoll):
- Optimiert für die Darstellung von Diagrammen
- Bessere Nutzung der Seitenbreite für Zeitachsen
- Professionelle Darstellung für medizinische Berichte

## Fehlerbehandlung

- Überprüft Existenz der CSV-Datei
- Validiert Zeitstempel-Format
- Behandelt leere Datensätze
- Zeigt aussagekräftige Fehlermeldungen

## Autor

Sascha Effert - Blood Pressure Data Analysis Tool

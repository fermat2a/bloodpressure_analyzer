# Blood Pressure Analyzer

> **🤖 ENTWICKLUNGSHINWEIS**  
> **Dieses Programm ist durch Verwendung von GitHub Copilot mit Hilfe von Visual Studio Code entstanden. Mit diesem Programm will ich die Fähigkeiten dieser Werkzeuge evaluieren. Daher versuche ich keine manuellen Eingriffe in dieses Projekt zu machen, die gesamte Bearbeitung aller Dateien, inkl. Dokumentation und git commit messages wird von github copilot erledigt.**

Ein Python-Programm zur Analyse und Visualisierung von Blutdruckdaten aus CSV-Dateien oder direkt von Withings Blutdruckmessgeräten.

## Funktionen

- **Lädt Blutdruckdaten aus CSV-Dateien** - Für manuelle Datenimporte
- **🩺 Automatischer Import von Withings API** - Direkt von Ihren Blutdruckmessgeräten (BPM Connect, BPM Connect Pro, BPM Core)
- Filtert Daten nach Zeiträumen
- Erstellt separate Listen für Morgen- und Abendmessungen
- Generiert Liniendiagramme für alle Datensätze
- Erstellt Durchschnitts- und Standardabweichungsdiagramme
- Generiert einen umfassenden PDF-Bericht mit Tabellen und Diagrammen

## Verwendung

### 🩺 Neu: Automatischer Import von Withings (Empfohlen!)

```bash
# Direkt von Withings Blutdruckmessgerät abrufen
./run_analyzer.sh --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

**Setup erforderlich**: Siehe [WITHINGS_SETUP.md](WITHINGS_SETUP.md) für die detaillierte Anleitung zur Einrichtung der Withings API Integration.

### Traditionelle CSV-Analyse:

```bash
./run_analyzer.sh <CSV-Datei> [--start "YYYY-MM-DD HH:MM:SS"] [--end "YYYY-MM-DD HH:MM:SS"]
```

### Beispiele:

```bash
# 🩺 Withings API - Automatischer Import (empfohlen)
./run_analyzer.sh --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"

# CSV-Daten analysieren
./run_analyzer.sh bloodPressure.csv

# Mit der Beispieldatei
./run_analyzer.sh bloodpressure_example.csv

# Daten ab einem bestimmten Zeitpunkt
./run_analyzer.sh bloodPressure.csv --start "2025-09-25 00:00:00"

# Daten in einem bestimmten Zeitraum
./run_analyzer.sh bloodPressure.csv --start "2025-09-25 00:00:00" --end "2025-09-30 23:59:59"

# Kombiniert: CSV + Withings API
./run_analyzer.sh manual_data.csv --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

### Direkte Python-Ausführung:

```bash
# Mit Withings API
python3 blood_pressure_analyzer.py --withings --start "YYYY-MM-DD HH:MM:SS" --end "YYYY-MM-DD HH:MM:SS"

# Mit CSV-Datei
python3 blood_pressure_analyzer.py <CSV-Datei> [--start "YYYY-MM-DD HH:MM:SS"] [--end "YYYY-MM-DD HH:MM:SS"]
```

## Datenquellen

### 🩺 Withings API (Empfohlen)
**Automatischer Import** von Withings Blutdruckmessgeräten:
- **BPM Connect**: Bluetooth-fähiges Standardgerät
- **BPM Connect Pro**: Professionelle Medizin-Version  
- **BPM Core**: Mit zusätzlicher EKG-Funktion

**Vorteile**: Keine manuelle Dateneingabe, immer aktuelle Daten, höchste Genauigkeit

**Setup**: Siehe detaillierte Anleitung in [WITHINGS_SETUP.md](WITHINGS_SETUP.md)

### CSV-Format (Alternative)

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
- `bloodpressure_complete.svg`: Liniendiagramm aller Daten
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
- requests >= 2.25.0 (für Withings API)

## Setup

### Grundinstallation
Das Bash-Skript `run_analyzer.sh` führt automatisch folgende Schritte aus:

1. Erstellt ein Python Virtual Environment (falls nicht vorhanden)
2. Aktiviert das Virtual Environment
3. Installiert alle benötigten Pakete
4. Führt das Analyseprogramm aus

### 🩺 Withings API Setup (Optional)
Für den automatischen Datenimport von Withings Blutdruckmessgeräten:

```bash
# Interaktives Setup durchführen
python withings_client.py
```

**Detaillierte Anleitung**: Siehe [WITHINGS_SETUP.md](WITHINGS_SETUP.md) für:
- Withings Developer Account erstellen
- App-Konfiguration
- OAuth-Autorisierung
- Fehlerbehebung

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

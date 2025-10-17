# Blood Pressure Analyzer mit Withings API Integration

Ein professioneller Blutdruckdaten-Analyzer mit automatischer Withings API Integration für nahtlosen Datenimport.

## 🚀 Neue Funktionen

### ✨ Withings API Integration
- **Automatischer Datenimport** direkt von Withings Blutdruckmessgeräten
- **OAuth 2.0 Authentifizierung** für sichere API-Zugriffe
- **Token-Management** mit automatischer Erneuerung
- **Unterstützung für alle Withings Blutdruckmessgeräte**

### 📊 Erweiterte Datenquellen
- **CSV-Import**: Wie bisher für manuelle Daten
- **Withings API**: Live-Daten von verbundenen Geräten
- **Kombinierte Analyse**: Beide Quellen gleichzeitig nutzbar

## 🛠️ Installation und Setup

### 1. Repository klonen
```bash
git clone https://github.com/fermat2a/bloodpressure_analyzer.git
cd bloodpressure_analyzer
```

### 2. Abhängigkeiten installieren
```bash
# Automatisch über das Script
./run_analyzer.sh --help

# Oder manuell
pip install -r requirements.txt
```

### 3. Withings API Setup (optional)
```bash
# Interaktives Setup
python withings_client.py
```

Folgen Sie der detaillierten Anleitung in [WITHINGS_SETUP.md](WITHINGS_SETUP.md)

## 📱 Verwendung

### CSV-Analyse (wie bisher)
```bash
# Mit Bash Script
./run_analyzer.sh bloodpressure_example.csv --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"

# Direkt mit Python
python blood_pressure_analyzer.py bloodpressure_example.csv --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

### Withings API (neu!) 🎉
```bash
# Automatischer Import von Withings
./run_analyzer.sh --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"

# Ohne CSV-Datei - nur API-Daten
python blood_pressure_analyzer.py --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

### Kombinierte Analyse
```bash
# CSV + Withings API zusammen
./run_analyzer.sh manual_data.csv --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

## 🩺 Unterstützte Geräte

### Withings Blutdruckmessgeräte
- **BPM Connect**: Bluetooth-fähiges Standardgerät
- **BPM Connect Pro**: Professionelle Medizin-Version  
- **BPM Core**: Mit zusätzlicher EKG-Funktion

### Datenformat
- **Systolischer Blutdruck** (mmHg)
- **Diastolischer Blutdruck** (mmHg)
- **Herzfrequenz** (BPM)
- **Zeitstempel** (automatische Zeitzonenkonvertierung)

## 📋 Neue Kommandozeilen-Parameter

| Parameter | Beschreibung | Beispiel |
|-----------|--------------|----------|
| `--withings` | Verwende Withings API | `--withings` |
| `--start` | Startzeitpunkt (erforderlich für API) | `--start "2025-10-01 00:00:00"` |
| `--end` | Endzeitpunkt (erforderlich für API) | `--end "2025-10-17 23:59:59"` |
| `csv_file` | CSV-Datei (optional wenn `--withings`) | `bloodpressure.csv` |

## 🔒 Sicherheit

- **OAuth 2.0**: Sichere Authentifizierung ohne Passwort-Speicherung
- **Token-Verschlüsselung**: Automatische Erneuerung und sichere Speicherung
- **Lokaler Callback**: Alle sensiblen Daten bleiben auf Ihrem System
- **.gitignore**: API-Credentials werden nicht versioniert

## 📄 Ausgabe-Dateien

Das Programm erstellt unverändert:
- **bloodpressure.pdf**: Vollständiger Analysebericht
- **bloodpressure_complete.svg**: Komplettes Liniendiagramm
- **bloodpressure_average.svg**: Durchschnittsdiagramm  
- **bloodpressure_moning_evening.svg**: Morgen-Abend-Vergleich

## 🔧 Fehlerbehebung

### Withings Setup-Probleme
```bash
# Setup zurücksetzen
rm withings_config.json withings_credentials.json
python withings_client.py
```

### Dependencies fehlen
```bash
# Neuinstallation
rm -rf venv/
./run_analyzer.sh --help
```

### API-Verbindungsprobleme
```bash
# Verbindung testen
python withings_client.py
```

## 📚 Dokumentation

- **[WITHINGS_SETUP.md](WITHINGS_SETUP.md)**: Detaillierte Withings API Setup-Anleitung
- **[Withings Developer Portal](https://developer.withings.com)**: Offizielle API-Dokumentation
- **[API Status](https://status.withings.com/)**: Aktuelle Service-Verfügbarkeit

## 🔄 Migration von CSV zu API

### Schritt 1: Bestehende CSV-Analyse
```bash
# Wie gewohnt
./run_analyzer.sh bloodpressure.csv --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

### Schritt 2: Withings Setup
```bash
# Einmaliges Setup
python withings_client.py
```

### Schritt 3: API-basierte Analyse
```bash
# Automatischer Datenimport
./run_analyzer.sh --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

## 🏗️ Architektur

```
blood_pressure_analyzer.py     # Hauptanalysator (erweitert)
├── CSV-Import                 # Bestehende Funktionalität
├── Withings API Import        # Neue Funktionalität  
└── Unified Analysis           # Gemeinsame Verarbeitung

withings_client.py             # Withings API Client
├── OAuth 2.0 Flow            # Authentifizierung
├── Token Management          # Automatische Erneuerung
├── API Calls                 # Datenabfrage
└── Error Handling            # Robuste Fehlerbehandlung
```

## 📈 Vorteile der API-Integration

### Für Benutzer
- ✅ **Automatisierung**: Kein manueller CSV-Export mehr
- ✅ **Aktualität**: Immer die neuesten Daten
- ✅ **Genauigkeit**: Direkt vom Messgerät ohne Übertragungsfehler
- ✅ **Zeitersparnis**: Ein Befehl statt mehrerer Schritte

### Für Entwickler  
- ✅ **Saubere Architektur**: Getrennte Module für verschiedene Datenquellen
- ✅ **Erweiterbarkeit**: Einfache Integration weiterer APIs
- ✅ **Robustheit**: Umfassendes Error-Handling und Retry-Logic
- ✅ **Sicherheit**: OAuth 2.0 Best Practices

## 🚦 Roadmap

- [ ] **Apple Health Integration**: Import von iPhone Health-Daten
- [ ] **Google Fit Integration**: Android Health-Daten
- [ ] **Garmin Connect**: Smartwatch-Daten
- [ ] **Fitbit API**: Wearable-Integration
- [ ] **Web Dashboard**: Browser-basierte Analyse

## 🤝 Contributing

Beiträge sind willkommen! Besonders für:
- Weitere Health-API Integrationen
- UI/UX Verbesserungen  
- Neue Analyse-Features
- Dokumentations-Updates

## 📜 Lizenz

MIT License - Siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- **Withings**: Für die umfassende Health API
- **matplotlib**: Für die exzellenten Visualisierungen
- **pandas**: Für die Datenverarbeitung
- **requests**: Für HTTP-Client Funktionalität
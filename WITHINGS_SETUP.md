# Withings API Setup Anleitung

Diese Anleitung führt Sie durch das Setup der Withings API Integration für den Blood Pressure Analyzer.

## Voraussetzungen

1. **Withings Konto**: Sie benötigen ein aktives Withings-Konto mit Blutdruckmessgerät
2. **Withings Developer Account**: Registrierung auf https://developer.withings.com
3. **Python Dependencies**: `requests` library (wird automatisch installiert)

## Schritt 1: Withings Developer App erstellen

1. Gehen Sie zu [Withings Developer Portal](https://developer.withings.com)
2. Melden Sie sich mit Ihrem Withings-Konto an
3. Klicken Sie auf "Create an App" oder "Neue App erstellen"
4. Füllen Sie die App-Details aus:
   - **App Name**: `Blood Pressure Analyzer` (oder ein Name Ihrer Wahl)
   - **Description**: `Personal blood pressure data analysis`
   - **Redirect URI**: `http://localhost:8080/callback`
   - **Scopes**: Wählen Sie `user.metrics` (für Gesundheitsdaten)

5. Speichern Sie die App und notieren Sie sich:
   - **Client ID** (wird angezeigt)
   - **Client Secret** (wird angezeigt)

## Schritt 2: API Setup durchführen

### Automatisches Setup (Empfohlen)

```bash
# Führen Sie das Setup-Script aus
python withings_client.py
```

Das Script wird Sie durch folgende Schritte führen:
1. Eingabe der Client ID und Client Secret
2. Automatisches Öffnen der Autorisierungs-URL
3. Anmeldung bei Withings und Berechtigung erteilen
4. Eingabe der Callback-URL
5. Automatisches Speichern der Tokens

### Manuelles Setup

1. **Credentials speichern**:
   Erstellen Sie eine Datei `withings_credentials.json`:
   ```json
   {
     "client_id": "IHRE_CLIENT_ID",
     "client_secret": "IHR_CLIENT_SECRET",
     "redirect_uri": "http://localhost:8080/callback"
   }
   ```

2. **OAuth Autorisierung**:
   ```python
   from withings_client import WithingsClient
   
   # Client erstellen
   client = WithingsClient("CLIENT_ID", "CLIENT_SECRET")
   
   # Autorisierung durchführen
   client.authorize()
   ```

## Schritt 3: Blutdruckdaten abrufen

### Mit dem Blood Pressure Analyzer

```bash
# Withings API verwenden (anstatt CSV)
python blood_pressure_analyzer.py --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"

# Kombiniert mit CSV (falls gewünscht)
python blood_pressure_analyzer.py bloodpressure.csv --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

### Direkter API-Aufruf

```python
from withings_client import WithingsClient
from datetime import datetime, timedelta

# Client laden
client = WithingsClient("CLIENT_ID", "CLIENT_SECRET")

# Daten der letzten 30 Tage abrufen
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

data = client.get_blood_pressure_data(start_date, end_date)

for entry in data:
    print(f"{entry['timestamp']}: SYS={entry['sys']}, DIA={entry['dia']}, Pulse={entry['pulse']}")
```

## Verfügbare Parameter

### Neue Kommandozeilen-Optionen

- `--withings`: Verwende Withings API anstatt CSV-Datei
- `--start`: Startzeitpunkt (erforderlich für Withings API)
- `--end`: Endzeitpunkt (erforderlich für Withings API)

### Beispiele

```bash
# Nur Withings API
python blood_pressure_analyzer.py --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"

# Nur CSV (wie bisher)
python blood_pressure_analyzer.py bloodpressure.csv --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"

# Bash Script mit Withings
./run_analyzer.sh --withings --start "2025-10-01 00:00:00" --end "2025-10-17 23:59:59"
```

## Unterstützte Blutdruckmessgeräte

Die API unterstützt alle Withings Blutdruckmessgeräte:
- **BPM Connect**: Bluetooth-fähiges Blutdruckmessgerät
- **BPM Connect Pro**: Professionelle Version
- **BPM Core**: Mit EKG-Funktion

## Datenformat

Die Withings API liefert folgende Blutdruckdaten:
- **Systolischer Blutdruck** (mmHg)
- **Diastolischer Blutdruck** (mmHg)
- **Herzfrequenz** (BPM)
- **Zeitstempel** (UTC mit automatischer Konvertierung)

## Fehlerbehebung

### "Keine Autorisierung"
```bash
# Setup erneut durchführen
python withings_client.py
```

### "requests not found"
```bash
# Dependencies installieren
pip install -r requirements.txt
```

### "Keine Daten gefunden"
- Überprüfen Sie den Zeitraum (--start und --end)
- Stellen Sie sicher, dass Blutdruckmessungen in der Withings App vorhanden sind
- Prüfen Sie die API-Berechtigung in Ihrem Withings-Konto

### Token abgelaufen
Die Tokens werden automatisch erneuert. Bei Problemen:
```bash
# Tokens zurücksetzen
rm withings_config.json
python withings_client.py
```

## Sicherheitshinweise

- **Credentials**: Speichern Sie `withings_credentials.json` niemals in öffentlichen Repositories
- **Tokens**: Die OAuth-Tokens werden sicher in `withings_config.json` gespeichert
- **API-Limits**: Die API hat Rate-Limits - vermeiden Sie zu häufige Anfragen
- **Lokaler Redirect**: Der Callback läuft auf localhost:8080

## Integration mit bestehenden Workflows

### Bash Script erweitern

Die `run_analyzer.sh` kann erweitert werden:

```bash
#!/bin/bash
echo "=== Blood Pressure Analyzer Setup ==="

# Prüfe auf Withings Parameter
if [[ "$*" == *"--withings"* ]]; then
    echo "Verwende Withings API..."
    # Prüfe Withings Setup
    if [ ! -f "withings_credentials.json" ]; then
        echo "Withings Setup erforderlich..."
        python withings_client.py
    fi
fi

# Aktiviere Virtual Environment und führe Analyzer aus
# ... (bestehender Code)
```

## API-Dokumentation

Detaillierte API-Referenz: https://developer.withings.com/api-reference

Unterstützte Endpunkte:
- `measure/getmeas`: Abruf von Gesundheitsmessungen
- `oauth2`: Token-Management
- `user/getdevice`: Geräte-Information

## Support

Bei Problemen:
1. Überprüfen Sie die [Withings API Status](https://status.withings.com/)
2. Konsultieren Sie die [Developer Documentation](https://developer.withings.com/developer-guide/)
3. Testen Sie die Verbindung mit `python withings_client.py`
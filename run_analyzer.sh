#!/bin/bash

# Blood Pressure Analyzer Setup und Ausführung Script
# Erstellt ein Virtual Environment und führt das Python-Programm aus

set -e  # Exit bei Fehlern

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/blood_pressure_analyzer.py"

echo "=== Blood Pressure Analyzer Setup ==="

# Prüfe ob Python3 installiert ist
if ! command -v python3 &> /dev/null; then
    echo "Fehler: python3 ist nicht installiert!"
    exit 1
fi

# Erstelle Virtual Environment falls es nicht existiert
if [ ! -d "$VENV_DIR" ]; then
    echo "Erstelle Virtual Environment..."
    python3 -m venv "$VENV_DIR"
fi

# Aktiviere Virtual Environment
echo "Aktiviere Virtual Environment..."
source "$VENV_DIR/bin/activate"

# Installiere erforderliche Pakete
echo "Installiere Python-Pakete..."
pip install --upgrade pip > /dev/null 2>&1

# Installiere Pakete aus requirements.txt
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "Installiere Pakete aus requirements.txt..."
    pip install -r "$SCRIPT_DIR/requirements.txt" > /dev/null 2>&1
else
    # Fallback: Installiere Pakete einzeln
    PACKAGES=(
        "matplotlib>=3.5.0"
        "pandas>=1.3.0"
        "numpy>=1.21.0"
    )

    for package in "${PACKAGES[@]}"; do
        echo "Installiere $package..."
        pip install "$package" > /dev/null 2>&1
    done
fi

# Prüfe ob das Python-Skript existiert
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Fehler: Python-Skript nicht gefunden: $PYTHON_SCRIPT"
    exit 1
fi

echo "=== Starte Blood Pressure Analyzer ==="

# Führe das Python-Skript mit allen übergebenen Parametern aus
python "$PYTHON_SCRIPT" "$@"

echo "=== Analyse abgeschlossen ==="
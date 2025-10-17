#!/usr/bin/env python3
"""
Blutdruckdaten-Analyzer
Analysiert Blutdruckdaten aus CSV-Dateien und erstellt Visualisierungen.
"""

import argparse
import csv
from datetime import datetime, time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from pathlib import Path
from collections import defaultdict
import numpy as np


class BloodPressureAnalyzer:
    def __init__(self, csv_file, start_time=None, end_time=None):
        self.csv_file = csv_file
        self.start_time = start_time
        self.end_time = end_time
        self.bloodpressure_complete = []
        self.bloodpressure_morning = []
        self.bloodpressure_evening = []
        
    def load_data(self):
        """Lädt die Daten aus der CSV-Datei"""
        with open(self.csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = datetime.fromisoformat(row['Date'])
                sys_bp = int(row['SYS'])
                dia_bp = int(row['DIA'])
                pulse = int(row['BPM'])
                
                self.bloodpressure_complete.append({
                    'timestamp': timestamp,
                    'sys': sys_bp,
                    'dia': dia_bp,
                    'pulse': pulse
                })
    
    def sort_data(self):
        """Sortiert die Daten nach Zeitstempel"""
        self.bloodpressure_complete.sort(key=lambda x: x['timestamp'])
    
    def filter_by_time_range(self):
        """Filtert die Daten basierend auf Start- und Endzeitpunkt"""
        if self.start_time:
            self.bloodpressure_complete = [
                entry for entry in self.bloodpressure_complete 
                if entry['timestamp'] >= self.start_time
            ]
        
        if self.end_time:
            self.bloodpressure_complete = [
                entry for entry in self.bloodpressure_complete 
                if entry['timestamp'] <= self.end_time
            ]
    
    def create_morning_data(self):
        """Erstellt Liste mit ersten Blutdruckwerten des Tages (4:00-12:00)"""
        daily_data = defaultdict(list)
        
        # Gruppiere Daten nach Datum
        for entry in self.bloodpressure_complete:
            date = entry['timestamp'].date()
            daily_data[date].append(entry)
        
        # Finde ersten Wert des Tages zwischen 4:00 und 12:00
        for date, entries in daily_data.items():
            entries.sort(key=lambda x: x['timestamp'])
            for entry in entries:
                entry_time = entry['timestamp'].time()
                if time(4, 0) <= entry_time <= time(12, 0):
                    self.bloodpressure_morning.append(entry)
                    break
    
    def create_evening_data(self):
        """Erstellt Liste mit letzten Blutdruckwerten des Tages (nach 18:00)"""
        daily_data = defaultdict(list)
        
        # Gruppiere Daten nach Datum
        for entry in self.bloodpressure_complete:
            date = entry['timestamp'].date()
            daily_data[date].append(entry)
        
        # Finde letzten Wert des Tages nach 18:00
        for date, entries in daily_data.items():
            entries.sort(key=lambda x: x['timestamp'], reverse=True)
            for entry in entries:
                entry_time = entry['timestamp'].time()
                if entry_time >= time(18, 0):
                    self.bloodpressure_evening.append(entry)
                    break
    
    def create_line_chart(self, data, filename, title):
        """Erstellt ein Liniendiagramm für die Blutdruckdaten"""
        if not data:
            print(f"Keine Daten für {title}")
            return
            
        timestamps = [entry['timestamp'] for entry in data]
        sys_values = [entry['sys'] for entry in data]
        dia_values = [entry['dia'] for entry in data]
        pulse_values = [entry['pulse'] for entry in data]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Blutdruckdiagramm
        ax1.plot(timestamps, sys_values, 'r-', label='Systolisch', linewidth=2)
        ax1.plot(timestamps, dia_values, 'b-', label='Diastolisch', linewidth=2)
        ax1.set_ylabel('Blutdruck (mmHg)', fontsize=12)
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Pulsdiagramm
        ax2.plot(timestamps, pulse_values, 'g-', label='Puls', linewidth=2)
        ax2.set_ylabel('Puls (bpm)', fontsize=12)
        ax2.set_xlabel('Datum/Zeit', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig(filename, format='svg', bbox_inches='tight')
        plt.close()
    
    def create_average_chart(self):
        """Erstellt ein Diagramm mit Durchschnittswerten und Standardabweichungen"""
        datasets = [
            ('Komplett', self.bloodpressure_complete),
            ('Morgens', self.bloodpressure_morning),
            ('Abends', self.bloodpressure_evening)
        ]
        
        categories = []
        sys_means = []
        sys_stds = []
        dia_means = []
        dia_stds = []
        pulse_means = []
        pulse_stds = []
        
        for name, data in datasets:
            if data:
                categories.append(name)
                sys_values = [entry['sys'] for entry in data]
                dia_values = [entry['dia'] for entry in data]
                pulse_values = [entry['pulse'] for entry in data]
                
                sys_means.append(np.mean(sys_values))
                sys_stds.append(np.std(sys_values))
                dia_means.append(np.mean(dia_values))
                dia_stds.append(np.std(dia_values))
                pulse_means.append(np.mean(pulse_values))
                pulse_stds.append(np.std(pulse_values))
        
        x = np.arange(len(categories))
        width = 0.25
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        bars1 = ax.bar(x - width, sys_means, width, yerr=sys_stds, 
                      label='Systolisch', color='red', alpha=0.7, capsize=5)
        bars2 = ax.bar(x, dia_means, width, yerr=dia_stds, 
                      label='Diastolisch', color='blue', alpha=0.7, capsize=5)
        bars3 = ax.bar(x + width, pulse_means, width, yerr=pulse_stds, 
                      label='Puls', color='green', alpha=0.7, capsize=5)
        
        ax.set_xlabel('Kategorie', fontsize=12)
        ax.set_ylabel('Werte', fontsize=12)
        ax.set_title('Durchschnittliche Blutdruckwerte mit Standardabweichung', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('bloodpressure_average.svg', format='svg', bbox_inches='tight')
        plt.close()
    
    def create_morning_evening_chart(self):
        """Erstellt ein kombiniertes Diagramm für Morgen- und Abenddaten"""
        if not self.bloodpressure_morning and not self.bloodpressure_evening:
            print("Keine Morgen- oder Abenddaten vorhanden")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Morgen- und Abenddaten kombinieren für bessere Darstellung
        if self.bloodpressure_morning:
            morning_timestamps = [entry['timestamp'] for entry in self.bloodpressure_morning]
            morning_sys = [entry['sys'] for entry in self.bloodpressure_morning]
            morning_dia = [entry['dia'] for entry in self.bloodpressure_morning]
            morning_pulse = [entry['pulse'] for entry in self.bloodpressure_morning]
            
            # Blutdruckdiagramm - Morgenwerte
            ax1.plot(morning_timestamps, morning_sys, 'r-', marker='o', label='Systolisch (Morgens)', 
                    linewidth=2, markersize=6, alpha=0.8)
            ax1.plot(morning_timestamps, morning_dia, 'b-', marker='o', label='Diastolisch (Morgens)', 
                    linewidth=2, markersize=6, alpha=0.8)
            
            # Pulsdiagramm - Morgenwerte
            ax2.plot(morning_timestamps, morning_pulse, 'g-', marker='o', label='Puls (Morgens)', 
                    linewidth=2, markersize=6, alpha=0.8)
        
        if self.bloodpressure_evening:
            evening_timestamps = [entry['timestamp'] for entry in self.bloodpressure_evening]
            evening_sys = [entry['sys'] for entry in self.bloodpressure_evening]
            evening_dia = [entry['dia'] for entry in self.bloodpressure_evening]
            evening_pulse = [entry['pulse'] for entry in self.bloodpressure_evening]
            
            # Blutdruckdiagramm - Abendwerte
            ax1.plot(evening_timestamps, evening_sys, 'r--', marker='s', label='Systolisch (Abends)', 
                    linewidth=2, markersize=6, alpha=0.8)
            ax1.plot(evening_timestamps, evening_dia, 'b--', marker='s', label='Diastolisch (Abends)', 
                    linewidth=2, markersize=6, alpha=0.8)
            
            # Pulsdiagramm - Abendwerte
            ax2.plot(evening_timestamps, evening_pulse, 'g--', marker='s', label='Puls (Abends)', 
                    linewidth=2, markersize=6, alpha=0.8)
        
        # Blutdruckdiagramm formatieren
        ax1.set_ylabel('Blutdruck (mmHg)', fontsize=12)
        ax1.set_title('Morgen- und Abendblutdruckwerte im Vergleich', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Pulsdiagramm formatieren
        ax2.set_ylabel('Puls (bpm)', fontsize=12)
        ax2.set_xlabel('Datum', fontsize=12)
        ax2.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.savefig('bloodpressure_moning_evening.svg', format='svg', bbox_inches='tight')
        plt.close()
    
    def create_pdf_report(self):
        """Erstellt den PDF-Bericht"""
        with PdfPages('bloodpressure.pdf') as pdf:
            # Startseite
            self.create_title_page(pdf)
            
            # Diagramme direkt erstellen (DIN A4 Querformat für alle)
            self._create_chart_for_pdf(pdf, self.bloodpressure_complete, 'Alle Blutdruckdaten')
            
            # Morgen-Abend-Vergleichsdiagramm
            self._create_morning_evening_chart_for_pdf(pdf)
            
            # Durchschnittsdiagramm
            self._create_average_chart_for_pdf(pdf)
            
            # Tabelle
            self.add_data_table_to_pdf(pdf)
    
    def create_title_page(self, pdf):
        """Erstellt die Titelseite"""
        fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 Querformat
        ax.axis('off')
        
        # Titel
        ax.text(0.5, 0.7, 'Blutdruckdaten Sascha Effert', 
               horizontalalignment='center', verticalalignment='center',
               fontsize=24, fontweight='bold', transform=ax.transAxes)
        
        # Zeitraum
        if self.start_time:
            start_str = self.start_time.strftime('%d.%m.%Y %H:%M')
        else:
            start_str = self.bloodpressure_complete[0]['timestamp'].strftime('%d.%m.%Y %H:%M')
        
        if self.end_time:
            end_str = self.end_time.strftime('%d.%m.%Y %H:%M')
        else:
            end_str = self.bloodpressure_complete[-1]['timestamp'].strftime('%d.%m.%Y %H:%M')
        
        ax.text(0.5, 0.4, f'Zeitraum: {start_str} - {end_str}', 
               horizontalalignment='center', verticalalignment='center',
               fontsize=16, transform=ax.transAxes)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def _create_chart_for_pdf(self, pdf, data, title):
        """Erstellt ein Liniendiagramm direkt für PDF"""
        if not data:
            fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 Querformat
            ax.text(0.5, 0.5, f'Keine Daten für {title}', 
                   horizontalalignment='center', verticalalignment='center',
                   fontsize=16, transform=ax.transAxes)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            return
            
        timestamps = [entry['timestamp'] for entry in data]
        sys_values = [entry['sys'] for entry in data]
        dia_values = [entry['dia'] for entry in data]
        pulse_values = [entry['pulse'] for entry in data]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.69, 8.27))  # A4 Querformat
        
        # Blutdruckdiagramm
        ax1.plot(timestamps, sys_values, 'r-', label='Systolisch', linewidth=2)
        ax1.plot(timestamps, dia_values, 'b-', label='Diastolisch', linewidth=2)
        ax1.set_ylabel('Blutdruck (mmHg)', fontsize=12)
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Pulsdiagramm
        ax2.plot(timestamps, pulse_values, 'g-', label='Puls', linewidth=2)
        ax2.set_ylabel('Puls (bpm)', fontsize=12)
        ax2.set_xlabel('Datum/Zeit', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def _create_average_chart_for_pdf(self, pdf):
        """Erstellt das Durchschnittsdiagramm direkt für PDF"""
        datasets = [
            ('Komplett', self.bloodpressure_complete),
            ('Morgens', self.bloodpressure_morning),
            ('Abends', self.bloodpressure_evening)
        ]
        
        categories = []
        sys_means = []
        sys_stds = []
        dia_means = []
        dia_stds = []
        pulse_means = []
        pulse_stds = []
        
        for name, data in datasets:
            if data:
                categories.append(name)
                sys_values = [entry['sys'] for entry in data]
                dia_values = [entry['dia'] for entry in data]
                pulse_values = [entry['pulse'] for entry in data]
                
                sys_means.append(np.mean(sys_values))
                sys_stds.append(np.std(sys_values))
                dia_means.append(np.mean(dia_values))
                dia_stds.append(np.std(dia_values))
                pulse_means.append(np.mean(pulse_values))
                pulse_stds.append(np.std(pulse_values))
        
        x = np.arange(len(categories))
        width = 0.25
        
        fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 Querformat
        
        bars1 = ax.bar(x - width, sys_means, width, yerr=sys_stds, 
                      label='Systolisch', color='red', alpha=0.7, capsize=5)
        bars2 = ax.bar(x, dia_means, width, yerr=dia_stds, 
                      label='Diastolisch', color='blue', alpha=0.7, capsize=5)
        bars3 = ax.bar(x + width, pulse_means, width, yerr=pulse_stds, 
                      label='Puls', color='green', alpha=0.7, capsize=5)
        
        ax.set_xlabel('Kategorie', fontsize=12)
        ax.set_ylabel('Werte', fontsize=12)
        ax.set_title('Durchschnittliche Blutdruckwerte mit Standardabweichung', 
                    fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def _create_morning_evening_chart_for_pdf(self, pdf):
        """Erstellt das Morgen-Abend-Kombinationsdiagramm direkt für PDF"""
        if not self.bloodpressure_morning and not self.bloodpressure_evening:
            fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 Querformat
            ax.text(0.5, 0.5, 'Keine Morgen- oder Abenddaten vorhanden', 
                   horizontalalignment='center', verticalalignment='center',
                   fontsize=16, transform=ax.transAxes)
            ax.axis('off')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.69, 8.27))  # A4 Querformat
        
        # Morgen- und Abenddaten kombinieren für bessere Darstellung
        if self.bloodpressure_morning:
            morning_timestamps = [entry['timestamp'] for entry in self.bloodpressure_morning]
            morning_sys = [entry['sys'] for entry in self.bloodpressure_morning]
            morning_dia = [entry['dia'] for entry in self.bloodpressure_morning]
            morning_pulse = [entry['pulse'] for entry in self.bloodpressure_morning]
            
            # Blutdruckdiagramm - Morgenwerte
            ax1.plot(morning_timestamps, morning_sys, 'r-', marker='o', label='Systolisch (Morgens)', 
                    linewidth=2, markersize=6, alpha=0.8)
            ax1.plot(morning_timestamps, morning_dia, 'b-', marker='o', label='Diastolisch (Morgens)', 
                    linewidth=2, markersize=6, alpha=0.8)
            
            # Pulsdiagramm - Morgenwerte
            ax2.plot(morning_timestamps, morning_pulse, 'g-', marker='o', label='Puls (Morgens)', 
                    linewidth=2, markersize=6, alpha=0.8)
        
        if self.bloodpressure_evening:
            evening_timestamps = [entry['timestamp'] for entry in self.bloodpressure_evening]
            evening_sys = [entry['sys'] for entry in self.bloodpressure_evening]
            evening_dia = [entry['dia'] for entry in self.bloodpressure_evening]
            evening_pulse = [entry['pulse'] for entry in self.bloodpressure_evening]
            
            # Blutdruckdiagramm - Abendwerte
            ax1.plot(evening_timestamps, evening_sys, 'r--', marker='s', label='Systolisch (Abends)', 
                    linewidth=2, markersize=6, alpha=0.8)
            ax1.plot(evening_timestamps, evening_dia, 'b--', marker='s', label='Diastolisch (Abends)', 
                    linewidth=2, markersize=6, alpha=0.8)
            
            # Pulsdiagramm - Abendwerte
            ax2.plot(evening_timestamps, evening_pulse, 'g--', marker='s', label='Puls (Abends)', 
                    linewidth=2, markersize=6, alpha=0.8)
        
        # Blutdruckdiagramm formatieren
        ax1.set_ylabel('Blutdruck (mmHg)', fontsize=12)
        ax1.set_title('Morgen- und Abendblutdruckwerte im Vergleich', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Pulsdiagramm formatieren
        ax2.set_ylabel('Puls (bpm)', fontsize=12)
        ax2.set_xlabel('Datum', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        ax2.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
    
    def add_data_table_to_pdf(self, pdf):
        """Fügt die Datentabelle zur PDF hinzu"""
        # Erstelle DataFrame für bessere Tabellendarstellung
        df_data = []
        for entry in self.bloodpressure_complete:
            df_data.append({
                'Zeitstempel': entry['timestamp'].strftime('%d.%m.%Y %H:%M:%S'),
                'SYS': entry['sys'],
                'DIA': entry['dia'],
                'Puls': entry['pulse']
            })
        
        # Bestimme Farbmarkierungen
        morning_timestamps = {entry['timestamp'] for entry in self.bloodpressure_morning}
        evening_timestamps = {entry['timestamp'] for entry in self.bloodpressure_evening}
        
        # Erstelle Tabellen-Seiten (max 30 Einträge pro Seite)
        rows_per_page = 30
        for i in range(0, len(df_data), rows_per_page):
            fig, ax = plt.subplots(figsize=(11.69, 8.27))  # A4 Querformat
            ax.axis('off')
            
            # Aktuelle Seitendaten
            page_data = df_data[i:i+rows_per_page]
            
            # Tabelle erstellen
            table_data = [['Zeitstempel', 'SYS', 'DIA', 'Puls']]
            table_data.extend([[row['Zeitstempel'], row['SYS'], row['DIA'], row['Puls']] 
                              for row in page_data])
            
            table = ax.table(cellText=table_data, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1.2, 1.5)
            
            # Farbmarkierungen (vereinfacht)
            for j, entry in enumerate(self.bloodpressure_complete[i:i+rows_per_page], 1):
                if entry['timestamp'] in morning_timestamps:
                    for k in range(4):
                        table[(j, k)].set_facecolor('#FFFF99')  # Helles Gelb
                elif entry['timestamp'] in evening_timestamps:
                    for k in range(4):
                        table[(j, k)].set_facecolor('#FFB366')  # Helles Orange
            
            # Legende (nur auf erster Seite)
            if i == 0:
                ax.text(0.1, 0.05, 'Legende: Gelb = Morgenwerte, Orange = Abendwerte', 
                       transform=ax.transAxes, fontsize=10)
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
    
    def run_analysis(self):
        """Führt die komplette Analyse durch"""
        print("Lade Daten...")
        self.load_data()
        
        print("Sortiere Daten...")
        self.sort_data()
        
        print("Filtere nach Zeitraum...")
        self.filter_by_time_range()
        
        print("Erstelle Morgendaten...")
        self.create_morning_data()
        
        print("Erstelle Abenddaten...")
        self.create_evening_data()
        
        print("Erstelle Liniendiagramme...")
        self.create_line_chart(self.bloodpressure_complete, 
                             'bloddpressure_complee.svg', 
                             'Alle Blutdruckdaten')
        self.create_line_chart(self.bloodpressure_morning, 
                             'bloodpressure_morning.svg', 
                             'Morgendliche Blutdruckdaten')
        self.create_line_chart(self.bloodpressure_evening, 
                             'bloodpressure_evening.svg', 
                             'Abendliche Blutdruckdaten')
        
        print("Erstelle Durchschnittsdiagramm...")
        self.create_average_chart()
        
        print("Erstelle Morgen-Abend-Kombinationsdiagramm...")
        self.create_morning_evening_chart()
        
        print("Erstelle PDF-Bericht...")
        self.create_pdf_report()
        
        print("Analyse abgeschlossen!")
        print(f"Gefundene Datenpunkte: {len(self.bloodpressure_complete)}")
        print(f"Morgendliche Messungen: {len(self.bloodpressure_morning)}")
        print(f"Abendliche Messungen: {len(self.bloodpressure_evening)}")


def main():
    parser = argparse.ArgumentParser(description='Blutdruckdaten-Analyzer')
    parser.add_argument('csv_file', help='Pfad zur CSV-Datei mit Blutdruckdaten')
    parser.add_argument('--start', type=str, help='Startzeitpunkt (YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--end', type=str, help='Endzeitpunkt (YYYY-MM-DD HH:MM:SS)')
    
    args = parser.parse_args()
    
    # Parse Zeitstempel
    start_time = None
    end_time = None
    
    if args.start:
        try:
            start_time = datetime.fromisoformat(args.start.replace(' ', 'T'))
            # Wenn keine Zeitzone angegeben, verwende lokale Zeitzone
            if start_time.tzinfo is None:
                from datetime import timezone, timedelta
                start_time = start_time.replace(tzinfo=timezone(timedelta(hours=2)))  # CEST
        except ValueError:
            print(f"Fehler beim Parsen des Startzeitpunkts: {args.start}")
            return
    
    if args.end:
        try:
            end_time = datetime.fromisoformat(args.end.replace(' ', 'T'))
            # Wenn keine Zeitzone angegeben, verwende lokale Zeitzone
            if end_time.tzinfo is None:
                from datetime import timezone, timedelta
                end_time = end_time.replace(tzinfo=timezone(timedelta(hours=2)))  # CEST
        except ValueError:
            print(f"Fehler beim Parsen des Endzeitpunkts: {args.end}")
            return
    
    # Prüfe ob CSV-Datei existiert
    if not Path(args.csv_file).exists():
        print(f"CSV-Datei nicht gefunden: {args.csv_file}")
        return
    
    # Starte Analyse
    analyzer = BloodPressureAnalyzer(args.csv_file, start_time, end_time)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()

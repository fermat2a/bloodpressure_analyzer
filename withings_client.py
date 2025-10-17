#!/usr/bin/env python3
"""
Withings API Client
Integriert Withings Health API für automatischen Blutdruckdaten-Import
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode, urlparse, parse_qs
import webbrowser
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import requests
except ImportError:
    print("requests library nicht gefunden. Installiere mit: pip install requests")
    exit(1)


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler für OAuth Callback"""
    
    def do_GET(self):
        """Behandelt GET Requests vom OAuth Callback"""
        # Parse URL und extrahiere Authorization Code
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if 'code' in query_params:
            # Erfolgreich - Authorization Code erhalten
            self.server.auth_code = query_params['code'][0]
            self.server.auth_state = query_params.get('state', [''])[0]
            
            # Sende Erfolgs-Response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Withings Autorisierung erfolgreich</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                    .success { color: green; font-size: 24px; }
                    .info { color: #666; margin-top: 20px; }
                </style>
            </head>
            <body>
                <div class="success">✅ Autorisierung erfolgreich!</div>
                <div class="info">Du kannst dieses Fenster jetzt schließen und zum Terminal zurückkehren.</div>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())
            
        elif 'error' in query_params:
            # Fehler - Benutzer hat Zugriff verweigert
            error = query_params.get('error', ['unknown'])[0]
            error_description = query_params.get('error_description', [''])[0]
            
            self.server.auth_error = f"{error}: {error_description}"
            
            # Sende Fehler-Response
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Withings Autorisierung fehlgeschlagen</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                    .error {{ color: red; font-size: 24px; }}
                    .info {{ color: #666; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="error">❌ Autorisierung fehlgeschlagen</div>
                <div class="info">Fehler: {error}<br>{error_description}</div>
                <div class="info">Du kannst dieses Fenster schließen und es erneut versuchen.</div>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())
        
        # Starte Shutdown-Timer
        threading.Timer(1.0, self.server.shutdown).start()
    
    def log_message(self, format, *args):
        """Unterdrücke Server-Log-Nachrichten"""
        pass


class OAuthCallbackServer(HTTPServer):
    """HTTP Server für OAuth Callback mit zusätzlichen Attributen"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_code = None
        self.auth_state = None
        self.auth_error = None


class WithingsClient:
    """Client für Withings Health API"""
    
    # Withings API URLs
    AUTH_URL = "https://account.withings.com/oauth2_user/authorize2"
    TOKEN_URL = "https://wbsapi.withings.net/v2/oauth2"
    API_BASE_URL = "https://wbsapi.withings.net"
    
    # Measure types für Blutdruckdaten
    MEASURE_TYPES = {
        'diastolic': 9,      # Diastolischer Blutdruck
        'systolic': 10,      # Systolischer Blutdruck  
        'heart_rate': 11     # Herzfrequenz
    }
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = "http://localhost:8080/callback"):
        """
        Initialisiert den Withings Client
        
        Args:
            client_id: Withings App Client ID
            client_secret: Withings App Client Secret
            redirect_uri: OAuth Redirect URI
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None
        self.config_file = Path("withings_config.json")
        
        # Lade gespeicherte Tokens
        self._load_tokens()
    
    def _load_tokens(self):
        """Lädt gespeicherte OAuth Tokens"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.access_token = data.get('access_token')
                    self.refresh_token = data.get('refresh_token')
                    self.token_expires_at = data.get('expires_at')
                    print("OAuth Tokens geladen")
            except Exception as e:
                print(f"Fehler beim Laden der Tokens: {e}")
    
    def _save_tokens(self):
        """Speichert OAuth Tokens"""
        data = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.token_expires_at
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
            print("OAuth Tokens gespeichert")
        except Exception as e:
            print(f"Fehler beim Speichern der Tokens: {e}")
    
    def get_authorization_url(self, scope: str = "user.metrics,user.info") -> str:
        """
        Erstellt die OAuth Authorization URL
        
        Args:
            scope: API Scope (z.B. "user.metrics")
            
        Returns:
            Authorization URL
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': scope,
            'state': 'blood_pressure_analyzer'  # CSRF protection
        }
        
        url = f"{self.AUTH_URL}?{urlencode(params)}"
        print(f"Authorization URL: {url}")
        return url
    
    def authorize(self, scope: str = "user.metrics,user.info") -> bool:
        """
        Führt den kompletten OAuth Flow durch mit lokalem Callback-Server
        
        Args:
            scope: API Scope
            
        Returns:
            True wenn erfolgreich autorisiert
        """
        # Extrahiere Port aus redirect_uri
        parsed_uri = urlparse(self.redirect_uri)
        callback_port = parsed_uri.port or 8080
        
        # Generiere Authorization URL
        auth_url = self.get_authorization_url(scope)
        
        print("\\n=== Withings OAuth Autorisierung ===")
        print("1. Dein Browser wird automatisch geöffnet")
        print("2. Melde dich bei Withings an und erlaube den Zugriff")
        print("3. Du wirst automatisch hierher zurückgeleitet\\n")
        
        # Starte lokalen Callback-Server
        print(f"Starte lokalen Callback-Server auf Port {callback_port}...")
        
        try:
            server = OAuthCallbackServer(('localhost', callback_port), OAuthCallbackHandler)
            
            # Starte Server in eigenem Thread
            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            print(f"✅ Callback-Server läuft auf http://localhost:{callback_port}")
            
            # Öffne Browser
            try:
                webbrowser.open(auth_url)
                print("🌐 Browser wird geöffnet...")
            except Exception as e:
                print(f"⚠️  Browser konnte nicht automatisch geöffnet werden: {e}")
                print(f"Öffne manuell: {auth_url}")
            
            # Warte auf Callback (max 5 Minuten)
            print("⏳ Warte auf Autorisierung...")
            timeout = 300  # 5 Minuten
            start_time = time.time()
            
            while (time.time() - start_time) < timeout:
                if server.auth_code:
                    print("✅ Authorization Code erhalten!")
                    auth_code = server.auth_code
                    server.shutdown()
                    server_thread.join(timeout=5)
                    
                    # Tausche Code gegen Token
                    return self._exchange_code_for_token(auth_code)
                
                elif server.auth_error:
                    print(f"❌ Autorisierung fehlgeschlagen: {server.auth_error}")
                    server.shutdown()
                    server_thread.join(timeout=5)
                    return False
                
                time.sleep(0.5)
            
            # Timeout erreicht
            print("⏰ Timeout erreicht. Autorisierung abgebrochen.")
            server.shutdown()
            server_thread.join(timeout=5)
            return False
            
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"❌ Port {callback_port} ist bereits belegt!")
                print("Versuche einen anderen Port oder beende andere Anwendungen.")
                print("\\nAlternativ: Manueller OAuth-Flow")
                return self._manual_oauth_flow(auth_url)
            else:
                print(f"❌ Fehler beim Starten des Callback-Servers: {e}")
                return self._manual_oauth_flow(auth_url)
        
        except Exception as e:
            print(f"❌ Unerwarteter Fehler beim OAuth-Flow: {e}")
            return self._manual_oauth_flow(auth_url)
    
    def _manual_oauth_flow(self, auth_url: str) -> bool:
        """
        Fallback: Manueller OAuth-Flow falls automatischer Server nicht funktioniert
        
        Args:
            auth_url: Authorization URL
            
        Returns:
            True wenn erfolgreich
        """
        print("\\n🔄 Wechsle zu manuellem OAuth-Flow...")
        print("1. Öffne die folgende URL in deinem Browser:")
        print(f"   {auth_url}")
        print("2. Melde dich bei Withings an und erlaube den Zugriff")
        print("3. Kopiere die vollständige Callback-URL hierher")
        print("   (Die URL beginnt mit 'http://localhost:8080/callback?code=...')\\n")
        
        # Warte auf manuelle Eingabe der Callback URL
        while True:
            try:
                callback_url = input("Callback URL: ").strip()
                
                if not callback_url:
                    print("❌ Keine URL eingegeben. Versuche es erneut.")
                    continue
                
                # Extrahiere Authorization Code
                parsed_url = urlparse(callback_url)
                query_params = parse_qs(parsed_url.query)
                
                if 'code' not in query_params:
                    print("❌ Kein Authorization Code in der URL gefunden.")
                    print("Stelle sicher, dass du die vollständige Callback-URL kopiert hast.")
                    continue
                
                auth_code = query_params['code'][0]
                print("✅ Authorization Code extrahiert!")
                
                # Tausche Code gegen Token
                return self._exchange_code_for_token(auth_code)
                
            except KeyboardInterrupt:
                print("\\n❌ Autorisierung abgebrochen.")
                return False
            except Exception as e:
                print(f"❌ Fehler beim Verarbeiten der URL: {e}")
                print("Versuche es erneut...")
                continue
    
    def _exchange_code_for_token(self, auth_code: str) -> bool:
        """
        Tauscht Authorization Code gegen Access Token
        
        Args:
            auth_code: OAuth Authorization Code
            
        Returns:
            True wenn erfolgreich
        """
        # Withings API erwartet Parameter als Form-Data
        data = {
            'action': 'requesttoken',
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }
        
        print(f"🔄 Tausche Authorization Code gegen Access Token...")
        
        try:
            response = requests.post(self.TOKEN_URL, data=data)
            
            print(f"📡 API Response Status: {response.status_code}")
            print(f"📡 API Response Content: {response.text[:200]}...")
            
            response.raise_for_status()
            token_data = response.json()
            
            if token_data.get('status') == 0:  # Withings success status
                body = token_data.get('body', {})
                self.access_token = body.get('access_token')
                self.refresh_token = body.get('refresh_token')
                expires_in = body.get('expires_in', 3600)
                self.token_expires_at = time.time() + expires_in
                
                if self.access_token:
                    self._save_tokens()
                    print("✅ OAuth Token erfolgreich erhalten!")
                    return True
                else:
                    print("❌ Kein Access Token in der Antwort erhalten")
                    return False
            else:
                error_msg = token_data.get('error', 'Unbekannter Fehler')
                print(f"❌ Withings API Fehler: {error_msg}")
                print(f"📄 Vollständige Antwort: {token_data}")
                return False
                
        except requests.RequestException as e:
            print(f"🌐 HTTP Fehler beim Token-Austausch: {e}")
            return False
        except ValueError as e:
            print(f"📄 JSON Parse Fehler: {e}")
            print(f"📄 Response Content: {response.text}")
            return False
        except Exception as e:
            print(f"❌ Allgemeiner Fehler beim Token-Austausch: {e}")
            return False
    
    def _refresh_access_token(self) -> bool:
        """
        Erneuert den Access Token mit dem Refresh Token
        
        Returns:
            True wenn erfolgreich
        """
        if not self.refresh_token:
            print("Kein Refresh Token verfügbar")
            return False
        
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        
        try:
            response = requests.post(self.TOKEN_URL, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            
            if token_data.get('status') == 0:
                body = token_data.get('body', {})
                self.access_token = body.get('access_token')
                self.refresh_token = body.get('refresh_token', self.refresh_token)
                expires_in = body.get('expires_in', 3600)
                self.token_expires_at = time.time() + expires_in
                
                self._save_tokens()
                print("Access Token erfolgreich erneuert!")
                return True
            else:
                print(f"Fehler beim Token-Refresh: {token_data.get('error')}")
                return False
                
        except Exception as e:
            print(f"Fehler beim Token-Refresh: {e}")
            return False
    
    def _ensure_valid_token(self) -> bool:
        """
        Stellt sicher, dass ein gültiger Access Token vorhanden ist
        
        Returns:
            True wenn gültiger Token verfügbar
        """
        if not self.access_token:
            print("Kein Access Token vorhanden. Autorisierung erforderlich.")
            return False
        
        # Prüfe ob Token abgelaufen ist (mit 5 Min Puffer)
        if self.token_expires_at and time.time() >= (self.token_expires_at - 300):
            print("Access Token ist abgelaufen. Erneuere...")
            return self._refresh_access_token()
        
        return True
    
    def get_blood_pressure_data(self, 
                               start_date: datetime, 
                               end_date: datetime) -> List[Dict]:
        """
        Ruft Blutdruckdaten von Withings API ab
        
        Args:
            start_date: Startdatum
            end_date: Enddatum
            
        Returns:
            Liste mit Blutdruckdaten
        """
        if not self._ensure_valid_token():
            print("Keine gültige Autorisierung. Führe zuerst authorize() aus.")
            return []
        
        # Konvertiere Datumsangaben zu Unix Timestamps
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        
        print(f"🔍 Suche Blutdruckdaten von {start_date.strftime('%Y-%m-%d')} bis {end_date.strftime('%Y-%m-%d')}")
        
        # API Request Parameter für Withings v2 API
        data = {
            'action': 'getmeas',
            'startdate': start_timestamp,
            'enddate': end_timestamp,
            'meastypes': ','.join(map(str, self.MEASURE_TYPES.values())),  # 9,10,11
            'category': 1,  # Real measurements (nicht geschätzt)
        }
        
        # Authorization Header verwenden anstatt oauth_token Parameter
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Debug-Ausgabe
        print(f"📡 API Request URL: {self.API_BASE_URL}/measure")
        print(f"📡 API Request Data: {data}")
        print(f"📡 API Request Headers: Authorization: Bearer {self.access_token[:20]}...")
        
        try:
            # POST Request anstatt GET für Withings v2 API
            response = requests.post(f"{self.API_BASE_URL}/measure", data=data, headers=headers)
            
            print(f"📡 API Response Status: {response.status_code}")
            print(f"📡 API Response Content: {response.text[:300]}...")
            
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 0:
                measurements = data.get('body', {}).get('measuregrps', [])
                print(f"✅ {len(measurements)} Messgrupppen gefunden")
                processed_data = self._process_blood_pressure_data(measurements)
                
                if not processed_data:
                    print("⚠️  Keine Blutdruckmessungen in den gefundenen Daten")
                    print("💡 Überprüfe:")
                    print("   - Sind Blutdruckmessungen im angegebenen Zeitraum vorhanden?")
                    print("   - Sind die Messungen mit einem Withings Blutdruckmessgerät gemacht?")
                    print("   - Sind die Daten in der Withings Health Mate App sichtbar?")
                
                return processed_data
            else:
                error_msg = data.get('error', 'Unbekannter Fehler')
                print(f"❌ Withings API Fehler: {error_msg}")
                print(f"📄 Status Code: {data.get('status')}")
                
                # Spezifische Fehlermeldungen
                if 'Invalid Params' in error_msg:
                    print("💡 Mögliche Ursachen:")
                    print("   - OAuth Token ungültig oder abgelaufen")
                    print("   - Zeitstempel-Format inkorrekt")
                    print("   - Fehlende API-Berechtigung")
                
                return []
                
        except requests.RequestException as e:
            print(f"🌐 HTTP Fehler beim Datenabruf: {e}")
            return []
        except ValueError as e:
            print(f"📄 JSON Parse Fehler: {e}")
            print(f"📄 Response Content: {response.text}")
            return []
        except Exception as e:
            print(f"❌ Allgemeiner Fehler beim Datenabruf: {e}")
            return []
    
    def _process_blood_pressure_data(self, measurements: List[Dict]) -> List[Dict]:
        """
        Verarbeitet rohe Withings Messdaten zu strukturierten Blutdruckdaten
        
        Args:
            measurements: Rohe Withings API Daten
            
        Returns:
            Strukturierte Blutdruckdaten
        """
        processed_data = []
        
        for group in measurements:
            timestamp = datetime.fromtimestamp(group['date'], tz=timezone.utc)
            measures = {m['type']: m['value'] * (10 ** m['unit']) for m in group['measures']}
            
            # Suche nach Blutdruckdaten in dieser Messung
            systolic = measures.get(self.MEASURE_TYPES['systolic'])
            diastolic = measures.get(self.MEASURE_TYPES['diastolic'])
            heart_rate = measures.get(self.MEASURE_TYPES['heart_rate'])
            
            # Nur hinzufügen wenn Blutdruckdaten vorhanden
            if systolic is not None and diastolic is not None:
                entry = {
                    'timestamp': timestamp,
                    'sys': int(systolic),
                    'dia': int(diastolic),
                    'pulse': int(heart_rate) if heart_rate is not None else 0
                }
                processed_data.append(entry)
        
        # Sortiere nach Zeitstempel
        processed_data.sort(key=lambda x: x['timestamp'])
        
        print(f"{len(processed_data)} Blutdruckmessungen von Withings API abgerufen")
        return processed_data
    
    def test_connection(self) -> bool:
        """
        Testet die Verbindung zur Withings API
        
        Returns:
            True wenn Verbindung erfolgreich
        """
        if not self._ensure_valid_token():
            return False
        
        # Teste mit einem einfachen API Call - verwende user endpoint
        data = {
            'action': 'getdevice'
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        print("🔗 Teste Withings API Verbindung...")
        
        try:
            response = requests.post(f"{self.API_BASE_URL}/v2/user", data=data, headers=headers)
            
            print(f"📡 Test Response Status: {response.status_code}")
            print(f"📡 Test Response Content: {response.text[:200]}...")
            
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 0:
                print("✅ Withings API Verbindung erfolgreich!")
                devices = data.get('body', {}).get('devices', [])
                if devices:
                    print(f"📱 {len(devices)} Gerät(e) gefunden:")
                    for device in devices:
                        device_type = device.get('type', 'Unbekannt')
                        model = device.get('model', 'Unbekannt')
                        print(f"   - {device_type}: {model}")
                return True
            else:
                error_msg = data.get('error', 'Unbekannter Fehler')
                print(f"❌ API Test fehlgeschlagen: {error_msg}")
                
                # Spezifische Hilfe bei häufigen Fehlern
                if 'Invalid Params' in error_msg:
                    print("💡 Mögliche Lösung: Token neu generieren")
                    print("   Führe 'python withings_client.py' aus und autorisiere erneut")
                
                return False
                
        except requests.RequestException as e:
            print(f"🌐 HTTP Fehler beim Verbindungstest: {e}")
            return False
        except Exception as e:
            print(f"❌ Allgemeiner Fehler beim Verbindungstest: {e}")
            return False


def setup_withings_api():
    """
    Hilfsfunktion für das initiale Withings API Setup
    """
    print("=== Withings API Setup ===")
    print("1. Gehe zu https://developer.withings.com/")
    print("2. Erstelle eine neue App")
    print("3. Notiere Client ID und Client Secret")
    print("4. Setze Redirect URI auf: http://localhost:8080/callback")
    print()
    
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("Client ID und Client Secret sind erforderlich!")
        return None
    
    # Speichere Credentials
    credentials = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:8080/callback'
    }
    
    try:
        with open('withings_credentials.json', 'w') as f:
            json.dump(credentials, f, indent=2)
        print("Credentials gespeichert in withings_credentials.json")
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")
        return None
    
    # Erstelle Client und starte Autorisierung
    client = WithingsClient(client_id, client_secret)
    
    if client.authorize():
        print("\\nWithings API erfolgreich eingerichtet!")
        return client
    else:
        print("\\nFehler bei der Autorisierung!")
        return None


if __name__ == '__main__':
    # Test/Setup Script
    credentials_file = Path('withings_credentials.json')
    
    if not credentials_file.exists():
        print("Keine Withings Credentials gefunden. Starte Setup...")
        client = setup_withings_api()
    else:
        # Lade existierende Credentials
        with open(credentials_file, 'r') as f:
            creds = json.load(f)
        
        client = WithingsClient(
            creds['client_id'],
            creds['client_secret'],
            creds.get('redirect_uri', 'http://localhost:8080/callback')
        )
        
        # Teste Verbindung
        if not client.test_connection():
            print("Autorisierung erforderlich...")
            client.authorize()
    
    if client and client.test_connection():
        # Teste Datenabfrage der letzten 30 Tage
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        print(f"\\nTeste Datenabfrage: {start_date.date()} bis {end_date.date()}")
        data = client.get_blood_pressure_data(start_date, end_date)
        
        if data:
            print(f"Erfolgreich {len(data)} Messungen abgerufen!")
            print("Beispiel-Daten:")
            for entry in data[:3]:  # Zeige erste 3 Einträge
                print(f"  {entry['timestamp'].strftime('%Y-%m-%d %H:%M')} - "
                      f"SYS: {entry['sys']}, DIA: {entry['dia']}, Puls: {entry['pulse']}")
        else:
            print("Keine Blutdruckdaten gefunden.")
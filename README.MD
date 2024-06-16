## Installation
1. Microsoft Edge oder Firefox muss auf dem Sytem installiert sein
2. Python 3.6+
3. Python Pakete installieren:
```(bash)
pip install -r requirements.txt
```
4. Erstellen einer .env Datei mit Email und Passwort:
```
EMAIL=vorname.nachname@stud-provadis-hochschule.de
PASSWORD=deinpasswort
```
5. Starten des Scripts:
python main.py [Anzahl_der_Dateien] [headless] [browser]
Der browser kann optional auf firefox durch das Browser-Argument gesetzt werden, Standardmäßig wird Edge benutzt.
# Beispiel:
```(bash)
python main.py 1500 true firefox
```
6. Ein Ordner mit dem Namen "Provadis-Coach-Mirror" muss einen Ordner "über" dem sein, in dem das Script ausgeführt wird.
Beispielhafte Ordnerstruktur:
```
Dokumente
----Provadis-Coach-Mirror
----Provadis-Scraper
--------main.py
--------(restliche Dateien)
```

Für Linux-Nutzer wird empfohlen, ein venv zu erstellen:
# Schritt 1: Navigieren zum Projektverzeichnis
cd /path/to/your/project

# Schritt 2: Erstellen eines virtuellen Umfelds
python3 -m venv venv

# Schritt 3: Aktivieren des virtuellen Umfelds
# Auf Linux/MacOS
```
source venv/bin/activate
```
# Auf Windows
```
.\venv\Scripts\activate
```

# Schritt 4: Installieren der Abhängigkeiten
pip install -r requirements.txt


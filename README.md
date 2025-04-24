# Provadis Scraper

Dieses Projekt scrapt Dateien von der Provadis Coach Website und speichert sie lokal. Es unterstützt sowohl lokale Ausführung als auch die Ausführung in einem Docker-Container.

## Installation mit Python (keine Git-Integration)
Für Docker, [Installation mit Docker](#docker-setup)

### Voraussetzungen

- Python 3.6+
- Git
- Firefox muss auf dem System installiert sein

### Virtuelle Umgebung einrichten

1. Navigieren Sie zum Projektverzeichnis:
    ```bash
    cd /path/to/your/project
    ```

2. Erstellen Sie eine virtuelle Umgebung:
    ```bash
    python3 -m venv venv
    ```

3. Aktivieren Sie die virtuelle Umgebung:
    - Auf Linux/MacOS:
        ```bash
        source venv/bin/activate
        ```
    - Auf Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4. Installieren Sie die Python-Pakete:
    ```bash
    pip install -r requirements.txt
    ```

5. Erstellen Sie eine `.env` Datei mit Email und Passwort:
    ```plaintext
    EMAIL=your_email@example.com
    PASSWORD=your_password
    ```

6. Ein Ordner mit dem Namen "Provadis-Coach-Mirror" muss einen Ordner "über" dem sein, in dem das Script ausgeführt wird.
    Beispielhafte Ordnerstruktur:
    ```plaintext
    Dokumente
    ├── Provadis-Coach-Mirror
    └── Provadis-Scraper
        ├── main.py
        ├── docker_main.py
        ├── download_files.py
        ├── scraper.py
        ├── utils.py
        ├── requirements.txt
        └── README.md
    ```

## Ausführung

Für die normale Ausführung, folgen Sie den untenstehenden Schritten:

```bash
python main.py [Anzahl_der_Dateien] [headless] [browser]
```
Beispiel:
```bash
python main.py 1500 True firefox
```

## Docker-Setup
Docker Voraussetzungen
    Docker installiert auf dem System

Docker-Konfiguration
1. Erstellen oder aktualisieren Sie die `.env` Datei im Projektverzeichnis mit den folgenden Inhalten:
    ```plaintext
    EMAIL=your_email@example.com
    PASSWORD=your_password
    GIT_USERNAME=your_github_username
    GIT_PAT=your_personal_access_token
    GIT_REPO=your_repository_url
    ```

    Für die Variable `GIT_PAT` müssen Sie einen [PAT generieren](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).


### Docker-Container erstellen und ausführen
Bauen Sie das Docker-Image:
```bash
docker build -t provadis-scraper .
```
Führen Sie den Docker-Container aus:
```bash
docker run -d --name provadis-scraper-container provadis-scraper
```
Der Scraper wird alle 10 Minuten ausgeführt und synchronisiert die Dateien mit Ihrem Git-Repository.

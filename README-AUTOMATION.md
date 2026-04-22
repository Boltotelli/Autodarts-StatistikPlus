# Statistik+ – Automatischer Release-Workflow

Mit diesem Setup musst du neue Releases nicht mehr von Hand zusammenklicken. GitHub Actions erledigt für dich:

- `manifest.json` auf die neue Version setzen
- `update.xml` mit der richtigen Release-URL erzeugen
- die CRX-Datei bauen
- ein GitHub-Release anlegen
- `source/manifest.json` und `update.xml` zurück nach `main` committen

## Einmalig einrichten

### 1) `extension-private-key.pem` lokal behalten
Diese Datei **niemals** ins Repo hochladen.

### 2) PEM als GitHub Secret speichern
Du brauchst den Inhalt der PEM-Datei Base64-kodiert als Secret.

#### Windows PowerShell
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("extension-private-key.pem"))
```

#### macOS / Linux / Git Bash
```bash
base64 -w 0 extension-private-key.pem
```
Falls `-w 0` nicht geht:
```bash
base64 extension-private-key.pem | tr -d '\n'
```

Dann in GitHub:
- Repo öffnen
- **Settings** → **Secrets and variables** → **Actions**
- **New repository secret**
- Name: `CHROME_EXTENSION_KEY_B64`
- Value: der komplette Base64-String

## Dateien, die ins Repo gehören
Hochladen bzw. committen:
- `source/`
- `update.xml`
- `.github/workflows/release.yml`
- `scripts/build_release.py`
- `README-AUTOMATION.md`

Nicht hochladen:
- `extension-private-key.pem`
- lokale ZIP-Dateien

## Release erstellen

### Variante A: per Git Tag
Lokal im Repo:
```bash
git tag v0.4.30
git push origin v0.4.30
```

### Variante B: direkt in GitHub
- **Actions** öffnen
- Workflow **Build and Release Statistik+** auswählen
- **Run workflow**
- Version z. B. `0.4.30` eintragen

## Was danach automatisch passiert
Der Workflow erzeugt:
- `statistik-plus-v0.4.30.crx`
- `statistik-plus-source-v0.4.30.zip`
- GitHub Release `v0.4.30`
- aktualisierte `update.xml`
- aktualisierte `source/manifest.json`

## Wichtige Hinweise
- Die Versionsnummer muss immer steigen.
- Der gleiche private Schlüssel muss immer weiterverwendet werden, sonst ändert sich die Extension-ID.
- Für Chrome unter Windows/macOS bleibt für die lokale Entwickler-Nutzung weiterhin **Entpackte Erweiterung laden** der normale Weg.

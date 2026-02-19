# Architektur — GlassesScraper MVP

## Überblick

```
Config (YAML + Pydantic) → Orchestrator → Shop-Module → Dimension Parser
                                ↓              ↓              ↓
                          Rate-Limiter    Browser (PW)    Validators
                                ↓              ↓              ↓
                            Retry          Scroll/Wait    Filters
                                ↓              ↓              ↓
                          State-File     Extraktoren    MatchResult
                                ↓
                          Exporter (CSV/JSON)
```

## Komponenten

### Config (`config.py` + `config.yaml`)
- Pydantic v2 Schema für alle Suchkriterien
- Fail-fast Validierung beim Start (min < max, etc.)
- Default-Werte für optionale Parameter

### Selektoren (`selectors/smartbuyglasses.yaml`)
- Externalisierte CSS-Selektoren + Labels
- Primär + Fallback-Selektoren
- Versioniert mit Datum
- Kommentare wo jeder Selektor gefunden wurde

### Models (`models.py`)
- `Frame` Dataclass: A, B, DBL, Temple, Preis, Name, URL, etc.
- Berechnete Properties: frame_pd, category
- Validierung via Validators
- Equality via URL (für Deduplizierung)

### Validators (`validators.py`)
- Plausibilitätschecks: A 35-65mm, Preis > 0, etc.
- Dezimalformat-Handling (50.5 vs 50,5)
- Währungs-Parsing (€, $, £, ₩)
- ValidationWarning für implausible Werte

### Filters (`filters.py`)
- Criteria-Klasse (aus Config geladen)
- `check(frame) → MatchResult(passed, category, reason)`
- Kategorien: IDEAL, GRÖSSER, AUSSERHALB

### Dimension Parser (`dimension_parser.py`)
- Multi-Format: "50-21-145", gelabelte Werte, HTML-Tabellen
- Multi-Sprache: EN/DE Labels
- Label-Aliases (Lens Width = Eye Size = Caliber = Glasbreite)
- Regex-Kaskade mit Fallbacks
- Multivariant: Alle Größen pro Produkt extrahieren

### Errors (`errors.py`)
- Exception-Hierarchie (siehe 04-decisions.md ADR-004)
- Jeder Fehlertyp hat definierte Retry-Strategie

### Retry (`retry.py`)
- Exponential Backoff (2s → 4s → 8s)
- Konfigurierbare max_retries pro Fehlertyp
- Respektiert Retry-After Header bei 429

### Rate-Limiter (`rate_limiter.py`)
- Adaptive Delays basierend auf Response-Zeit
- Soft/Hard Request-Limits pro Minute
- Zwangspause bei Hard-Limit

### State (`state.py`)
- Pause/Resume via JSON State-File
- Speichert: besuchte URLs, bisherige Ergebnisse, Position
- Schreibt nach jedem verarbeiteten Produkt
- Automatische Erkennung ob Resume möglich

### Browser (`browser.py`)
- Playwright + playwright-stealth
- Scroll-to-Bottom für Lazy Loading
- Wait-for-Network-Idle
- Cookie-Banner automatisch schließen
- CAPTCHA-Erkennung + Graceful Stop
- Crash Recovery (Browser-Neustart)

### Shop-Module (`shops/`)
- `BaseShop` abstrakte Basisklasse
- `SmartBuyGlasses` MVP-Implementierung
- Liest Selektoren aus YAML
- Interface: get_catalog_url, get_product_links, extract_dimensions, etc.

### Orchestrator (`orchestrator.py`)
- Steuert den Gesamtablauf
- Error Recovery (Produkt crasht → nächstes Produkt)
- URL-Deduplizierung über Seiten
- Loop-Erkennung (Pagination)
- Gesamtzahl-Vergleich (Sanity Check)
- Progress-Callback
- Run-Stats (Metriken)

### Exporter (`exporter.py`)
- CSV + JSON Export
- Timestamp im Dateinamen
- Gruppierung nach Modell
- Summary-Ausgabe

### Logger (`logger.py`)
- Strukturiertes JSON-Logging
- Separate Log-Datei pro Run
- Log-Levels: DEBUG, INFO, WARNING, ERROR

## Datenfluss

```
1. Config laden + validieren (fail-fast)
2. robots.txt prüfen
3. State-File prüfen (Resume möglich?)
4. Browser starten
5. Katalogseite laden
6. Für jede Seite:
   a. Scroll + Wait
   b. Produkt-Links extrahieren
   c. Gegen URL-Set deduplizieren
   d. Für jedes neue Produkt:
      - Produktseite laden (mit Retry)
      - Rate-Limiter beachten
      - Maße extrahieren (Dimension Parser)
      - Validieren (Plausibilitätschecks)
      - Filtern (Criteria Check)
      - Match → Speichern
      - State-File updaten
   e. Nächste Seite? Loop-Check?
7. Browser schließen
8. Ergebnisse exportieren (CSV/JSON)
9. Summary + Stats ausgeben
```

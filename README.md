# 🕶️ GlassesScraper

Automatisierter Scraper für Brillen-Onlineshops — findet Gestelle, die exakten Maßkriterien entsprechen.

## Problem

Bei starker Kurzsichtigkeit (~−6,5 dpt) hängen Glasdicke, Gewicht und Optik kritisch von der Gestellgröße ab. Die manuelle Suche ist extrem aufwändig:
- Shops bieten keine präzisen Maß-Filter
- Maße stehen erst auf der Produktdetailseite
- Hunderte Produkte müssen einzeln geprüft werden
- Internationale Shops (Korea, Singapur) sind schwer zu durchsuchen

## Lösung

GlassesScraper durchsucht Shops automatisch per Playwright, extrahiert Gestellmaße und filtert nach einem konfigurierbaren Maßkorridor.

## Suchkriterien (Default)

| Parameter | Ideal | Max |
|-----------|-------|-----|
| A (Scheibenbreite) | 48–50 mm | 52 mm |
| B (Scheibenhöhe) | 36–38 mm | 40 mm |
| DBL (Steg) | 19–21 mm | 18–22 mm |
| Frame-PD (A+DBL) | 68–70 mm | 67–71 mm |
| Form | oval/soft | keine Außenspitze |
| Material | Vollrand Acetat | — |

## MVP-Scope

- **1 Shop:** SmartBuyGlasses
- **Output:** CSV/JSON mit Matches (Name, URL, Preis, Maße, Kategorie)
- **Kategorien:** ✅ IDEAL · ⚠️ GRÖSSER · ❌ AUSSERHALB

## Tech Stack

- **Python 3.12+**
- **Playwright** + playwright-stealth (Browser-Automation)
- **Pydantic v2** (Config-Validierung)
- **pytest** (TDD, ~103 Tests)

## Architektur

```
Config (YAML/Pydantic) → Orchestrator → Shop-Module → Dimension Parser
                              ↓              ↓              ↓
                        Rate-Limiter    Browser (PW)    Validators
                              ↓              ↓              ↓
                          State-File    Extraktoren     Filters
                              ↓                            ↓
                        Exporter (CSV/JSON)          MatchResult
```

**Key Features:**
- Externalisierte CSS-Selektoren (YAML) — Wartung ohne Code-Änderung
- Adaptive Rate-Limiting basierend auf Response-Zeit
- Pause/Resume via State-File
- Multivariant-Handling (alle Größen pro Modell)
- CAPTCHA-Erkennung + Graceful Stop
- Exception-Hierarchie mit typisierten Retry-Strategien

## Projektstruktur

```
glasses-scraper/
├── docs/                  # Projekt-Dokumentation
│   ├── 00-vision.md
│   ├── 01-requirements.md
│   ├── 02-architecture.md
│   ├── 03-tdd-plan.md
│   ├── 04-decisions.md    # 8 ADRs
│   ├── 05-progress.md
│   └── 06-review-feedback.md
├── src/                   # Source Code
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
├── selectors/             # Externalisierte CSS-Selektoren
├── state/                 # Pause/Resume State-Files
├── results/               # Scraping-Ergebnisse
└── logs/                  # Strukturierte Logs
```

## Status

🟡 **Planung abgeschlossen** — bereit für Entwicklung (Tag 1 von 5)

## Lizenz

Private Nutzung.

---

*Built with 🍒 by [avacitronessa](https://github.com/avacitronessa) & [Amely](https://openclaw.ai)*

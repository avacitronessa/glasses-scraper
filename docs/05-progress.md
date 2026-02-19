# Progress — GlassesScraper

## Status: 🟡 Planung abgeschlossen, bereit für Entwicklung

## Meilensteine

### ✅ Planung
- [x] Fachliche Anforderungen definiert (Maßkorridor, 6 Kriterien)
- [x] Erste manuelle Recherche durchgeführt (~25 Kandidaten gefunden)
- [x] Architektur designed (7 Recherche-Module, Orchestrator-Pattern)
- [x] TDD-Plan erstellt (7 Layer, ~103 Tests)
- [x] 2 Review-Runden durch User (15 Verbesserungspunkte)
- [x] Alle Verbesserungen bewertet und in MVP/Phase 2 sortiert
- [x] MVP-Scope finalisiert
- [x] 8 Architecture Decision Records geschrieben
- [x] Projekt-Dokumentation erstellt

### 🔲 Entwicklung (Tag 1-5)
- [ ] Tag 1 AM: Layer 1 — Config + Models + Validators (~15 Tests)
- [ ] Tag 1 PM: Layer 2 — Filters (~15 Tests)
- [ ] Tag 2 AM: Layer 3 — Dimension Parser (~20 Tests)
- [ ] Tag 2 PM: Layer 3b — Errors + Retry + RateLimiter (~15 Tests)
- [ ] Tag 3: Fixtures sammeln + Layer 4 — SBG Extraktion (~15 Tests)
- [ ] Tag 3 PM: Layer 4b — Pagination + State (~10 Tests)
- [ ] Tag 4 AM: Layer 5 — Orchestrator (~10 Tests)
- [ ] Tag 4 PM: Layer 6 — Exporter (~8 Tests)
- [ ] Tag 5 AM: Layer 7 — Browser + E2E (~5 Tests)
- [ ] Tag 5 PM: Bugfixes, Refactoring, README

### 🔲 Phase 2 (nach MVP)
- [ ] Weitere Shops (Zenni, Mister Spex, Koreanische Shops)
- [ ] Circuit Breaker, Canary Tests
- [ ] Proxy-Rotation, Parallelisierung
- [ ] SQLite-Persistenz + Diff zwischen Runs
- [ ] SaaS-Ausbau (siehe heir-search Projekt)

## Nächste Aktion
→ **Tag 1 starten:** Tests für Config (Pydantic) + Models + Validators schreiben
→ Rolle: Senior Developer
→ Zuerst: pyproject.toml + pytest Setup

## Offene Fragen
- Keine aktuell

## Blockers
- Keine aktuell

# Architecture Decision Records — GlassesScraper

## ADR-001: TDD-Ansatz
- **Datum:** 2026-02-19
- **Kontext:** Web-Scraping ist fragil. Fehler treten oft erst nach Minuten auf.
- **Entscheidung:** Test-Driven Development. Tests zuerst, Code danach.
- **Begründung:** Feedback-Loop von Sekunden statt Minuten. ~103 Tests geben Vertrauen.
- **Trade-off:** Höherer initialer Aufwand, aber deutlich weniger Debugging.

## ADR-002: Selektoren externalisiert (YAML)
- **Datum:** 2026-02-19
- **Kontext:** DOM-Strukturen von Shops ändern sich regelmäßig.
- **Entscheidung:** CSS-Selektoren in `selectors/smartbuyglasses.yaml`, nicht im Code.
- **Begründung:** Wartung ohne Code-Änderung. Primär- + Fallback-Selektoren. Review-Feedback Punkt 2.
- **Trade-off:** Etwas mehr Komplexität beim Laden, aber massiver Wartungsvorteil.

## ADR-003: Pydantic für Config-Validierung
- **Datum:** 2026-02-19
- **Kontext:** Config-Fehler (min > max) sollten sofort erkannt werden, nicht nach 10min Scraping.
- **Entscheidung:** Pydantic v2 Schema für config.yaml mit fail-fast Validierung.
- **Begründung:** Review-Feedback Punkt 15. Fail-fast Prinzip.
- **Alternativen:** Manuelle Validierung (fehleranfällig), JSON Schema (weniger Python-nativ).

## ADR-004: Exception-Hierarchie + Retry
- **Datum:** 2026-02-19
- **Kontext:** Web-Scraping hat viele Fehlerquellen (Netzwerk, Parsing, Bot-Detection).
- **Entscheidung:** Spezifische Exception-Typen mit definierter Retry-Strategie pro Typ.
- **Begründung:** Review-Feedback Punkt 1. Generisches `except Exception` ist gefährlich.
- **Details:** NetworkError → Retry 3x mit Backoff. ParsingError → Log + Skip. BotDetection → Stop.

## ADR-005: Adaptive Rate-Limiting
- **Datum:** 2026-02-19
- **Kontext:** Fixer Delay (1.5s) ist zu aggressiv bei langsamem Server, zu langsam bei schnellem.
- **Entscheidung:** Adaptive Delays basierend auf Server-Response-Zeit.
- **Begründung:** Review-Feedback Punkt 4. Respektvoller Umgang mit fremden Servern.

## ADR-006: Pause/Resume mit State-File
- **Datum:** 2026-02-19
- **Kontext:** Bei 1000+ Produkten ist ein Crash wahrscheinlich.
- **Entscheidung:** JSON State-File nach jedem verarbeiteten Produkt.
- **Begründung:** Review-Feedback Punkt 10. Resume statt Neustart spart Stunden.
- **Trade-off:** I/O-Overhead pro Produkt (vernachlässigbar vs. 3s Delay pro Seite).

## ADR-007: Multivariant-Handling
- **Datum:** 2026-02-19
- **Kontext:** Brillen kommen oft in 2-3 Größen (z.B. 48-21 und 52-21).
- **Entscheidung:** Alle Größenvarianten von der Produktseite extrahieren, jede passende als eigenen Eintrag.
- **Begründung:** Review-Feedback Punkt 7. Sonst verpassen wir passende kleinere Größen.

## ADR-008: MVP = 1 Shop (SmartBuyGlasses)
- **Datum:** 2026-02-19
- **Kontext:** 13 Shops gleichzeitig zu scrapen ist zu komplex für den MVP.
- **Entscheidung:** Nur SmartBuyGlasses im MVP. Weitere Shops in Phase 2.
- **Begründung:** Lieber 1 Shop richtig als 13 halbgar. Plugin-Architektur ermöglicht einfache Erweiterung.

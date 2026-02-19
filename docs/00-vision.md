# GlassesScraper — Vision

## Was
Ein automatisierter Scraper der Brillen-Onlineshops weltweit nach Gestellen durchsucht, die exakten Maßkriterien entsprechen — optimiert für hohe Korrektionswerte (ca. −6,5 dpt).

## Warum
Bei starker Kurzsichtigkeit sind Glasdicke, Gewicht und Kantenoptik kritisch abhängig von der Gestellgröße. Die manuelle Suche nach passenden Gestellen ist extrem zeitaufwändig, weil:
- Shops keine präzisen Maß-Filter anbieten
- Maße oft erst auf der Produktdetailseite stehen
- Hunderte von Produkten einzeln geprüft werden müssen
- Internationale Shops (Korea, Singapur) tolle Modelle haben, aber schwer zu durchsuchen sind

## Für wen
- Primär: Die Nutzerin (Damen-Brillen, Vollrand Acetat)
- Perspektive: Potenziell als SaaS für andere Brillenträger mit hoher Korrektur (→ heir-search für SaaS-Plan)

## Erfolg = 
- Scraper läuft durch, findet alle passenden Gestelle in einem Shop
- Ergebnis: CSV/Excel mit Artikelname, Shop, URL, Preis, Maße, Kategorie
- Korrekte Filterung nach dem definierten Maßkorridor
- Robust genug um regelmäßig genutzt zu werden

## MVP-Scope
- 1 Shop: SmartBuyGlasses
- TDD-Entwicklung
- ~103 Tests
- ~5 Tage Entwicklungszeit

"""Validators — Plausibilitätschecks für extrahierte Daten."""

import re
from typing import Optional


class ValidationWarning(Exception):
    """Warnung bei implausiblen Werten (kein harter Fehler)."""

    pass


# Plausible Bereiche für Brillenmaße (in mm)
DIMENSION_BOUNDS = {
    "a": (30, 70),
    "b": (20, 60),
    "dbl": (10, 30),
    "temple": (100, 160),
}


def validate_dimension(name: str, value: float) -> bool:
    """Prüft ob ein Maß plausibel ist."""
    bounds = DIMENSION_BOUNDS.get(name)
    if bounds is None:
        return True
    low, high = bounds
    if value < low or value > high:
        raise ValidationWarning(
            f"{name}={value}mm ist implausibel (erwartet: {low}-{high}mm)"
        )
    return True


def validate_price(price: float) -> bool:
    """Prüft ob ein Preis plausibel ist."""
    if price <= 0:
        raise ValidationWarning(f"price={price} ist ungültig (muss > 0 sein)")
    return True


def validate_url(url: str) -> bool:
    """Prüft ob eine URL gültig ist."""
    if not url or not re.match(r"https?://\S+", url):
        raise ValidationWarning(f"url='{url}' ist keine gültige URL")
    return True


def parse_decimal(value: str) -> Optional[float]:
    """Parst Dezimalzahlen in verschiedenen Formaten (Punkt, Komma, mit Einheit)."""
    if not value:
        return None
    # Einheiten entfernen
    cleaned = re.sub(r"[a-zA-Z\s]+$", "", value.strip())
    # Komma → Punkt
    cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None

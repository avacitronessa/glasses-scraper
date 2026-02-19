"""Filters — Bewertung von Frames gegen Suchkriterien."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.config import CriteriaConfig, RangeConfig
from src.models import Frame


class Category(Enum):
    IDEAL = "ideal"
    LARGER = "larger"
    OUTSIDE = "outside"


@dataclass
class MatchResult:
    passed: bool
    category: Category
    reason: Optional[str] = None


@dataclass
class Criteria:
    a: RangeConfig
    b: RangeConfig
    dbl: RangeConfig
    frame_pd: RangeConfig

    @classmethod
    def from_config(cls, config: CriteriaConfig) -> "Criteria":
        return cls(
            a=config.a,
            b=config.b,
            dbl=config.dbl,
            frame_pd=config.frame_pd,
        )


def _check_range(
    value: Optional[float], range_cfg: RangeConfig, name: str
) -> tuple[Optional[Category], Optional[str]]:
    """Prüft einen Wert gegen einen Bereich.

    Returns:
        (None, None) wenn im Idealbereich
        (LARGER, None) wenn akzeptabel aber nicht ideal
        (OUTSIDE, reason) wenn außerhalb
    """
    if value is None:
        return Category.OUTSIDE, f"{name} fehlt"

    if value < range_cfg.min or value > range_cfg.max:
        return (
            Category.OUTSIDE,
            f"{name}={value}mm außerhalb ({range_cfg.min}-{range_cfg.max})",
        )

    if range_cfg.ideal_min <= value <= range_cfg.ideal_max:
        return None, None  # ideal

    return Category.LARGER, None  # akzeptabel


def check(frame: Frame, criteria: Criteria) -> MatchResult:
    """Bewertet ein Frame gegen die Suchkriterien."""
    # A ist Pflicht
    cat_a, reason_a = _check_range(frame.a, criteria.a, "A")
    if cat_a == Category.OUTSIDE:
        return MatchResult(passed=False, category=Category.OUTSIDE, reason=reason_a)

    # DBL ist Pflicht
    cat_dbl, reason_dbl = _check_range(frame.dbl, criteria.dbl, "DBL")
    if cat_dbl == Category.OUTSIDE:
        return MatchResult(passed=False, category=Category.OUTSIDE, reason=reason_dbl)

    # Frame-PD prüfen (berechnet aus A + DBL)
    if frame.frame_pd is not None:
        cat_fpd, reason_fpd = _check_range(
            frame.frame_pd, criteria.frame_pd, "Frame-PD"
        )
        if cat_fpd == Category.OUTSIDE:
            return MatchResult(
                passed=False,
                category=Category.OUTSIDE,
                reason=reason_fpd,
            )
    else:
        cat_fpd = None

    # B ist optional
    cat_b = None
    if frame.b is not None:
        cat_b, reason_b = _check_range(frame.b, criteria.b, "B")
        if cat_b == Category.OUTSIDE:
            return MatchResult(
                passed=False,
                category=Category.OUTSIDE,
                reason=reason_b,
            )

    # Gesamtkategorie: LARGER wenn mindestens ein Wert nicht ideal
    all_cats = [cat_a, cat_b, cat_dbl, cat_fpd]
    if any(c == Category.LARGER for c in all_cats):
        return MatchResult(passed=True, category=Category.LARGER)

    return MatchResult(passed=True, category=Category.IDEAL)

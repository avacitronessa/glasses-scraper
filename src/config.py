"""Konfiguration — Pydantic-basiert mit fail-fast Validierung."""

from pathlib import Path

import yaml
from pydantic import BaseModel, model_validator


class RangeConfig(BaseModel):
    min: float
    max: float
    ideal_min: float
    ideal_max: float

    @model_validator(mode="after")
    def validate_range(self):
        if self.min < 0 or self.max < 0:
            raise ValueError(
                f"Negative Werte nicht erlaubt: min={self.min}, max={self.max}"
            )
        if self.min > self.max:
            raise ValueError(
                f"min ({self.min}) darf nicht größer sein als max ({self.max})"
            )
        if self.ideal_min > self.ideal_max:
            raise ValueError(
                f"ideal_min ({self.ideal_min}) darf nicht "
                f"größer sein als ideal_max ({self.ideal_max})"
            )
        return self


class CriteriaConfig(BaseModel):
    a: RangeConfig
    b: RangeConfig
    dbl: RangeConfig
    frame_pd: RangeConfig


class ScrapingConfig(BaseModel):
    base_url: str
    max_pages: int = 100
    max_retries: int = 3
    request_delay_min: float = 1.5
    request_delay_max: float = 4.0
    timeout: int = 30


class OutputConfig(BaseModel):
    format: str = "csv"
    directory: str = "results"


class AppConfig(BaseModel):
    criteria: CriteriaConfig
    scraping: ScrapingConfig
    output: OutputConfig


def load_config(path: Path) -> AppConfig:
    """Lädt und validiert die Konfiguration aus einer YAML-Datei."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return AppConfig(**data)

"""Tests für Config — Pydantic-basierte Konfiguration mit fail-fast Validierung."""

import pytest

from src.config import load_config


class TestLoadConfig:
    def test_loads_valid_yaml(self, tmp_path):
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
criteria:
  a: { min: 48, max: 52, ideal_min: 48, ideal_max: 50 }
  b: { min: 36, max: 40, ideal_min: 36, ideal_max: 38 }
  dbl: { min: 18, max: 22, ideal_min: 19, ideal_max: 21 }
  frame_pd: { min: 67, max: 71, ideal_min: 68, ideal_max: 70 }
scraping:
  base_url: "https://www.smartbuyglasses.com"
output:
  format: csv
  directory: results
""")
        config = load_config(config_file)
        assert config.criteria.a.min == 48
        assert config.criteria.a.max == 52

    def test_rejects_min_greater_than_max(self, tmp_path):
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
criteria:
  a: { min: 55, max: 48, ideal_min: 48, ideal_max: 50 }
  b: { min: 36, max: 40, ideal_min: 36, ideal_max: 38 }
  dbl: { min: 18, max: 22, ideal_min: 19, ideal_max: 21 }
  frame_pd: { min: 67, max: 71, ideal_min: 68, ideal_max: 70 }
scraping:
  base_url: "https://www.smartbuyglasses.com"
output:
  format: csv
  directory: results
""")
        with pytest.raises(ValueError, match="min.*max"):
            load_config(config_file)

    def test_rejects_negative_values(self, tmp_path):
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
criteria:
  a: { min: -5, max: 52, ideal_min: 48, ideal_max: 50 }
  b: { min: 36, max: 40, ideal_min: 36, ideal_max: 38 }
  dbl: { min: 18, max: 22, ideal_min: 19, ideal_max: 21 }
  frame_pd: { min: 67, max: 71, ideal_min: 68, ideal_max: 70 }
scraping:
  base_url: "https://www.smartbuyglasses.com"
output:
  format: csv
  directory: results
""")
        with pytest.raises(ValueError):
            load_config(config_file)

    def test_default_values(self, tmp_path):
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
criteria:
  a: { min: 48, max: 52, ideal_min: 48, ideal_max: 50 }
  b: { min: 36, max: 40, ideal_min: 36, ideal_max: 38 }
  dbl: { min: 18, max: 22, ideal_min: 19, ideal_max: 21 }
  frame_pd: { min: 67, max: 71, ideal_min: 68, ideal_max: 70 }
scraping:
  base_url: "https://www.smartbuyglasses.com"
output:
  format: csv
  directory: results
""")
        config = load_config(config_file)
        assert config.scraping.max_pages == 100
        assert config.scraping.max_retries == 3
        assert config.scraping.request_delay_min == 1.5

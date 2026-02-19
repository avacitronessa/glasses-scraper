"""Tests für Filters — IDEAL / GRÖSSER / AUSSERHALB Kategorisierung."""

import pytest

from src.config import load_config
from src.filters import Category, Criteria, check
from src.models import Frame


@pytest.fixture
def criteria(tmp_path):
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
    return Criteria.from_config(config.criteria)


def _frame(**kwargs) -> Frame:
    defaults = {
        "name": "Test",
        "url": "https://example.com/test",
        "shop": "TestShop",
        "a": 49,
        "b": 37,
        "dbl": 21,
        "temple": 140,
    }
    defaults.update(kwargs)
    return Frame(**defaults)


class TestPerfectMatch:
    def test_ideal_match(self, criteria):
        result = check(_frame(a=49, b=37, dbl=20), criteria)
        assert result.passed is True
        assert result.category == Category.IDEAL

    def test_larger_match(self, criteria):
        result = check(_frame(a=51, b=39, dbl=20), criteria)
        assert result.passed is True
        assert result.category == Category.LARGER


class TestRejectA:
    def test_a_too_large(self, criteria):
        result = check(_frame(a=55), criteria)
        assert result.passed is False
        assert result.category == Category.OUTSIDE

    def test_a_too_small(self, criteria):
        result = check(_frame(a=40), criteria)
        assert result.passed is False

    def test_a_just_over_max(self, criteria):
        result = check(_frame(a=53), criteria)
        assert result.passed is False


class TestRejectB:
    def test_b_too_large(self, criteria):
        result = check(_frame(b=45), criteria)
        assert result.passed is False


class TestRejectDBL:
    def test_dbl_too_small(self, criteria):
        result = check(_frame(dbl=15), criteria)
        assert result.passed is False

    def test_dbl_too_large(self, criteria):
        result = check(_frame(dbl=25), criteria)
        assert result.passed is False


class TestRejectFramePD:
    def test_frame_pd_too_low(self, criteria):
        result = check(_frame(a=48, dbl=16), criteria)  # FPD=64
        assert result.passed is False

    def test_frame_pd_too_high(self, criteria):
        result = check(_frame(a=52, dbl=24), criteria)  # FPD=76
        assert result.passed is False


class TestMissingValues:
    def test_missing_b_still_passes(self, criteria):
        result = check(_frame(b=None), criteria)
        assert result.passed is True

    def test_missing_a_fails(self, criteria):
        result = check(_frame(a=None), criteria)
        assert result.passed is False

    def test_missing_dbl_fails(self, criteria):
        result = check(_frame(dbl=None), criteria)
        assert result.passed is False


class TestEdgeCases:
    def test_exact_boundary_larger(self, criteria):
        result = check(_frame(a=52, b=40, dbl=22), criteria)  # FPD=74>71
        assert result.passed is False

    def test_exact_boundary_ideal_max(self, criteria):
        result = check(_frame(a=50, b=38, dbl=20), criteria)  # FPD=70
        assert result.passed is True
        assert result.category == Category.IDEAL

    def test_fpd_acceptable_but_not_ideal(self, criteria):
        result = check(_frame(a=50, b=38, dbl=21), criteria)  # FPD=71
        assert result.passed is True
        assert result.category == Category.LARGER

    def test_reason_contains_rejection_info(self, criteria):
        result = check(_frame(a=55), criteria)
        assert result.reason is not None
        assert "a" in result.reason.lower()

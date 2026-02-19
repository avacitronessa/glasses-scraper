"""Tests für Validators — Plausibilitätschecks für extrahierte Daten."""

import pytest

from src.validators import (
    ValidationWarning,
    parse_decimal,
    validate_dimension,
    validate_price,
    validate_url,
)


class TestValidateDimension:
    def test_plausible_a(self):
        assert validate_dimension("a", 49) is True

    def test_implausible_a_too_large(self):
        with pytest.raises(ValidationWarning, match="a"):
            validate_dimension("a", 500)

    def test_implausible_a_too_small(self):
        with pytest.raises(ValidationWarning, match="a"):
            validate_dimension("a", 5)

    def test_implausible_b_too_large(self):
        with pytest.raises(ValidationWarning, match="b"):
            validate_dimension("b", 200)

    def test_plausible_dbl(self):
        assert validate_dimension("dbl", 20) is True

    def test_implausible_dbl(self):
        with pytest.raises(ValidationWarning, match="dbl"):
            validate_dimension("dbl", 0)


class TestValidatePrice:
    def test_valid_price(self):
        assert validate_price(129.90) is True

    def test_zero_price_fails(self):
        with pytest.raises(ValidationWarning, match="price"):
            validate_price(0)

    def test_negative_price_fails(self):
        with pytest.raises(ValidationWarning, match="price"):
            validate_price(-10)


class TestValidateUrl:
    def test_valid_url(self):
        assert validate_url("https://example.com/product") is True

    def test_invalid_url(self):
        with pytest.raises(ValidationWarning, match="url"):
            validate_url("not-a-url")

    def test_empty_url(self):
        with pytest.raises(ValidationWarning, match="url"):
            validate_url("")


class TestParseDecimal:
    def test_dot_format(self):
        assert parse_decimal("50.5") == 50.5

    def test_comma_format(self):
        assert parse_decimal("50,5") == 50.5

    def test_integer(self):
        assert parse_decimal("50") == 50.0

    def test_with_mm_suffix(self):
        assert parse_decimal("50mm") == 50.0

    def test_invalid_returns_none(self):
        assert parse_decimal("abc") is None

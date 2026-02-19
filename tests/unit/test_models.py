"""Tests für Models — Frame Dataclass mit berechneten Properties."""

from src.models import Frame


class TestFrame:
    def test_creation(self):
        frame = Frame(
            name="Ray-Ban RB5154",
            url="https://example.com/rb5154",
            shop="SmartBuyGlasses",
            a=49,
            b=37,
            dbl=21,
            temple=140,
            price=129.90,
            currency="EUR",
        )
        assert frame.name == "Ray-Ban RB5154"
        assert frame.a == 49

    def test_frame_pd_calculation(self):
        frame = Frame(
            name="Test",
            url="https://example.com",
            shop="Test",
            a=49,
            b=37,
            dbl=21,
            temple=140,
        )
        assert frame.frame_pd == 70  # 49 + 21

    def test_frame_pd_none_when_missing_dbl(self):
        frame = Frame(
            name="Test",
            url="https://example.com",
            shop="Test",
            a=49,
            b=37,
            dbl=None,
            temple=140,
        )
        assert frame.frame_pd is None

    def test_to_dict(self):
        frame = Frame(
            name="Test",
            url="https://example.com",
            shop="Test",
            a=49,
            b=37,
            dbl=21,
            temple=140,
            price=99.90,
            currency="EUR",
        )
        d = frame.to_dict()
        assert d["name"] == "Test"
        assert d["frame_pd"] == 70
        assert d["price"] == 99.90

    def test_equality_by_url(self):
        frame1 = Frame(
            name="Test A",
            url="https://example.com/same",
            shop="Shop1",
            a=49,
            b=37,
            dbl=21,
        )
        frame2 = Frame(
            name="Test B",
            url="https://example.com/same",
            shop="Shop2",
            a=50,
            b=38,
            dbl=20,
        )
        assert frame1 == frame2

    def test_inequality_different_url(self):
        frame1 = Frame(
            name="Test",
            url="https://example.com/a",
            shop="Test",
            a=49,
            b=37,
            dbl=21,
        )
        frame2 = Frame(
            name="Test",
            url="https://example.com/b",
            shop="Test",
            a=49,
            b=37,
            dbl=21,
        )
        assert frame1 != frame2

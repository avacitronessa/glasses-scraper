"""Models — Frame Dataclass mit berechneten Properties."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Frame:
    name: str
    url: str
    shop: str
    a: Optional[float] = None
    b: Optional[float] = None
    dbl: Optional[float] = None
    temple: Optional[float] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    variant: Optional[str] = None

    @property
    def frame_pd(self) -> Optional[float]:
        """Frame-PD = A + DBL."""
        if self.a is not None and self.dbl is not None:
            return self.a + self.dbl
        return None

    def to_dict(self) -> dict:
        """Konvertiert Frame zu Dictionary inkl. berechneter Properties."""
        return {
            "name": self.name,
            "url": self.url,
            "shop": self.shop,
            "a": self.a,
            "b": self.b,
            "dbl": self.dbl,
            "temple": self.temple,
            "frame_pd": self.frame_pd,
            "price": self.price,
            "currency": self.currency,
            "variant": self.variant,
        }

    def __eq__(self, other):
        if not isinstance(other, Frame):
            return NotImplemented
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)

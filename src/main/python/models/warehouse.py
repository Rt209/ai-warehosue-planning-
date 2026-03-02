from dataclasses import dataclass, field
from typing import List, Optional
from .common import Box3


@dataclass
class Warehouse:
    """
    Represents a physical warehouse space for planning and optimization.
    """
    id: str
    name: str
    bounds: Box3
    metadata: dict = field(default_factory=dict)

    @property
    def volume(self) -> float:
        """Calculate the total volume of the warehouse."""
        size = self.bounds.max - self.bounds.min
        return size.x * size.y * size.z

    def __post_init__(self):
        if not self.name:
            self.name = f"Warehouse-{self.id}"

from dataclasses import dataclass, field
from typing import List, Optional
from .common import Box3
from .item import Item


@dataclass
class Warehouse:
    """
    Represents a physical warehouse space for planning and optimization.
    """
    id: str
    name: str
    bounds: Box3
    
    # Constraints
    max_load_capacity: float = 0.0  # Maximum total weight capacity
    
    # State
    items: List[Item] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def volume(self) -> float:
        """Calculate the total volume of the warehouse."""
        size = self.bounds.max - self.bounds.min
        return size.x * size.y * size.z

    @property
    def current_weight(self) -> float:
        """Calculate the total weight of all placed items."""
        return sum(item.weight for item in self.items if item.position is not None)

    def __post_init__(self):
        if not self.name:
            self.name = f"Warehouse-{self.id}"

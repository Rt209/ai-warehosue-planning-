from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from .common import Vec3


@dataclass
class Group:
    """Represents a category of items with specific planning requirements."""
    id: str
    name: str
    reserve_ratio: float = 0.0
    weight: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Item:
    """Represents an individual item to be stored and planned."""
    id: str
    group_id: str
    dimensions: Vec3
    rotatable: bool = True
    weight: float = 0.0
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def volume(self) -> float:
        """Calculate the volume of the item."""
        return self.dimensions.x * self.dimensions.y * self.dimensions.z

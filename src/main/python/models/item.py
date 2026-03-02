from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from .common import Vec3, Orientation


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
    """Represents an individual item to be stored and planned with physical constraints."""
    id: str
    group_id: str
    dimensions: Vec3
    
    # Constraints
    is_fragile: bool = False
    max_stack_weight: float = 0.0  # Weight this item can support on top
    weight: float = 0.0
    priority: int = 0
    allowed_orientations: List[Orientation] = field(default_factory=lambda: [Orientation.DEFAULT])
    
    # Spatial State (Populated by Engine)
    position: Optional[Vec3] = None
    current_orientation: Orientation = Orientation.DEFAULT
    
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def volume(self) -> float:
        """Calculate the volume of the item."""
        return self.dimensions.x * self.dimensions.y * self.dimensions.z

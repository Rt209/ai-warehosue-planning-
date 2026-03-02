from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


class Orientation(Enum):
    """Standard 3D orientations for box-shaped items."""
    DEFAULT = auto()      # (L, W, H)
    SIDE_LONG = auto()   # (W, L, H)
    UPRIGHT = auto()     # (H, W, L)
    UPRIGHT_LONG = auto() # (H, L, W)
    SIDE_FLAT = auto()   # (L, H, W)
    SIDE_UP = auto()     # (W, H, L)


@dataclass(frozen=True)
class Vec3:
    """A 3D vector for coordinate and size calculations."""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __sub__(self, other: 'Vec3') -> 'Vec3':
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other: 'Vec3') -> 'Vec3':
        if not isinstance(other, Vec3):
            return NotImplemented
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar: float) -> 'Vec3':
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    @property
    def magnitude(self) -> float:
        """Calculate the vector's length."""
        return (self.x**2 + self.y**2 + self.z**2)**0.5


@dataclass(frozen=True)
class Box3:
    """A 3D bounding box for spatial tracking."""
    min: Vec3
    max: Vec3

    @property
    def size(self) -> Vec3:
        """Calculate the box's dimensions."""
        return self.max - self.min

    @property
    def center(self) -> Vec3:
        """Calculate the geometric center of the box."""
        size = self.size
        return self.min + (size * 0.5)

    def contains(self, point: Vec3) -> bool:
        """Check if a point is within the bounding box."""
        return (self.min.x <= point.x <= self.max.x and
                self.min.y <= point.y <= self.max.y and
                self.min.z <= point.z <= self.max.z)

    def intersects(self, other: 'Box3') -> bool:
        """Check if this box intersects with another box."""
        return not (self.max.x < other.min.x or self.min.x > other.max.x or
                    self.max.y < other.min.y or self.min.y > other.max.y or
                    self.max.z < other.min.z or self.min.z > other.max.z)

from typing import List, Tuple, Optional
from models.common import Vec3, Orientation
from models.item import Item
from models.warehouse import Warehouse


class PackingEngine:
    """
    A deterministic 3D bin-packing engine that enforces physical constraints.
    """

    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse

    def pack(self, items: List[Item]) -> Tuple[List[Item], List[Item]]:
        """
        Attempt to pack a list of items into the warehouse.
        Returns (packed_items, unpacked_items).
        """
        # 1. Sort items by priority (desc) then volume (desc)
        sorted_items = sorted(
            items, 
            key=lambda x: (x.priority, x.volume), 
            reverse=True
        )

        packed: List[Item] = []
        unpacked: List[Item] = []

        for item in sorted_items:
            success = self._find_placement(item, packed)
            if success:
                packed.append(item)
            else:
                unpacked.append(item)

        # Update warehouse state
        self.warehouse.items = packed
        return packed, unpacked

    def _find_placement(self, item: Item, current_packed: List[Item]) -> bool:
        """
        Find a valid position and orientation for the item.
        Uses a simple greedy approach: bottom-to-top, back-to-front, left-to-right.
        """
        # Try each allowed orientation
        for orientation in item.allowed_orientations:
            dims = self._get_rotated_dimensions(item.dimensions, orientation)
            
            # Simple greedy search (can be optimized with Maximal Rectangles later)
            # For now, we iterate through a discretized grid or existing surfaces
            # To keep it simple and deterministic for Step 2:
            for z in range(0, int(self.warehouse.bounds.size.z - dims.z) + 1):
                for y in range(0, int(self.warehouse.bounds.size.y - dims.y) + 1):
                    for x in range(0, int(self.warehouse.bounds.size.x - dims.x) + 1):
                        pos = Vec3(float(x), float(y), float(z))
                        
                        if self._is_valid_placement(item, pos, dims, current_packed):
                            item.position = pos
                            item.current_orientation = orientation
                            return True
        return False

    def _get_rotated_dimensions(self, original: Vec3, orientation: Orientation) -> Vec3:
        """Calculate the dimensions of an item after rotation."""
        l, w, h = original.x, original.y, original.z
        if orientation == Orientation.SIDE_LONG:
            return Vec3(w, l, h)
        elif orientation == Orientation.UPRIGHT:
            return Vec3(h, w, l)
        elif orientation == Orientation.UPRIGHT_LONG:
            return Vec3(h, l, w)
        elif orientation == Orientation.SIDE_FLAT:
            return Vec3(l, h, w)
        elif orientation == Orientation.SIDE_UP:
            return Vec3(w, h, l)
        return original

    def _is_valid_placement(self, item: Item, pos: Vec3, dims: Vec3, packed: List[Item]) -> bool:
        """Check if placement is within bounds, doesn't collide, and respects physics."""
        
        # 1. Check Warehouse Bounds
        if (pos.x + dims.x > self.warehouse.bounds.max.x or
            pos.y + dims.y > self.warehouse.bounds.max.y or
            pos.z + dims.z > self.warehouse.bounds.max.z):
            return False

        # 2. Check Collisions with already packed items
        for other in packed:
            if self._rect_intersect(pos, dims, other.position, self._get_rotated_dimensions(other.dimensions, other.current_orientation)):
                return False

        # 3. Physical Constraints (Gravity/Support)
        if pos.z > 0:
            if not self._has_sufficient_support(pos, dims, packed):
                return False

        # 4. Fragility & Weight Constraints
        # Check if we are placing this on top of something fragile
        for other in packed:
            if self._is_directly_below(other, pos, dims):
                if other.is_fragile:
                    return False
                # Future: Check other.max_stack_weight vs item.weight
        
        return True

    def _rect_intersect(self, p1: Vec3, d1: Vec3, p2: Vec3, d2: Vec3) -> bool:
        """3D AABB intersection check."""
        return not (p1.x + d1.x <= p2.x or p2.x + d2.x <= p1.x or
                    p1.y + d1.y <= p2.y or p2.y + d2.y <= p1.y or
                    p1.z + d1.z <= p2.z or p2.z + d2.z <= p1.z)

    def _has_sufficient_support(self, pos: Vec3, dims: Vec3, packed: List[Item]) -> bool:
        """Check if the item has something underneath it (basic gravity check)."""
        # Simplified: Check if any item's top surface is at pos.z and overlaps in XY
        # In a real engine, we'd check for % of surface area supported.
        for other in packed:
            other_dims = self._get_rotated_dimensions(other.dimensions, other.current_orientation)
            if abs((other.position.z + other_dims.z) - pos.z) < 0.01:
                # Check XY overlap
                if self._xy_overlap(pos, dims, other.position, other_dims):
                    return True
        return False

    def _xy_overlap(self, p1: Vec3, d1: Vec3, p2: Vec3, d2: Vec3) -> bool:
        return not (p1.x + d1.x <= p2.x or p2.x + d2.x <= p1.x or
                    p1.y + d1.y <= p2.y or p2.y + d2.y <= p1.y)

    def _is_directly_below(self, other: Item, pos: Vec3, dims: Vec3) -> bool:
        """Check if 'other' is immediately under the proposed placement."""
        other_dims = self._get_rotated_dimensions(other.dimensions, other.current_orientation)
        return (abs((other.position.z + other_dims.z) - pos.z) < 0.01 and 
                self._xy_overlap(pos, dims, other.position, other_dims))

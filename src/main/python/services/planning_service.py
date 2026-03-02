from typing import List, Optional, Dict, Any
from models.warehouse import Warehouse
from models.item import Item
from services.packing_engine import PackingEngine


class PlanningService:
    """Service for orchestrating warehouse space optimization and reporting."""

    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse
        self.items_queue: List[Item] = []
        self.engine = PackingEngine(warehouse)

    def add_item(self, item: Item) -> bool:
        """Add an item to the planning queue."""
        self.items_queue.append(item)
        return True

    def calculate_utilization(self) -> float:
        """Calculate current volume utilization based on placed items."""
        if self.warehouse.volume == 0:
            return 0.0
        total_item_volume = sum(item.volume for item in self.warehouse.items if item.position is not None)
        return (total_item_volume / self.warehouse.volume) * 100.0

    def optimize_layout(self) -> Dict[str, Any]:
        """Perform the packing optimization and return a status report."""
        packed, unpacked = self.engine.pack(self.items_queue)
        
        # Once optimized, the engine updates the warehouse items.
        # Clear the queue for the next batch if needed, or keep for re-runs.
        return {
            "status": "success",
            "packed_count": len(packed),
            "unpacked_count": len(unpacked),
            "utilization": self.calculate_utilization()
        }

    def get_packing_report(self) -> Dict[str, Any]:
        """
        Generate a structured report of the current packing layout.
        This is used by the AI Agent for analysis and the Frontend for rendering.
        """
        items_data = []
        for item in self.warehouse.items:
            if item.position is not None:
                items_data.append({
                    "id": item.id,
                    "group_id": item.group_id,
                    "position": {"x": item.position.x, "y": item.position.y, "z": item.position.z},
                    "dimensions": {"x": item.dimensions.x, "y": item.dimensions.y, "z": item.dimensions.z},
                    "orientation": item.current_orientation.name,
                    "is_fragile": item.is_fragile,
                    "weight": item.weight
                })

        return {
            "warehouse_id": self.warehouse.id,
            "warehouse_size": {
                "x": self.warehouse.bounds.size.x,
                "y": self.warehouse.bounds.size.y,
                "z": self.warehouse.bounds.size.z
            },
            "utilization": self.calculate_utilization(),
            "total_weight": self.warehouse.current_weight,
            "items": items_data
        }

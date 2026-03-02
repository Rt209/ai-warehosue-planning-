import sys
from models.common import Vec3, Box3
from models.warehouse import Warehouse
from models.item import Item
from services.planning_service import PlanningService


def main():
    """Main application entry point."""
    print("--- AI Warehouse Planning System ---")

    # 1. Initialize Warehouse
    bounds = Box3(min=Vec3(0, 0, 0), max=Vec3(100, 100, 10))
    warehouse = Warehouse(id="WH001", name="Main Distribution Center", bounds=bounds)
    print(f"Initialized Warehouse: {warehouse.name} ({warehouse.volume} units)")

    # 2. Initialize Service
    planner = PlanningService(warehouse)

    # 3. Add sample items
    item1 = Item(id="ITM001", group_id="G1", dimensions=Vec3(2, 2, 2))
    item2 = Item(id="ITM002", group_id="G1", dimensions=Vec3(5, 5, 2))

    planner.add_item(item1)
    planner.add_item(item2)

    # 4. Show current status
    utilization = planner.calculate_utilization()
    print(f"Current Utilization: {utilization:.2f}%")
    print(f"Total items in queue: {len(planner.items)}")

    print("--- Ready for optimization ---")


if __name__ == "__main__":
    main()

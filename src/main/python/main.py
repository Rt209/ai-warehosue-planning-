import sys
import json
from models.common import Vec3, Box3, Orientation
from models.warehouse import Warehouse
from models.item import Item
from services.planning_service import PlanningService


def main():
    """Main application entry point."""
    print("--- AI Warehouse Planning System: Backend Integration Test ---")

    # 1. Initialize Warehouse (Small for testing)
    bounds = Box3(min=Vec3(0, 0, 0), max=Vec3(10, 10, 10))
    warehouse = Warehouse(id="WH001", name="Test Distribution Center", bounds=bounds)
    print(f"Initialized Warehouse: {warehouse.name} ({warehouse.volume} units)")

    # 2. Initialize Service
    planner = PlanningService(warehouse)

    # 3. Add items with physical constraints
    # Item 1: Large and Fragile (Should be on floor, nothing on top)
    item1 = Item(id="ITM-FRG", group_id="G1", dimensions=Vec3(5, 5, 2), is_fragile=True, weight=10.0)
    
    # Item 2: Large and Heavy (Should be on floor)
    item2 = Item(id="ITM-HVY", group_id="G1", dimensions=Vec3(5, 5, 2), weight=50.0)
    
    # Item 3: Small item (Should be placed next to others or on top of HVY)
    item3 = Item(id="ITM-SML", group_id="G1", dimensions=Vec3(2, 2, 2), weight=5.0)

    planner.add_item(item1)
    planner.add_item(item2)
    planner.add_item(item3)

    # 4. Perform Optimization
    print("\nExecuting Optimization...")
    result = planner.optimize_layout()
    print(f"Optimization Status: {result['status']}")
    print(f"Items Packed: {result['packed_count']} / Total: {result['packed_count'] + result['unpacked_count']}")

    # 5. Show detailed report (Simulating what the AI or Frontend would see)
    report = planner.get_packing_report()
    print("\nPacking Report Summary:")
    print(f"Utilization: {report['utilization']:.2f}%")
    print(f"Total Weight: {report['total_weight']} kg")
    
    # Pretty print the items list for visual verification
    print("\nPlaced Items Details:")
    for item in report['items']:
        print(f" - {item['id']} at {item['position']} (Fragile: {item['is_fragile']})")

    print("\n--- Integration Test Complete ---")


if __name__ == "__main__":
    main()

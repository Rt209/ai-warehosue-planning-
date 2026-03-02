import unittest
from models.common import Vec3, Box3, Orientation
from models.item import Item
from models.warehouse import Warehouse
from services.packing_engine import PackingEngine


class TestPackingEngine(unittest.TestCase):
    def setUp(self):
        self.bounds = Box3(min=Vec3(0, 0, 0), max=Vec3(10, 10, 10))
        self.warehouse = Warehouse(id="WH01", name="Test Warehouse", bounds=self.bounds)
        self.engine = PackingEngine(self.warehouse)

    def test_basic_packing(self):
        item1 = Item(id="I1", group_id="G1", dimensions=Vec3(2, 2, 2))
        packed, unpacked = self.engine.pack([item1])
        
        self.assertEqual(len(packed), 1)
        self.assertEqual(packed[0].position, Vec3(0, 0, 0))

    def test_gravity_support(self):
        # Place two items. The second should be on top of the first or on the floor.
        item1 = Item(id="I1", group_id="G1", dimensions=Vec3(2, 2, 2))
        item2 = Item(id="I2", group_id="G1", dimensions=Vec3(2, 2, 2))
        
        packed, unpacked = self.engine.pack([item1, item2])
        
        self.assertEqual(len(packed), 2)
        # Check if item2 is either on floor or on top of item1
        # Given our greedy engine, it should be next to item1 on the floor first
        self.assertEqual(packed[1].position.z, 0) 

    def test_fragility_constraint(self):
        # Item 1 is fragile. Item 2 should NOT be placed on top of it.
        item1 = Item(id="I1", group_id="G1", dimensions=Vec3(5, 5, 2), is_fragile=True)
        item2 = Item(id="I2", group_id="G1", dimensions=Vec3(2, 2, 2))
        
        # We'll force a scenario where it might want to stack by limiting floor space
        small_bounds = Box3(min=Vec3(0, 0, 0), max=Vec3(5, 5, 10))
        small_wh = Warehouse(id="WH02", name="Small", bounds=small_bounds)
        engine = PackingEngine(small_wh)
        
        packed, unpacked = engine.pack([item1, item2])
        
        # item2 cannot be on floor (item1 takes it all) and cannot be on top (item1 is fragile)
        self.assertEqual(len(packed), 1)
        self.assertEqual(len(unpacked), 1)
        self.assertEqual(unpacked[0].id, "I2")


if __name__ == '__main__':
    unittest.main()

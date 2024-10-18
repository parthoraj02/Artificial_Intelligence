import unittest
from unittest.mock import patch
from vacuum_cleaner_simulation import VacuumCleaner, Tile

class TestVacuumCleaner(unittest.TestCase):

    @patch('random.randint', return_value=1)  # Set the vacuum cleaner's initial position to tile B (index 1)
    def test_move_left(self, mock_randint):
        vacuum = VacuumCleaner()
        vacuum.move_left()
        self.assertEqual(vacuum.position, 0)  # Check if the vacuum moves to tile A (index 0)
        self.assertEqual(vacuum.moves, 1)  # Moves should increment

    @patch('random.randint', return_value=0)  # Set the vacuum cleaner's initial position to tile A (index 0)
    def test_move_right(self, mock_randint):
        vacuum = VacuumCleaner()
        vacuum.move_right()
        self.assertEqual(vacuum.position, 1)  # Check if the vacuum moves to tile B (index 1)
        self.assertEqual(vacuum.moves, 1)  # Moves should increment

    @patch('random.choice', side_effect=[True, False])  # Tile A is dirty, Tile B is clean
    @patch('random.randint', return_value=0)  # Vacuum starts at Tile A
    def test_suck(self, mock_randint, mock_choice):
        vacuum = VacuumCleaner()
        vacuum.suck()  # Should clean Tile A (index 0)
        self.assertFalse(vacuum.tiles[0].is_dirty)  # Tile A should be clean now
        self.assertEqual(vacuum.cleans, 1)  # Cleans should increment

        vacuum.move_right()
        vacuum.suck()  # Tile B is already clean
        self.assertEqual(vacuum.cleans, 1)  # Cleans should not increment

    @patch('random.random', side_effect=[0.3, 0.6])  # Random values: Tile A will be dirty, Tile B clean
    def test_update_tiles(self, mock_random):
        vacuum = VacuumCleaner()
        vacuum.update_tiles()  # Updates the dirtiness of the tiles
        self.assertTrue(vacuum.tiles[0].is_dirty)  # Tile A should be dirty
        self.assertFalse(vacuum.tiles[1].is_dirty)  # Tile B should remain clean

if __name__ == '__main__':
   unittest.main()
import unittest
import random
from UtilityBase import create_environment, run_simulation, collect, valid_moves, utility, move_towards_object, start


class TestSimulationFunctions(unittest.TestCase):

    def setUp(self):
        """Set up a default environment for testing."""
        random.seed(42)  # For reproducibility
        self.room = create_environment()

    def test_create_environment(self):
        """Test the creation of the environment."""
        room = create_environment()
        # Check if the room has the correct dimensions (6 rows, 8 columns)

        self.assertTrue(all(len(row) == 8 for row in room))
    def test_create_environment(self):
        room = create_environment()
        # Ensure there's at least one 'H' for hurdles
        hurdles = sum(row.count('H') for row in room)
        self.assertGreaterEqual(hurdles, 1)

    def test_start(self):
        x, y = start(self.room)
        self.assertNotEqual(self.room[x][y], 'H')

    def test_collect(self):
        """Test object collection logic."""
        room = self.room
        # Set up an object at a specific position
        room[2][3] = '*'
        self.assertTrue(collect(room, 2, 3))  # Should collect the object

    def test_valid_moves(self):
        """Test that valid moves are calculated correctly."""
        room = self.room
        visit_place = set()
        hurdle_stats = {'hurdles': 0, 'extra_moves': 0}
        valid = valid_moves(3, 3, room, visit_place, hurdle_stats)
        for x, y in valid:
            self.assertTrue(0 <= x < 6 and 0 <= y < 8 and room[x][y] != 'H')

    def test_utility(self):
        room = self.room
        distance = utility(2, 2, 4, 4, room)
        room[2][2] = 'H'
        self.assertEqual(utility(2, 2, 4, 4, room), float('inf'))

    def test_move_towards_object(self):
        room = self.room
        visit_place = set()
        hurdle_stats = {'hurdles': 0, 'extra_moves': 0}


        room[5][7] = '*'
        x, y = 0, 0  # Starting at the top-left

        new_x, new_y = move_towards_object(x, y, 5, 7, room, visit_place, hurdle_stats)


        self.assertLessEqual(abs(new_x - 5) + abs(new_y - 7), abs(x - 5) + abs(y - 7))

    # def test_run_simulation(self):
    #     """Test the entire simulation run. Manual visual verification required for plot."""
    #     run_simulation()  # The plot and print statements should be observed manually


if __name__ == '__main__':
    unittest.main()

import random


class Tile:
    def _init_(self):
        self.is_dirty = random.choice([True, False])

    def clean(self):
        self.is_dirty = False

    def _str_(self):
        return "Dirty" if self.is_dirty else "Clean"


class VacuumCleaner:
    def _init_(self):
        self.tiles = [Tile(), Tile()]
        self.position = random.randint(0, 1)
        self.moves = 0
        self.cleans = 0

    def move_left(self):
        if self.position > 0:
            self.position -= 1
            self.moves += 1
            print(f"Moved left to Tile {self.position + 1}")

    def move_right(self):
        if self.position < len(self.tiles) - 1:
            self.position += 1
            self.moves += 1
            print(f"Moved right to Tile {self.position + 1}")

    def suck(self):
        if self.tiles[self.position].is_dirty:
            print(f"Tile {self.position + 1} was dirty. Cleaning...")
            self.tiles[self.position].clean()
            self.cleans += 1
        else:
            print(f"Tile {self.position + 1} is already clean.")

    def update_tiles(self):
        for i, tile in enumerate(self.tiles):
            if random.random() < 0.5:
                tile.is_dirty = True
            else:
                tile.is_dirty = False
            print(f"Tile {i + 1} state updated to: {tile}")

    def print_status(self):
        print(f"Tile A: {self.tiles[0]}")
        print(f"Tile B: {self.tiles[1]}")
        print(f"Vacuum Cleaner is on Tile {self.position + 1}")
        print(f"Clean: {self.moves}")
        print(f"Moves: {self.cleans}")


def main():
    vacuum = VacuumCleaner()
    steps = 0
    max_steps = 1000

    while steps < max_steps:
        vacuum.print_status()

        print(f"Action for Tile {vacuum.position + 1}:")
        vacuum.suck()

        other_position = 1 - vacuum.position
        vacuum.position = other_position
        print(f"Moved to Tile {vacuum.position + 1}")

        vacuum.suck()

        if random.choice([True, False]):
            if vacuum.position > 0:
                vacuum.move_left()
            else:
                vacuum.move_right()

        vacuum.update_tiles()
        steps += 1
        print()

    print("Final State:")
    vacuum.print_status()

    if vacuum.cleans > 0:

        performance = vacuum.cleans / vacuum.moves

    else:
        performance = float('inf')

    print(f"Performance : {performance * 100:.1f}%")


if __name__ == "__main__":
    main()
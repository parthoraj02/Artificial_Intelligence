import random
import matplotlib.pyplot as plt
import numpy as np

def create_environment():
    room = []
    for _ in range(6):
        row = [random.choice([0, '*']) for _ in range(8)]
        room.append(row)

    num_hurdles = max(1, len(room) * len(room[0]) // 8)
    hurdle_positions = set()

    while len(hurdle_positions) < num_hurdles:
        i = random.randint(0, 5)
        j = random.randint(0, 7)
        if room[i][j] == 0:
            room[i][j] = 'H'
            hurdle_positions.add((i, j))

    return room

def print_environment(room):
    print("Environment:")
    for row in room:
        print(" ".join([str(cell) for cell in row]))
    print()

def start(room):
    while True:
        x = random.randint(1, 4)
        y = random.randint(1, 6)
        if room[x][y] != 'H':
            return x, y

def plot_room(room, x, y, visit_place, target_x, target_y, ax):
    ax.clear()

    room_np = np.zeros((6, 8))

    for i, row in enumerate(room):
        for j, cell in enumerate(row):
            if cell == '*':
                room_np[i, j] = 1  # Objects
            elif cell == 'H':
                room_np[i, j] = 999  # Hurdles

    room_np[x, y] = 2  # Truck position
    room_np[target_x, target_y] = 3  # Target position

    cmap = plt.colormaps['winter']  # or use plt.get_cmap('winter')
    ax.imshow(room_np, cmap=cmap, vmin=-1, vmax=1000)

    for (i, j) in visit_place:
        ax.text(j, i, 'V', ha='center', va='center', color='black', fontsize=14, fontweight='bold',
                fontname='Comic Sans MS')

    ax.text(y, x, 'C', ha='center', va='center', color='red', fontsize=16, fontweight='bold', fontname='Comic Sans MS')
    ax.text(target_y, target_x, 'T', ha='center', va='center', color='yellow', fontsize=20, fontweight='bold',
            fontname='Comic Sans MS')

    for i, row in enumerate(room):
        for j, cell in enumerate(row):
            if cell == '*':
                ax.text(j, i, '*', ha='center', va='center', color='white', fontsize=14, fontweight='bold',
                        fontname='Comic Sans MS')
            elif cell == 'H':
                ax.text(j, i, 'H', ha='center', va='center', color='black', fontsize=16, fontweight='bold',
                        fontname='Comic Sans MS')

    ax.set_xticks(np.arange(-.5, 8, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 6, 1), minor=True)
    ax.grid(which='minor', color='white', linestyle='--', linewidth=1)

    plt.pause(1)

def collect(room, x, y):
    """ Checks if the agent has collected an object at (x, y) and removes it from the room. """
    if room[x][y] == '*':
        room[x][y] = 0  # Remove the object after collecting
        return True
    return False

def valid_moves(x, y, room, visit_place, hurdle_stats):
    """Returns a list of valid moves from the current position, counting hurdles and extra moves."""
    moves = []
    if x > 0:  # Check move up
        if room[x - 1][y] != 'H' and (x - 1, y) not in visit_place:
            moves.append((x - 1, y))

    if x < 5:  # Check move down
        if room[x + 1][y] != 'H' and (x + 1, y) not in visit_place:
            moves.append((x + 1, y))

    if y > 0:  # Check move left
        if room[x][y - 1] != 'H' and (x, y - 1) not in visit_place:
            moves.append((x, y - 1))

    if y < 7:  # Check move right
        if room[x][y + 1] != 'H' and (x, y + 1) not in visit_place:
            moves.append((x, y + 1))

    return moves

def utility(x, y, target_x, target_y, room):
    """Calculate utility based on distance to the target and avoiding hurdles."""
    # Calculate Manhattan distance to the target
    distance = abs(x - target_x) + abs(y - target_y)

    # Check if there is a hurdle at the position
    if room[x][y] == 'H':
        return float('inf')  # High cost for hurdles (avoid)

    return distance  # Lower distance means higher utility (move closer to the target)

def move_towards_object(x, y, object_x, object_y, room, visit_place, hurdle_stats):
    """ Moves the agent towards the target object location, avoiding hurdles. """
    possible_moves = valid_moves(x, y, room, visit_place, hurdle_stats)

    if not possible_moves:
        return x, y

    # Choose the move with the highest utility (closest to the target)
    best_move = min(possible_moves, key=lambda move: utility(move[0], move[1], object_x, object_y, room))

    return best_move


def print_results(total_objects_collected, total_move_count, total_action_count,
                  total_collect_action_count, total_hurdles_confronted,
                  total_extra_moves_due_to_hurdles):
    print("Simulation Results:")
    print(f"Total Objects Collected: {total_objects_collected}")
    print(f"Total Moves Made: {total_move_count}")
    print(f"Total Actions Taken: {total_move_count+total_objects_collected}")
    print(f"Total Collect Actions: {total_collect_action_count}")
    print(f"Total Hurdles Confronted: {total_hurdles_confronted}")
    print(f"Total Extra Moves Due to Hurdles: {total_extra_moves_due_to_hurdles}")

def run_simulation():
    total_objects_collected = 0
    total_move_count = 0
    total_collect_action_count = 0
    total_action_count = 0
    total_hurdles_confronted = 0
    total_extra_moves_due_to_hurdles = 0

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect('equal')

    for step in range(3):
        print(f"Step {step + 1}:")
        objects_collected = 0
        move_count = 0
        collect_action_count = 0
        action_count = 0
        hurdle_stats = {'hurdles': 0, 'extra_moves': 0}

        room = create_environment()
        print_environment(room)

        x, y = start(room)
        print(f"Starting Position: ({x}, {y})")

        visit_place = set()
        visit_place.add((x, y))

        # Get all object positions at the beginning
        object_positions = [(i, j) for i in range(6) for j in range(8) if room[i][j] == '*']

        if not object_positions:
            print("No objects to collect. Stopping.")
            return

        # Randomly choose a target object
        target_x, target_y = random.choice(object_positions)
        print(f"Initial target object location: ({target_x}, {target_y})")

        # Check if the truck starts on a target object
        if (x, y) == (target_x, target_y):
            objects_collected += 1
            total_objects_collected += 1
            collect_action_count += 1
            object_positions.remove((x, y))
            print(f"Started on object and collected at ({x}, {y}).")
            if object_positions:
                target_x, target_y = random.choice(object_positions)
                print(f"New target object location: ({target_x}, {target_y})")
            else:
                print("No more objects to collect.")
                break

        while True:
            plot_room(room, x, y, visit_place, target_x, target_y, ax)

            if collect(room, x, y):
                objects_collected += 1
                total_objects_collected += 1
                collect_action_count += 1
                object_positions.remove((x, y))  # Remove collected object
                print(f"Collected object at ({x}, {y}).")

            if (x == 0 or x == 5 or y == 0 or y == 7):
                print(f"Reached boundary at position ({x}, {y}). Stopping.")
                break

            # Move towards the target object using utility-based decisions
            previous_x, previous_y = x, y
            x, y = move_towards_object(x, y, target_x, target_y, room, visit_place, hurdle_stats)

            # Increment move count only if the position changes
            if (x, y) != (previous_x, previous_y):
                move_count += 1
                print(f"Moved to position: ({x}, {y})")
                visit_place.add((x, y))
            else:
                print(f"Could not move from position: ({x}, {y}). No valid moves available.")
                break  # Exit if no valid moves

            if not object_positions:
                print("All objects collected. Stopping.")
                break

            # Update the target object if the current one is collected
            if (x, y) == (target_x, target_y) and object_positions:
                target_x, target_y = random.choice(object_positions)
                print(f"New target object location: ({target_x}, {target_y})")

        total_move_count += move_count
        total_collect_action_count += collect_action_count
        total_action_count += action_count
        total_hurdles_confronted += hurdle_stats['hurdles']
        total_extra_moves_due_to_hurdles += hurdle_stats['extra_moves']

    plt.show()

    print_results(
        total_objects_collected,
        total_move_count,
        total_action_count,
        total_collect_action_count,
        total_hurdles_confronted,
        total_extra_moves_due_to_hurdles
    )

    if total_objects_collected > 0:
        calculate_performance = (total_move_count+total_objects_collected) / total_objects_collected
        print(f"Efficiency: {calculate_performance}")
    else:
        print("No objects collected, cannot calculate efficiency.")


# Run the simulation
run_simulation()
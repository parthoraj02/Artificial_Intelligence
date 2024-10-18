import random


# Environment: The room with objects.
def generate_environment():
    environment = []
    for _ in range(5):
        row = [0] * 7
        environment.append(row)

    # Randomly place 5 objects ('1') in the room
    for _ in range(10):
        while True:
            x = random.randint(0, 4)
            y = random.randint(0, 6)
            if environment[x][y] == 0:
                environment[x][y] = '1'
                break

    return environment


# Sensor: Detect the starting position of the agent.
def agent_start():
    x_pos = random.randint(1, 4)
    y_pos = random.randint(1, 6)
    return x_pos, y_pos


# Environment: Display the environment and agent's position.
def display_environment(environment, agent_x, agent_y):
    for i, row in enumerate(environment):
        for j, cell in enumerate(row):
            if i == agent_x and j == agent_y:
                print("A", end=" ")  # A represents the agent
            else:
                print(cell if cell != 0 else '0', end=" ")
        print()
    print("\n")


# Actuators: Agent movement actions.
def move_up_direction(agent_x, agent_y):
    return agent_x - 1, agent_y


def move_down_direction(agent_x, agent_y):
    return agent_x + 1, agent_y


def move_left_direction(agent_x, agent_y):
    return agent_x, agent_y - 1


def move_right_direction(agent_x, agent_y):
    return agent_x, agent_y + 1


# Actuator: Choose a random direction and move the agent.
def move_agent(agent_x, agent_y, visited_positions):
    possible_directions = ['up', 'down', 'left', 'right']

    while possible_directions:
        direction = random.choice(possible_directions)

        if direction == 'up':
            new_x, new_y = move_up_direction(agent_x, agent_y)
        elif direction == 'down':
            new_x, new_y = move_down_direction(agent_x, agent_y)
        elif direction == 'left':
            new_x, new_y = move_left_direction(agent_x, agent_y)
        elif direction == 'right':
            new_x, new_y = move_right_direction(agent_x, agent_y)

        # Check if the new position is within bounds and not visited
        if (0 <= new_x < 5 and 0 <= new_y < 7) and (new_x, new_y) not in visited_positions:
            return new_x, new_y

        # Remove the invalid direction and try another
        possible_directions.remove(direction)

    # If all possible moves are invalid (all visited or out of bounds), return original position
    return agent_x, agent_y


# Sensor: Collect objects in the environment.
def grab_item(environment, agent_x, agent_y):
    if environment[agent_x][agent_y] == '1':
        environment[agent_x][agent_y] = 0
        return True
    return False


# Performance Measurement: Calculate agent performance based on actions.
def evaluate_performance(total_agent_actions, object_collection_actions):
    return total_agent_actions / object_collection_actions if object_collection_actions > 0 else 0


# Sensor: Check if the agent is at the boundary.
def check_boundary(agent_x, agent_y):
    return agent_x == 0 or agent_y == 0 or agent_x == 4 or agent_y == 6


# Performance: Display the simulation results.
def show_results(total_objects, total_movements, all_agent_actions, collection_actions, performance_result):
    print("===== Simulation Summary =====")
    print(f"Total Collected Objects: {total_objects}")
    print(f"Total Movements: {total_movements}")
    print(f"Total Agent Actions (Movements + Collections): {all_agent_actions}")
    print(f"Total Collection Actions: {collection_actions}")
    print(f"Performance (Actions / Collections): {performance_result:.2f}")
    print("===============================")


# Main Simulation Loop (Environment and Performance Measurement)
def run_agent_simulation():
    collected_items = 0
    moves_count = 0
    collection_count = 0
    total_actions_count = 0

    for round_num in range(100):  # Run for up to 100 steps
        print(f"--- Round {round_num + 1} ---")
        round_collected_items = 0
        current_moves = 0
        round_collections = 0
        round_actions = 0

        environment = generate_environment()
        agent_x, agent_y = agent_start()

        visited_positions = set()  # Track visited positions
        visited_positions.add((agent_x, agent_y))  # Mark starting point as visited
        agent_path = [(agent_x, agent_y)]  # Track the path of the agent

        while True:
            if grab_item(environment, agent_x, agent_y):  # Try to collect an object
                round_collected_items += 1
                collected_items += 1
                round_collections += 1

            display_environment(environment, agent_x, agent_y)  # Print the room with the agent's current position

            if check_boundary(agent_x, agent_y):  # Stop if the agent reaches the boundary
                print(f"Items collected in this round: {round_collected_items}")
                break

            new_x, new_y = move_agent(agent_x, agent_y, visited_positions)  # Move the agent
            round_actions += 1  # Every movement is an action

            # If the agent cannot move (all directions visited), stop the current round
            if (new_x, new_y) == (agent_x, agent_y):
                print("Agent has no valid moves left. Stopping this round.")
                break

            agent_x, agent_y = new_x, new_y  # Update the agent's position
            visited_positions.add((agent_x, agent_y))  # Mark the new position as visited
            current_moves += 1  # Count the move
            agent_path.append((agent_x, agent_y))  # Add the new position to the path

        # Print the path taken in this round
        print(f"Path taken in round {round_num + 1}: {agent_path}\n")

        # Update overall totals after each simulation
        moves_count += current_moves
        collection_count += round_collections
        total_actions_count += (current_moves + round_collections)  # Total actions = moves + collections

    # Performance Calculation
    final_performance = evaluate_performance(total_actions_count, collection_count)

    # Output Results
    print("\n--- Overall Simulation Results ---")
    show_results(collected_items, moves_count, total_actions_count, collection_count, final_performance)


run_agent_simulation()
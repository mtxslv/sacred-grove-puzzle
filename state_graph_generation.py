import networkx as nx

class StateGraphGenerator:

    opposite_directions = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E'
    }

    def __init__(self, graph, maximum_number_of_states: int = 7980):
        self.graph = graph
        self.maximum_number_of_states = maximum_number_of_states

    def get_available_tiles(self, current_tile, statue_shadow_position, statue_mirror_position) -> set[int]:
        """Wolf link can move to empty tiles

        Args:
            current_tile (int): where Wolf Link is currently standing.

        Returns:
            set[int]: a set of tile numbers that Wolf Link can move to.
        """
        neighbors = set(self.graph.neighbors(current_tile))
        available_tiles = neighbors - set([
            statue_shadow_position,
            statue_mirror_position
        ])
        return available_tiles      
    
    def will_link_move_to_invalid_position(self, new_link_position: int, new_shadow_statue_position: int, new_mirror_statue_position: int) -> bool:
        """Check if Wolf Link will move to a tile occupied by a statue after the move.

        Args:
            new_link_position (int): the tile number where Wolf Link will move to.
            new_shadow_statue_position (int): the tile number where the shadow statue will move to.
            new_mirror_statue_position (int): the tile number where the mirror statue will move to.
        Returns:
            bool: true if Wolf Link will be on the same tile as a statue after the move
        """
        return new_link_position in {new_shadow_statue_position, new_mirror_statue_position}
    
    def get_shadow_statue_new_position(self, statue_shadow_position: int, link_movement_direction: str, old_mirror_statue_position) -> int:
        """Calculate the new position of the shadow statue based on Wolf Link's movement direction.

        Args:
            statue_shadow_position (int): the current position of the shadow statue.
            link_movement_direction (str): the direction in which Wolf Link is moving ('N', 'S', 'E', 'W').

        Returns:
            int: the new tile number for the shadow statue, or its current position if it cannot move.
        """
        shadow_statue_new_position = next(
            iter(
                [n for n in self.graph.neighbors(statue_shadow_position) if self.graph.get_edge_data(statue_shadow_position, n).get('dir') == link_movement_direction]
            ),
            statue_shadow_position # If no valid move for the shadow statue, it stays in place
        )
        if shadow_statue_new_position == old_mirror_statue_position:
            # If the shadow statue tries to move to the tile where the mirror statue is, it cannot move and stays in place
            shadow_statue_new_position = statue_shadow_position
        return shadow_statue_new_position
    
    def get_mirror_statue_new_position(self, statue_mirror_position: int, link_movement_direction: str, old_shadow_statue_position: int) -> int:
        """Calculate the new position of the mirror statue based on Wolf Link's movement direction.

        Args:
            statue_mirror_position (int): the current position of the mirror statue.
            link_movement_direction (str): the direction in which Wolf Link is moving ('N', 'S', 'E', 'W').

        Returns:
            int: the new tile number for the mirror statue, or its current position if it cannot move.
        """
        mirror_statue_direction = self.opposite_directions[link_movement_direction]
        mirror_statue_new_position = next(
            iter(
                [n for n in self.graph.neighbors(statue_mirror_position) if self.graph.get_edge_data(statue_mirror_position, n).get('dir') == mirror_statue_direction]
            ), 
            statue_mirror_position
        ) # If no valid move for the mirror statue, it stays in place
        if mirror_statue_new_position == old_shadow_statue_position:
            # If the mirror statue tries to move to the tile where the shadow statue is, it cannot move and stays in place
            mirror_statue_new_position = statue_mirror_position
        return mirror_statue_new_position   

    def get_next_states(self, current_state: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        """Generate the next possible states based on the current state.

        Args:
            current_state (tuple[int, int, int]): a tuple representing the current positions of Wolf Link, the shadow statue, and the mirror statue.

        Returns:
            list[tuple[int, int, int]]: a list of tuples representing the next possible states.
        """
        wolf_link_position, shadow_statue_position, mirror_statue_position = current_state
        next_states = []
        for neighbor in self.get_available_tiles(wolf_link_position, shadow_statue_position, mirror_statue_position):
            movement_direction = self.graph.get_edge_data(wolf_link_position, neighbor).get('dir')
            new_shadow_statue_position = self.get_shadow_statue_new_position(shadow_statue_position, movement_direction, mirror_statue_position)
            new_mirror_statue_position = self.get_mirror_statue_new_position(mirror_statue_position, movement_direction, shadow_statue_position)
            if not self.will_link_move_to_invalid_position(neighbor, new_shadow_statue_position, new_mirror_statue_position):
                if new_shadow_statue_position != new_mirror_statue_position:
                    # If both statues end up on the same tile, they cannot occupy the same space and thus this state is invalid. 
                    # We add otherwise.
                    next_states.append((neighbor, new_shadow_statue_position, new_mirror_statue_position))
        return next_states

    def brute_force_state_graph_generation(self,
                                           wolf_link_position: int = 11,
                                           shadow_statue_position: int = 13,
                                           mirror_statue_position: int = 9):
        state_graph = nx.DiGraph()
        state = (wolf_link_position, shadow_statue_position, mirror_statue_position)
        states_to_visit_stack = [state]
        visited_states = set()
        while states_to_visit_stack:
            # Check if the current state has already been added to the state graph
            current_state = states_to_visit_stack.pop()
            if current_state in visited_states: 
            # if current_state in state_graph: 
                pass
            else:
                wolf_link_position, shadow_statue_position, mirror_statue_position = current_state
                visited_states.add(current_state)
                state_graph.add_node(
                    current_state, 
                    wolf_link_position=wolf_link_position, 
                    shadow_statue_position=shadow_statue_position, 
                    mirror_statue_position=mirror_statue_position
                )
                # Generate new states based on possible moves for Wolf Link
                # For each possible move for Wolf Link, calculate the new positions of the statues and create a new state tuple
                # This will lead to new possible states that can be added to the state graph
                # Add each new state to the states_to_visit_stack for further exploration
                # Also add edges to the state graph to represent the transitions between states based on Wolf Link's moves
                # This process will continue until all reachable states have been explored and added to the state graph
                next_states = self.get_next_states(current_state)
                for next_state in next_states:
                    # First we add the new node
                    state_graph.add_node(
                        next_state, 
                        wolf_link_position=next_state[0], 
                        shadow_statue_position=next_state[1], 
                        mirror_statue_position=next_state[2]
                    )
                    # Then we add the edge from the current state to the new state
                    state_graph.add_edge(current_state, next_state)
                    # At last, we add the new state to the stack to explore its neighbors later
                    states_to_visit_stack.append(next_state)
            if len(state_graph) >= self.maximum_number_of_states:
                print("Maximum number of states reached. Stopping state graph generation.")
                break
        return state_graph
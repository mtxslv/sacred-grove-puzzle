import random

from moving_characters import *


class Search:
    opposite_directions = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E'
    }

    def __init__(self, graph , wolf_link: MovingCharacter, statue_mirror: Statue, statue_shadow: Statue, maximum_steps: int = 25):
        self.graph = graph
        self.wolf_link = wolf_link
        self.statue_mirror = statue_mirror
        self.statue_shadow = statue_shadow
        self.maximum_steps = maximum_steps

    def get_available_tiles(self, current_tile) -> set[int]:
        """Wolf link can move to empty tiles

        Args:
            current_tile (int): where Wolf Link is currently standing.

        Returns:
            set[int]: a set of tile numbers that Wolf Link can move to.
        """
        neighbors = set(self.graph.neighbors(current_tile))
        available_tiles = neighbors - set([
            self.statue_shadow.position,
            self.statue_mirror.position
        ])
        return available_tiles
    
    def has_reached_goal(self,) -> bool:
        """Check if both statues are in the goal tiles.

        Returns:
            bool: true if goal reached, false otherwise.
        """
        positions = {self.statue_shadow.position, self.statue_mirror.position}
        return positions == {5, 15}
    
    def has_link_moved_to_invalid_position(self,) -> bool:
        """Check if Wolf Link has moved to a tile occupied by a statue.

        Returns:
            bool: true if Wolf Link is on the same tile as a statue, false otherwise.
        """
        return self.wolf_link.position in {self.statue_shadow.position, self.statue_mirror.position}
    
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
    
    def get_shadow_statue_new_position(self, link_movement_direction: str) -> int:
        """Calculate the new position of the shadow statue based on Wolf Link's movement direction.

        Args:
            link_movement_direction (str): the direction in which Wolf Link is moving ('N', 'S', 'E', 'W').

        Returns:
            int: the new tile number for the shadow statue, or its current position if it cannot move.
        """
        shadow_statue_new_position = next(
            iter(
                [n for n in self.graph.neighbors(self.statue_shadow.position) if self.graph.get_edge_data(self.statue_shadow.position, n).get('dir') == link_movement_direction]
            ),
            self.statue_shadow.position # If no valid move for the shadow statue, it stays in place
        )
        return shadow_statue_new_position
    
    def get_mirror_statue_new_position(self, link_movement_direction: str) -> int:
        """Calculate the new position of the mirror statue based on Wolf Link's movement direction.

        Args:
            link_movement_direction (str): the direction in which Wolf Link is moving ('N', 'S', 'E', 'W').

        Returns:
            int: the new tile number for the mirror statue, or its current position if it cannot move.
        """
        mirror_statue_direction = self.opposite_directions[link_movement_direction]
        mirror_statue_new_position = next(
            iter(
                [n for n in self.graph.neighbors(self.statue_mirror.position) if self.graph.get_edge_data(self.statue_mirror.position, n).get('dir') == mirror_statue_direction]
            ), 
            self.statue_mirror.position
        ) # If no valid move for the mirror statue, it stays in place
        return mirror_statue_new_position

    def move(self, new_link_position: int, mirror_statue_new_position: int, shadow_statue_new_position: int):
        """Move Wolf Link to a new tile and update the statues' positions according to their patterns.
        """
        # Move Statues to new positions 
        self.statue_mirror.move(mirror_statue_new_position)
        self.statue_shadow.move(shadow_statue_new_position)

        # Move Wolf Link to the new position
        self.wolf_link.move(new_link_position)

    def random_walk_search(self,):
        """Decide randomly where to search
        """
        steps = 0
        while True:
            where_can_link_go = self.get_available_tiles(self.wolf_link.position)
            if not where_can_link_go:
                print("No more available moves for Wolf Link. Search failed.")
                break
            else:
                # shuffle next possible tiles for link:
                shuffled_next_tiles = list(where_can_link_go)
                random.shuffle(shuffled_next_tiles)

                # Now, for each one, try if it is safe:
                for next_link_position in shuffled_next_tiles:
                    print(next_link_position)
                    link_movement_direction = self.graph.get_edge_data(self.wolf_link.position, next_link_position).get('dir')
                    shadow_statue_new_position = self.get_shadow_statue_new_position(link_movement_direction)
                    mirror_statue_new_position = self.get_mirror_statue_new_position(link_movement_direction)

                    print(f"Trying to move Wolf Link to {next_link_position} with direction {link_movement_direction}. Shadow Statue would move to {shadow_statue_new_position}, Mirror Statue would move to {mirror_statue_new_position}.")
                    if self.will_link_move_to_invalid_position(next_link_position, shadow_statue_new_position, mirror_statue_new_position):
                        print("Wolf Link moved to an invalid position. Search failed.")
                    else:
                        # go there
                        self.move(
                            next_link_position,
                            mirror_statue_new_position,
                            shadow_statue_new_position
                        )
                        # increase steps
                        steps += 1
                        break
            if self.has_reached_goal():
                print("Goal reached!")
                break
            if self.has_link_moved_to_invalid_position():
                break
            if steps >= self.maximum_steps:
                print("Maximum steps reached. Search failed.")
                break

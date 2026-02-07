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
    
    def move(self, new_link_position: int):
        """Move Wolf Link to a new tile and update the statues' positions according to their patterns.
        """
        link_movement_direction = self.graph.get_edge_data(self.wolf_link.position, new_link_position).get('dir')

        # Mirror statue moves to the tile opposite to Wolf Link's new position
        mirror_statue_direction = self.opposite_directions[link_movement_direction]
        mirror_statue_new_position = next(
            iter(
                [n for n in self.graph.neighbors(self.statue_mirror.position) if self.graph.get_edge_data(self.statue_mirror.position, n).get('dir') == mirror_statue_direction]
            ), self.statue_mirror.position
        ) # If no valid move for the mirror statue, it stays in place
        self.statue_mirror.move(mirror_statue_new_position)

        # Shadow statue moves to the tile in the same direction as Wolf Link's new position
        shadow_statue_new_position = next(
            iter(
                [n for n in self.graph.neighbors(self.statue_shadow.position) if self.graph.get_edge_data(self.statue_shadow.position, n).get('dir') == link_movement_direction]
            ),
            self.statue_shadow.position # If no valid move for the shadow statue, it stays in place
        )
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
                # choose randomly where to move
                next_link_position = random.choice(list(where_can_link_go))
                # go there
                self.move(next_link_position)
                # increase steps
                steps += 1
            if self.has_reached_goal():
                print("Goal reached!")
                break
            if self.has_link_moved_to_invalid_position():
                print("Wolf Link moved to an invalid position. Search failed.")
                break
            if steps >= self.maximum_steps:
                print("Maximum steps reached. Search failed.")
                break

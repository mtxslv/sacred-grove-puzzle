from dataclasses import dataclass, field

@dataclass
class MovingCharacter:
    position: int
    history: list[int] = field(default_factory=list)

    def move(self, new_position: int) -> None:
        self.history.append(self.position)
        self.position = new_position

@dataclass
class WolfLink(MovingCharacter):
    ... # no additional attributes for now

@dataclass
class Statue(MovingCharacter):
    # pattern should be one of 'shadow' or 'mirror'
    pattern: str = field(default='')
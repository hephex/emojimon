from collections import namedtuple
from typing import List, Union, Tuple
from dataclasses import dataclass
import abc

__all__ = ["Emojimon", "Character", "GoTo", "Catch", "Action"]


@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int


@dataclass
class Creature(abc.ABC):

    id: str

    @abc.abstractclassmethod
    def emoji(cls):
        raise NotImplementedError


@dataclass
class Flyer(Creature, abc.ABC):
    pass


@dataclass
class Swimmer(Creature, abc.ABC):
    pass


@dataclass
class Runner(Creature, abc.ABC):
    pass


@dataclass
class Bird(Flyer):
    @classmethod
    def emoji(cls):
        return "🐦"


@dataclass
class Shark(Swimmer):
    @classmethod
    def emoji(cls):
        return "🦈"


@dataclass
class Lion(Runner):
    @classmethod
    def emoji(cls):
        return "🦁"


@dataclass
class Player:
    username: str
    emoji: str


Item = Union[None, Creature, Player]


@dataclass
class Map:

    size: int


@dataclass
class GoTo:

    username: str
    from_: Position
    to: Position


@dataclass
class Catch:

    from_: Position
    to: Position
    username: str
    creature_id: str


Action = Union[GoTo, Catch]

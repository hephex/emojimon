import collections
from typing import Generator, List, Dict
from emojimon.types import Map, Action, Creature, Player, Position, GoTo, Catch
from dataclasses import dataclass, replace
from functools import singledispatch
import copy

__all__ = ["Engine", "generate_world", "State"]


class InvalidMove(Exception):
    """
    Raised when a player tries to perform an invalid move i.e. move to a cell too far away.
    """


@dataclass
class State:
    """
    Represents the state of the 
    """

    map: Map
    creatures: Dict[Position, Creature]
    players: Dict[Position, Player]
    collections: Dict[str, List[Creature]]


def is_nearby(pos_a: Position, pos_b: Position) -> bool:
    """
    Returns `True` if the position are adjacent. Otherwise, `False`.
    """
    return abs(pos_a.x - pos_b.x) <= 1 and abs(pos_a.y - pos_b.y) <= 1


@singledispatch
def perform_action(action: Action, current: State) -> State:
    """
    Calculates the next state when applying the given action to the current state.
    """
    raise TypeError(f"unexpected action type: {action!r}")


@perform_action.register
def perform_action_goto(action: GoTo, state: State) -> State:
    """
    Calculates the next state after moving a player around.

    Raises an `InvalidMove` if the player is trying to move to a position
    too far away or from a position different from its current one.
    """
    player = state.players.get(action.from_)

    is_valid = (
        player is not None
        and player.username == action.username
        and is_nearby(action.from_, action.to)
    )

    if not is_valid:
        raise InvalidMove("player is not at the specified position")

    new_players = copy.deepcopy(state.players)
    del new_players[action.from_]

    if player:
        new_players[action.to] = player

    return replace(state, players=new_players)


@perform_action.register
def perform_action_catch(action: Catch, state: State) -> State:
    """
    Calculates the next state after catching a creature.

    Raises an `InvalidMove` if:
        * the player is trying to catch a creature too far away
        * the player is trying to catch from a position different from its current one
        * the player is trying to catch an animal that does not exist
    """
    player = state.players.get(action.from_)
    creature = state.creatures.get(action.to)

    is_valid = (
        player is not None
        and player.username == action.username
        and creature is not None
        and creature.id == action.creature_id
        and is_nearby(action.from_, action.to)
    )

    if not is_valid:
        raise InvalidMove("player/creature is not at the specified position")

    new_creatures = copy.deepcopy(state.creatures)
    del new_creatures[action.to]

    new_collections = copy.deepcopy(state.collections)
    player_collection: List[Creature] = new_collections.get(player.username, [])

    player_collection.append(creature)

    new_collections[player.username] = player_collection

    return replace(state, creatures=new_creatures, collections=new_collections)


class Engine:
    """
    The Engine is responsible for keeping track of the current state and perform
    any move requested by the player.
    """

    def __init__(self, init: State):
        self.state = init

    def perform(self, action):
        """
        Applies the given action to the current state.
        """
        self.state = perform_action(action, self.state)

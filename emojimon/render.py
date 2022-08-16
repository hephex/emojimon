from emojimon.engine import State
from emojimon.types import Position
import os


__all__ = ["render"]


def render(state: State):
    size = state.map.size
    sep = "+----" * size + "+"

    os.system("clear")

    print(sep)

    for row in range(size):
        display_row = []
        display_row.append("|")

        for col in range(size):
            player = state.players.get(Position(x=col, y=row))
            display_row.append(player.emoji if player else " ")

            display_row.append(" ")

            creature = state.creatures.get(Position(x=col, y=row))
            display_row.append(creature.emoji() if creature else "  ")

            display_row.append("|")

        print("".join(display_row))
        print(sep)

    for (username, collection) in state.collections.items():
        print(username, "->", " ".join(creature.emoji() for creature in collection))

    print("\n")
    print("\n")

# Emojimon

Gotta catch them all.

## Setup

1. [install poetry](https://python-poetry.org/docs/)
2. install all dependencies `$ poetry install`

## How to run...

### ... the game

The main function has some hardcoded inputs you can use to see the game being played
or test different actions. To run the game execture:

```bash
$ poetry run play
+----+----+----+
|  🦁|    |    |
+----+----+----+
|  🦈|🕵️   |    |
+----+----+----+
|    |    |  🐦|
+----+----+----+

...
```

### ... the tests

There are some unit tests to check the basic functionalities of the game.
You can run them with:

```bash
$ poetry run pytest --cov=emojimo

======================================================================================================== test session starts ========================================================================================================
platform linux -- Python 3.7.4, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/federico.figus/git/src/github.com/hephex/emojimon
plugins: cov-3.0.0
collected 31 items                                                                                                                                                                                                                  

tests/test_engine.py ...............................                                                                                                                                                                          [100%]

----------- coverage: platform linux, python 3.7.4-final-0 -----------
Name                   Stmts   Miss  Cover
------------------------------------------
emojimon/__init__.py      16     12    25%
emojimon/engine.py        48      2    96%
emojimon/render.py        25     20    20%
emojimon/types.py         50      4    92%
------------------------------------------
TOTAL                    139     38    73%
```

### ... linters & co.

* [black](https://github.com/psf/black): `poetry run black`
* [mypy](http://mypy-lang.org/): `poetry run mypy`

## Assumptions

* _maps are always squares_. It makes my life easier :)
* _there's only one player in the map_. This is easy to extend transforming the dictionaries in the class `State` be map `Positon` to `List[Player]`.
* _there's only one creature in each cell_. This is easy to extend transforming the dictionary in the State class to map `Positon` to `List[Creature]`.
* _a player and a creature can be in the same cell_. If we want to avoid this we can add a check in `perform_action_goto` to raise an error if the cell is already taken.
* _the position coordinates are within the grid_. If we want to avoid bad input we cann add some checks beforehand, but it would be easier to do if the input source was known (i.e. stdin)
* _a cell is adjacent to another if the x and y coordinates are a most one far from each other_. In the image below, all the cells with `AA` are adjacent to the cell containing `XX`.

    ```text
    +----+----+----+----+----+
    |    |    |    |    |    |
    +----+----+----+----+----+
    |    | AA | AA | AA |    |
    +----+----+----+----+----+
    |    | AA | XX | AA |    |
    +----+----+----+----+----+
    |    | AA | AA | AA |    |
    +----+----+----+----+----+
    |    |    |    |    |    |
    +----+----+----+----+----+
    ```

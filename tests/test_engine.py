from testfixtures import compare
from emojimon import engine, types
import pytest
import dataclasses

DUMMY_CREATURE_POSITION = {
    types.Position(x=0, y=0): types.Lion(id="lion"),
    types.Position(x=0, y=1): types.Shark(id="shark"),
    types.Position(x=2, y=2): types.Bird(id="bird"),
}


def test_is_nearby__should_return_true_if_positions_are_the_same():
    assert engine.is_nearby(types.Position(x=0, y=0), types.Position(x=0, y=0))


@pytest.mark.parametrize(
    ["pos_a", "pos_b"],
    [
        pytest.param(types.Position(x=0, y=0), types.Position(x=0, y=0), id="top left"),
        pytest.param(types.Position(x=1, y=0), types.Position(x=1, y=0), id="top"),
        pytest.param(
            types.Position(x=2, y=0), types.Position(x=2, y=0), id="top right"
        ),
        pytest.param(types.Position(x=0, y=1), types.Position(x=0, y=1), id="left"),
        pytest.param(types.Position(x=2, y=1), types.Position(x=2, y=1), id="tight"),
        pytest.param(
            types.Position(x=0, y=2), types.Position(x=0, y=2), id="bottom left"
        ),
        pytest.param(types.Position(x=1, y=2), types.Position(x=1, y=2), id="bottom"),
        pytest.param(
            types.Position(x=2, y=2), types.Position(x=2, y=2), id="bottom right"
        ),
    ],
)
def test_is_nearby__should_return_true_if_positions_are_adjacent(pos_a, pos_b):
    assert engine.is_nearby(pos_a, pos_b)


@pytest.mark.parametrize(
    ["pos_a", "pos_b"],
    [
        pytest.param(types.Position(x=0, y=0), types.Position(x=2, y=2)),
        pytest.param(types.Position(x=1, y=0), types.Position(x=1, y=2)),
        pytest.param(types.Position(x=0, y=1), types.Position(x=2, y=1)),
    ],
)
def test_is_nearby__should_return_true_if_positions_not_adjacent(pos_a, pos_b):
    assert not engine.is_nearby(pos_a, pos_b)


def test_Engine_perform_move__should_not_change_state_when_destination_is_in_same_position():
    init_state = engine.State(
        map=types.Map(size=3),
        creatures=DUMMY_CREATURE_POSITION,
        players={types.Position(x=1, y=1): types.Player(username="john", emoji="🕵️")},
        collections={},
    )
    eng = engine.Engine(init=init_state)

    eng.perform(
        types.GoTo(username="john", from_=types.Position(1, 1), to=types.Position(1, 1))
    )

    compare(eng.state, init_state)


@pytest.mark.parametrize(
    ["next_position"],
    [
        pytest.param(types.Position(x=0, y=0), id="move up left"),
        pytest.param(types.Position(x=1, y=0), id="move up"),
        pytest.param(types.Position(x=2, y=0), id="move up right"),
        pytest.param(types.Position(x=0, y=1), id="move left"),
        pytest.param(types.Position(x=2, y=1), id="move right"),
        pytest.param(types.Position(x=0, y=2), id="move down left"),
        pytest.param(types.Position(x=1, y=2), id="move down"),
        pytest.param(types.Position(x=2, y=2), id="move down right"),
    ],
)
def test_Engine_perform_move__move_to_the_give_position(next_position):
    player = types.Player(username="john", emoji="🕵️")
    init_state = engine.State(
        map=types.Map(size=3),
        creatures=DUMMY_CREATURE_POSITION,
        players={types.Position(x=1, y=1): player},
        collections={},
    )
    eng = engine.Engine(init=init_state)

    eng.perform(
        types.GoTo(username="john", from_=types.Position(1, 1), to=next_position)
    )

    compare(eng.state, dataclasses.replace(init_state, players={next_position: player}))


@pytest.mark.parametrize(
    ["goto"],
    [
        pytest.param(
            types.GoTo(
                username="john", from_=types.Position(2, 2), to=types.Position(1, 1)
            ),
            id="move non nearby cell",
        ),
        pytest.param(
            types.GoTo(
                username="jane", from_=types.Position(1, 1), to=types.Position(1, 1)
            ),
            id="move invalid user",
        ),
    ],
)
def test_Engine_perform_move__should_raise_an_exception_when_moving_to_wrong_position(
    goto
):
    init_state = engine.State(
        map=types.Map(size=3),
        creatures=DUMMY_CREATURE_POSITION,
        players={types.Position(x=0, y=0): types.Player(username="john", emoji="🕵️")},
        collections={},
    )
    eng = engine.Engine(init=init_state)

    with pytest.raises(engine.InvalidMove):
        eng.perform(goto)


@pytest.mark.parametrize(
    ["catch_position"],
    [
        pytest.param(types.Position(x=0, y=0), id="catch up left"),
        pytest.param(types.Position(x=1, y=0), id="catch up"),
        pytest.param(types.Position(x=2, y=0), id="catch up right"),
        pytest.param(types.Position(x=0, y=1), id="catch left"),
        pytest.param(types.Position(x=2, y=1), id="catch right"),
        pytest.param(types.Position(x=0, y=2), id="catch down left"),
        pytest.param(types.Position(x=1, y=2), id="catch down"),
        pytest.param(types.Position(x=2, y=2), id="catch down right"),
    ],
)
def test_Engine_perform_move__catch_creature_in_the_given_position(catch_position):
    player = types.Player(username="john", emoji="🕵️")
    lion = types.Lion(id="lion")
    init_state = engine.State(
        map=types.Map(size=3),
        creatures={catch_position: lion},
        players={types.Position(x=1, y=1): player},
        collections={},
    )
    eng = engine.Engine(init=init_state)

    eng.perform(
        types.Catch(
            username="john",
            from_=types.Position(1, 1),
            to=catch_position,
            creature_id="lion",
        )
    )

    compare(
        eng.state,
        dataclasses.replace(init_state, creatures={}, collections={"john": [lion]}),
    )

from emojimon import engine, types, render
import time


def generate_world() -> engine.State:
    return engine.State(
        map=types.Map(size=3),
        creatures={
            types.Position(x=0, y=0): types.Lion(id="lion"),
            types.Position(x=0, y=1): types.Shark(id="shark"),
            types.Position(x=2, y=2): types.Bird(id="bird"),
        },
        players={types.Position(x=1, y=1): types.Player(username="john", emoji="🕵️")},
        collections={},
    )


def main():
    init = generate_world()
    eng = engine.Engine(init)

    actions = [
        types.GoTo(
            username="john", from_=types.Position(1, 1), to=types.Position(0, 1)
        ),
        types.Catch(
            username="john",
            creature_id="shark",
            from_=types.Position(0, 1),
            to=types.Position(0, 1),
        ),
        types.Catch(
            username="john",
            creature_id="lion",
            from_=types.Position(0, 1),
            to=types.Position(0, 0),
        ),
        types.GoTo(
            username="john", from_=types.Position(0, 1), to=types.Position(0, 2)
        ),
        types.GoTo(
            username="john", from_=types.Position(0, 2), to=types.Position(1, 2)
        ),
        types.Catch(
            username="john",
            creature_id="bird",
            from_=types.Position(1, 2),
            to=types.Position(2, 2),
        ),
    ]

    render.render(init)
    time.sleep(1)

    for action in actions:
        eng.perform(action)
        render.render(eng.state)
        time.sleep(1)

    print("== GAME OVER ==")
    print()

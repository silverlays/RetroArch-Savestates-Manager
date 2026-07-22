from pathlib import Path

from PySide6.QtCore import QObject, Signal

from settings import settings


class State:
    number: int
    path: Path
    image_path: Path | None

    def __init__(self, number: int, path: Path):
        self.number = number
        self.path = path

        image_path = Path(str(f"{path}.png"))
        self.image_path = image_path if image_path.exists() else None


class Game:
    states: list[State]
    name: str

    def __init__(
        self, name: str, number: int | None = None, state_path: Path | None = None
    ):
        self.states = []
        self.name = name
        if number is not None and state_path is not None:
            self.add_state(State(number, state_path))

    def add_state(self, state: State):
        if not any(s.number == state.number for s in self.states):
            self.states.append(state)


class Manager(QObject):
    games: list[Game]
    update_needed = Signal()

    def __init__(self):
        super().__init__()
        self.games = []

        if settings.states_path:
            states = settings.states_path.rglob("*.state*")

            for state_path in states:
                if state_path.suffix == ".auto":
                    game_name = state_path.stem.split(state_path.suffix[0])[0]
                    state_number = -1
                elif state_path.suffix == ".state":
                    game_name = state_path.stem
                    state_number = 0
                else:
                    game_name = state_path.stem
                    state_number = int(state_path.suffix.split(".state")[1])

                game = self.get_game(game_name)
                if not game:
                    self.games.append(Game(game_name, state_number, state_path))
                else:
                    game.add_state(State(state_number, state_path))

            self.games.sort(key=lambda k: k.name)

    def delete_state(self, name: str, state_number: int):
        # TODO Finish this
        if game := self.get_game(name):
            if state := self.get_state(name, state_number):
                game.states.remove(state)
                if len(game.states) == 0:
                    self.games.remove(game)
            self.update_needed.emit()

    def get_states(self, name: str) -> list[State]:
        if game := self.get_game(name):
            return game.states
        else:
            return []

    def get_states_count(self, name: str) -> int:
        if game := self.get_game(name):
            return len(game.states)
        else:
            return 0

    def get_game(self, name: str) -> Game | None:
        return next((g for g in self.games if g.name == name), None)

    def get_state(self, name: str, state_number: int) -> State | None:
        if game := self.get_game(name):
            return next((s for s in game.states if s.number == state_number), None)
        return None

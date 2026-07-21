from pathlib import Path

from settings import settings


class State:
    number: int
    path: Path

    def __init__(self, number: int, path: Path):
        self.number = number
        self.path = path


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


class Manager:
    games: list[Game]

    def __init__(self):
        self.games = []

    def add_game(
        self, name: str, state_number: int | None = None, state_path: Path | None = None
    ):
        if not any(game.name == name for game in self.games):
            if state_number and state_path:
                self.games.append(Game(name, state_number, state_path))
            else:
                self.games.append(Game(name))

    def games_string(self):
        for game in self.games:
            yield game.name

    def get_states(self, name: str) -> list[State]:
        if any(n.name == name for n in self.games):
            game = [g for g in self.games if g.name == name][0]
            return game.states
        else:
            return []

    def get_states_count(self, name: str) -> int:
        if any(n.name == name for n in self.games):
            game = [g for g in self.games if g.name == name][0]
            return len(game.states)
        else:
            return 0

    def get_game_card(self, name: str) -> dict[str, list[str]]:
        card = {}
        game = [g for g in self.games if g.name == name][0]

        card["name"] = game.name
        card["states"] = []
        for state in game.states:
            state_text = "Auto" if state.number == -1 else str(state.number)
            card["states"].append(state_text)

        return card

    @classmethod
    def load(cls):
        cls = cls()
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

                if not any(g.name == game_name for g in cls.games):
                    cls.games.append(Game(game_name, state_number, state_path))
                else:
                    game = [g for g in cls.games if g.name == game_name][0]
                    game.add_state(State(state_number, state_path))

            cls.games.sort(key=lambda k: k.name)
        return cls


manager = Manager.load()

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt, QObject, Signal
from PySide6.QtGui import QPixmap, QImage, QColor, QPainter, QFont

from settings import settings


# region State
@dataclass
class State:
    number: int
    pixmap: QPixmap
    state_path: Path

    @staticmethod
    def create_pixmap(path: Path | None = None) -> QPixmap:
        if path and path.exists():
            return QPixmap(QImage(path).scaledToHeight(240))
        else:
            pixmap = QPixmap(426, 240)
            pixmap.fill(QColor("#2b2b2b"))

            painter = QPainter(pixmap)
            painter.setPen(QColor("#888888"))
            painter.setFont(QFont("Arial", 10))
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "No Image")
            painter.end()

            return pixmap


# endregion


# region Game
class Game:
    states: list[State]
    name: str

    def __init__(self, name: str, number: int, pixmap: QPixmap, state_path: Path):
        self.states = []
        self.name = name
        self.add_state(State(number, pixmap, state_path))

    def add_state(self, state: State):
        if existing_state := next(
            (s for s in self.states if s.number == state.number), None
        ):
            existing_state.pixmap = state.pixmap
        else:
            self.states.append(state)


# endregion


# region Manager
class Manager(QObject):
    games: list[Game]
    update_needed = Signal()

    def __init__(self):
        super().__init__()
        self.games = []

        if settings.states_path:
            states = settings.states_path.rglob("*.state*")

            for path in states:
                game_name, state_number, pixmap = self._extract_from_path(path)
                game = self.get_game(game_name)

                if not game:
                    self.games.append(Game(game_name, state_number, pixmap, path))
                else:
                    game.add_state(State(state_number, pixmap, path))

            self.games.sort(key=lambda k: k.name)

    def delete_state(self, name: str, state_number: int):
        # TODO delete_state() Implement real delete
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

    def move_slot(self, name: str, state_number: int, new_slot_number: int):
        # TODO move_slot() Implement real slot change
        if game := self.get_game(name):
            if state := self.get_state(name, state_number):
                pixmap = state.pixmap
                state_path = state.state_path

                if not next(
                    (s for s in game.states if s.number == new_slot_number), None
                ):
                    # FIXME Handle pixmap switch
                    game.states.remove(state)
                    game.add_state(State(new_slot_number, pixmap, state_path))

        self.update_needed.emit()

    def _extract_from_path(self, path: Path):
        if path.suffix == ".png":
            emulator = path.parts[-2]
            game_name = path.stem.split(path.suffix[0])[0]
            state_number = int(path.suffixes[0].split(".state")[1])
            pixmap = State.create_pixmap(path)
        elif path.suffix == ".auto":
            emulator = path.parts[-2]
            game_name = path.stem.split(path.suffix[0])[0]
            state_number = -1
            pixmap = State.create_pixmap()
        elif path.suffix == ".state":
            emulator = path.parts[-2]
            game_name = path.stem
            state_number = 0
            pixmap = State.create_pixmap()
        else:
            emulator = path.parts[-2]
            game_name = path.stem
            state_number = int(path.suffix.split(".state")[1])
            pixmap = State.create_pixmap()

        return (f"{game_name} -- {emulator}", state_number, pixmap)


# endregion

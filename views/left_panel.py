from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGroupBox,
    QListWidget,
    QVBoxLayout,
)

from manager import Game


# region GameList
class GameList(QListWidget):
    game_selection_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("game_list_widget")
        self.game_list = []

        self.currentTextChanged.connect(self.game_selection_changed)

    def refresh(self, game_list: list[Game]):
        self.clear()

        for game in game_list:
            self.addItem(game.name)

        needed_width = self.sizeHintForColumn(0)
        needed_width += self.frameWidth() * 2
        needed_width += 20
        self.setMinimumWidth(needed_width)


# endregion


# region LeftPanel
class LeftPanel(QGroupBox):
    list_widget: GameList

    def __init__(self):
        super().__init__()

        self.setTitle("1. Select a game")

        layout = QVBoxLayout(self)

        self.list_widget = GameList()
        layout.addWidget(self.list_widget)


# endregion

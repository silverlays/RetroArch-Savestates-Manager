from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QGroupBox,
    QListWidget,
    QVBoxLayout,
)

from manager import manager


class GameList(QListWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("game_list_widget")

        for game in manager.games_string():
            self.addItem(game)

        needed_width = self.sizeHintForColumn(0)
        needed_width += self.frameWidth() * 2
        needed_width += 20
        self.setMinimumWidth(needed_width)


class LeftPanel(QGroupBox):
    update_right_panel = Signal(str)

    def __init__(self):
        super().__init__()

        self.setTitle("1. Select a game")

        layout = QVBoxLayout(self)

        self.list_widget = GameList()
        self.list_widget.currentTextChanged.connect(self.update_right_panel.emit)
        layout.addWidget(self.list_widget)

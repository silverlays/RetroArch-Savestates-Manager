from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QFont, QWheelEvent
from PySide6.QtWidgets import (
    QGroupBox,
    QFrame,
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)

from manager import Game, State


class StateCard(QFrame):
    game_name: str
    state_number: int
    pixmap: QPixmap | None

    state_number_label: QLabel
    picture_label: QLabel
    delete_button: QPushButton

    delete_state = Signal(str, int)

    def __init__(self, game_name: str, state: State, pixmap: QPixmap):
        super().__init__()

        self.game_name = game_name
        self.state_number = state.number
        self.pixmap = pixmap

        layout = QVBoxLayout(self)

        self.setObjectName("state_frame")

        self.state_number_label = QLabel(
            f"Savestate: <b>{"Auto" if self.state_number == -1 else str(self.state_number)}</b>"
        )
        self.state_number_label.setObjectName("state_number_label")
        self.state_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_number_label.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum
        )
        layout.addWidget(self.state_number_label)

        self.picture_label = QLabel()
        self.picture_label.setObjectName("picture_label")
        self.picture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.picture_label.setContentsMargins(0, 10, 0, 10)
        self.picture_label.setPixmap(self.pixmap)
        layout.addWidget(self.picture_label)

        self.delete_button = QPushButton("🗑️ DELETE")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.clicked.connect(
            lambda: self.delete_state.emit(self.game_name, self.state_number)
        )
        layout.addWidget(self.delete_button)


class CardsContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.widget_layout = QHBoxLayout(self)

    def add_state(self, name: str, state: State) -> StateCard:
        pixmap = (
            QPixmap.fromImage(QImage(str(state.image_path)))
            if state.image_path
            else self.create_placeholder_pixmap()
        )
        card = StateCard(name, state, pixmap)
        self.widget_layout.addWidget(card)

        return card

    def create_placeholder_pixmap(self) -> QPixmap:
        pixmap = QPixmap(320, 240)
        pixmap.fill(QColor("#2b2b2b"))

        painter = QPainter(pixmap)
        painter.setPen(QColor("#888888"))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "No Image")
        painter.end()

        return pixmap


class RightPanel(QGroupBox):
    game: Game

    cards_container: CardsContainer
    scroll_area: QScrollArea
    game_label: QLabel

    delete_requested = Signal(str, int)

    def __init__(self):
        super().__init__()

        self.setTitle("2. Savestate operation")

        layout = QVBoxLayout(self)

        self.game_label = QLabel()
        self.game_label.setObjectName("game_label")
        layout.addWidget(self.game_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setFixedWidth(800)
        self.scroll_area.wheelEvent = self.scroll_area_wheelEvent
        layout.addWidget(self.scroll_area)

    def clear_container(self):
        self.game_label.setText("")
        if widget := self.scroll_area.widget():
            widget.deleteLater()

    @Slot(Game)
    def update_cards(self, game: Game):
        self.clear_container()
        self.game = game
        self.game_label.setText(game.name)
        self.cards_container = CardsContainer()

        for state in game.states:
            card = self.cards_container.add_state(game.name, state)
            card.delete_state.connect(self.delete_requested.emit)

        self.scroll_area.setWidget(self.cards_container)

    def scroll_area_wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        if delta != 0:
            scroll_bar = self.scroll_area.horizontalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - delta)
            event.accept()
        else:
            super().wheelEvent(event)

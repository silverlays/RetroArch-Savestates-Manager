from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap, QWheelEvent
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
    QCheckBox,
)

from views.change_slot_dialog import ChangeSlotDialog

from manager import Game, State


# region StateCard
class StateCard(QFrame):
    game_name: str
    state_number: int
    pixmap: QPixmap | None

    state_number_label: QLabel
    picture_label: QLabel
    delete_button: QPushButton
    change_slot_button: QPushButton

    change_slot = Signal(str, int, int)  # name, state_number, new_slot_number
    delete_state = Signal(str, int)  # name, state_number

    def __init__(self, game_name: str, state: State):
        super().__init__()

        self.game_name = game_name
        self.state_number = state.number
        self.pixmap = state.pixmap

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

        # Picture (Pixmap) Label
        self.picture_label = QLabel()
        self.picture_label.setObjectName("picture_label")
        self.picture_label.setContentsMargins(0, 10, 0, 10)
        self.picture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.picture_label.setPixmap(self.pixmap)
        layout.addWidget(self.picture_label)

        # Change Slot Button
        self.change_slot_button = QPushButton("🔄 CHANGE SLOT")
        self.change_slot_button.setObjectName("change_slot_button")
        self.change_slot_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.change_slot_button.clicked.connect(self.on_change_slot_button_clicked)
        layout.addWidget(self.change_slot_button)

        # Delete Button
        self.delete_button = QPushButton("🗑️ DELETE")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_button.clicked.connect(
            lambda: self.delete_state.emit(self.game_name, self.state_number)
        )
        layout.addWidget(self.delete_button)

    @Slot()
    def on_change_slot_button_clicked(self):
        dialog = ChangeSlotDialog(self.state_number, self)
        if dialog.exec() == ChangeSlotDialog.DialogCode.Accepted:
            new_slot = (
                -1
                if dialog.new_slot_combobox.currentText() == "Auto"
                else int(dialog.new_slot_combobox.currentText())
            )
            self.change_slot.emit(self.game_name, self.state_number, new_slot)


# endregion


# region CardsContainer
class CardsContainer(QWidget):
    def __init__(self):
        super().__init__()

        self.widget_layout = QHBoxLayout(self)

    def add_state(self, name: str, state: State) -> StateCard:
        card = StateCard(name, state)
        self.widget_layout.addWidget(card)

        return card


# endregion


# region RightPanel
class RightPanel(QGroupBox):
    game: Game
    cards_container: CardsContainer

    game_label: QLabel
    scroll_area: QScrollArea
    delete_confirmation: QCheckBox

    change_slot_requested = Signal(str, int, int)  # name, state_number, new_slot_number
    delete_requested = Signal(str, int)  # name, state_number

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
        self.scroll_area.setFixedWidth(1000)
        self.scroll_area.wheelEvent = self.scroll_area_wheelEvent
        layout.addWidget(self.scroll_area)

        self.delete_confirmation = QCheckBox("Ask confirmation before delete")
        layout.addWidget(self.delete_confirmation)

    def clear_container(self):
        self.game_label.setText("")
        if widget := self.scroll_area.widget():
            widget.deleteLater()

    @Slot(Game)
    def update_cards(self, game: Game):
        self.clear_container()
        self.game = game
        self.game_label.setText(
            f"<span style='background-color: #2D2D2D; color: #AAAAAA; padding: 2px 8px; border-radius: 4px; font-size: 0.9em;'>{game.emulator}</span> {game.name}"
        )
        self.cards_container = CardsContainer()

        for state in game.states:
            card = self.cards_container.add_state(game.name, state)
            card.change_slot.connect(self.change_slot_requested.emit)
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


# endRegion

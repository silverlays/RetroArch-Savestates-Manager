from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QWheelEvent
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

from manager import manager


class StateFrame(QFrame):
    state_number_label: QLabel
    picture_label: QLabel
    delete_button: QPushButton

    def __init__(self, state_number: int):
        super().__init__()

        self.state_number = state_number
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
        self.picture_label.setPixmap(self.create_placeholder_pixmap())
        layout.addWidget(self.picture_label)

        self.delete_button = QPushButton("🗑️ DELETE")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.delete_button)

    def create_placeholder_pixmap(self) -> QPixmap:
        pixmap = QPixmap(320, 240)
        pixmap.fill(QColor("#2b2b2b"))

        painter = QPainter(pixmap)
        painter.setPen(QColor("#888888"))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "No Image")
        painter.end()

        return pixmap


class StatesContainer(QScrollArea):
    state_frames: list[QFrame]
    update_container = Signal(str)

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedWidth(800)

        self.state_frames = []
        self.container_widget = QWidget()
        self.container_layout = QHBoxLayout(self.container_widget)
        self.setWidget(self.container_widget)

        self.update_container.connect(self.on_update_container_triggered)

    @Slot(str)
    def on_update_container_triggered(self, name: str):
        for frame in self.state_frames:
            self.container_layout.removeWidget(frame)
            frame.deleteLater()

        self.state_frames.clear()
        layout = QHBoxLayout()

        for state in manager.get_states(name):
            state_frame = StateFrame(state.number)
            self.state_frames.append(state_frame)
            self.container_layout.addWidget(state_frame)

    def wheelEvent(self, event: QWheelEvent) -> None:
        delta = event.angleDelta().y()
        if delta != 0:
            scroll_bar = self.horizontalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - delta)
            event.accept()
        else:
            super().wheelEvent(event)


class RightPanel(QGroupBox):
    states_container: StatesContainer

    def __init__(self):
        super().__init__()

        self.setTitle("2. Savestate operation")

        layout = QVBoxLayout(self)

        self.game_label = QLabel()
        self.game_label.setObjectName("game_label")
        layout.addWidget(self.game_label)

        self.states_container = StatesContainer()
        layout.addWidget(self.states_container)

    @Slot(str)
    def on_updated_game(self, name: str):
        self.game_label.setText(name)
        self.states_container.update_container.emit(name)

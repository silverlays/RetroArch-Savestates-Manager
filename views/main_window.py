from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QVBoxLayout, QMessageBox

from views.left_panel import LeftPanel
from views.right_panel import RightPanel

import constants as c
from manager import Manager
from settings import settings


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.manager = Manager()
        layout = QVBoxLayout(self)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()

        # Window Properties
        self.setWindowTitle(f"{c.APP_NAME} v{c.APP_VERSION[0]}.{c.APP_VERSION[1]}")
        self.setMinimumHeight(550)

        # Left Panel
        self.left_panel.list_widget.refresh(self.manager.games)
        self.left_panel.list_widget.game_selection_changed.connect(
            self.on_game_selection_changed
        )
        self.splitter.addWidget(self.left_panel)

        # Right Panel
        self.right_panel.change_slot_requested.connect(self.on_change_slot_request)
        self.right_panel.delete_requested.connect(self.on_delete_state_request)
        self.right_panel.delete_confirmation.setChecked(settings.ask_confirmation)
        self.right_panel.delete_confirmation.stateChanged.connect(
            lambda c: setattr(settings, "ask_confirmation", bool(c))
        )
        self.splitter.addWidget(self.right_panel)

        if self.left_panel.list_widget.count() > 0:
            self.left_panel.list_widget.setCurrentRow(0)

        self.manager.update_needed.connect(self.on_update_needed)

        # Window Layout
        layout.addWidget(self.splitter)

        # Center window before show
        self.center_on_screen()

    @Slot(str)
    def on_game_selection_changed(self, name: str):
        if game := self.manager.get_game(name):
            self.right_panel.update_cards(game)

    @Slot(str, int, int)
    def on_change_slot_request(
        self, name: str, state_number: int, new_slot_number: int
    ):
        self.manager.move_slot(name, state_number, new_slot_number)

    @Slot(str, int)
    def on_delete_state_request(self, name: str, state_number: int) -> None:
        if settings.ask_confirmation:
            reply = QMessageBox.warning(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete slot #{state_number} ?",
                buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                defaultButton=QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        self.manager.delete_state(name, state_number)

    @Slot()
    def on_update_needed(self):
        selected_game = self.left_panel.list_widget.currentItem().text()
        self.left_panel.list_widget.refresh(self.manager.games)
        if new_row := self.left_panel.list_widget.findItems(
            selected_game, Qt.MatchFlag.MatchExactly
        ):
            self.left_panel.list_widget.setCurrentItem(new_row[0])
        else:
            self.right_panel.clear_container()

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.adjustSize()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_geometry.center())
        self.move(frame_geometry.topLeft())

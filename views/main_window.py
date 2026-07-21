from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QVBoxLayout

from views.left_panel import LeftPanel
from views.right_panel import RightPanel
from views.right_panel import RightPanel
from views.states_folder_dialog import StatesFolderDialog

import constants as c
from manager import manager
from settings import settings


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.states_folder_dialog = StatesFolderDialog()
        layout = QVBoxLayout(self)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()

        # Window Properties
        self.setWindowTitle(f"{c.APP_NAME} v{c.APP_VERSION[0]}.{c.APP_VERSION[1]}")
        self.setMinimumHeight(500)

        # Left Panel
        self.left_panel.update_right_panel.connect(self.right_panel.on_updated_game)
        self.splitter.addWidget(self.left_panel)

        # Right Panel
        self.splitter.addWidget(self.right_panel)

        # Window Layout
        layout.addWidget(self.splitter)

        # Center window before show
        self.center_on_screen()

        while not settings.retroarch_path:
            self.states_folder_dialog.exec()

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.adjustSize()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_geometry.center())
        self.move(frame_geometry.topLeft())

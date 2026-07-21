from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDialogButtonBox,
    QFileDialog,
)

from settings import settings


class StatesFolderDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.window_layout = QVBoxLayout()
        self.frame_widget = QFrame()
        self.frame_layout = QHBoxLayout()
        self.label = QLabel("RetroArch folder:")
        self.folder_le = QLineEdit()
        self.browse_button = QPushButton("...")
        self.dialog_buttons = QDialogButtonBox(Qt.Orientation.Horizontal)

        self.setup_ui()

    def setup_ui(self):
        self.folder_le.setFixedWidth(300)
        self.browse_button.setFixedSize(40, 30)
        self.browse_button.clicked.connect(self.on_browse_button_clicked)

        self.frame_layout.addWidget(self.label)
        self.frame_layout.addWidget(self.folder_le)
        self.frame_layout.addWidget(self.browse_button)
        self.frame_widget.setLayout(self.frame_layout)

        self.dialog_buttons.addButton(QDialogButtonBox.StandardButton.Ok)
        self.dialog_buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        self.dialog_buttons.accepted.connect(self.on_ok_button_clicked)
        self.dialog_buttons.rejected.connect(self.close)

        self.window_layout.addWidget(self.frame_widget)
        self.window_layout.addWidget(self.dialog_buttons)

        self.setLayout(self.window_layout)

    def on_ok_button_clicked(self):
        settings.retroarch_path = self.folder_le.text()
        if settings.states_path and settings.states_path.exists():
            self.accept()
        else:
            self.folder_le.setProperty("hasError", True)
            self.folder_le.style().unpolish(self.folder_le)
            self.folder_le.style().polish(self.folder_le)
            self.folder_le.update()

    def on_browse_button_clicked(self):
        user_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select RetroArch directory",
            options=QFileDialog.Option.DontUseNativeDialog
            | QFileDialog.Option.ShowDirsOnly,
        )
        self.folder_le.setText(user_path)

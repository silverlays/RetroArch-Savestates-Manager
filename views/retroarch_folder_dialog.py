from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDialogButtonBox,
    QFileDialog,
)

from settings import settings


class RetroarchFolderDialog(QDialog):
    description_label: QLabel
    form_layout: QHBoxLayout
    form_label: QLabel
    form_le: QLineEdit
    dialog_buttons: QDialogButtonBox

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Description Label
        self.description_label = QLabel(
            "Specify your RetroArch installation folder in the field below"
        )
        self.description_label.setProperty("class", "description")
        layout.addWidget(self.description_label)

        # Form
        self.form_layout = QHBoxLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 20)

        ## Form Label
        self.form_label = QLabel("RetroArch folder:")
        self.form_layout.addWidget(self.form_label)

        # Form LineEdit
        self.form_le = QLineEdit()
        self.form_le.setFixedWidth(300)
        self.form_layout.addWidget(self.form_le)

        # Form Browse Button
        self.form_browse_button = QPushButton("...")
        self.form_browse_button.setFixedSize(40, 30)
        self.form_browse_button.clicked.connect(self.on_browse_button_clicked)
        self.form_layout.addWidget(self.form_browse_button)

        layout.addLayout(self.form_layout)

        # Buttons Box
        self.dialog_buttons = QDialogButtonBox(
            Qt.Orientation.Horizontal,
            standardButtons=QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
        )
        self.dialog_buttons.accepted.connect(self.on_ok_button_clicked)
        self.dialog_buttons.rejected.connect(self.close)
        layout.addWidget(self.dialog_buttons)

    @Slot()
    def on_ok_button_clicked(self):
        settings.retroarch_path = self.form_le.text()
        if settings.states_path and settings.states_path.exists():
            self.accept()
        else:
            self.form_le.setProperty("hasError", True)
            self.form_le.style().unpolish(self.form_le)
            self.form_le.style().polish(self.form_le)
            self.form_le.update()

    @Slot()
    def on_browse_button_clicked(self):
        user_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select RetroArch directory",
            options=QFileDialog.Option.DontUseNativeDialog
            | QFileDialog.Option.ShowDirsOnly,
        )
        self.form_le.setText(user_path)

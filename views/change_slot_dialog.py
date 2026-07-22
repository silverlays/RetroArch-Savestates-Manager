from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox


class ChangeSlotDialog(QDialog):
    description_label: QLabel
    old_slot_label: QLabel
    new_slot_combobox: QComboBox
    standard_buttons: QDialogButtonBox

    def __init__(self, state_number: int, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Description Label
        self.description_label = QLabel(
            "You can choose here the new slot for a savestate"
        )
        self.description_label.setProperty("class", "description")
        layout.addWidget(self.description_label)

        # Old Slot Label
        self.old_slot_label = QLabel(
            f'Old slot number: <span style="color: #2ecc71; font-weight: bold;">{state_number}</span>'
        )
        self.old_slot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.old_slot_label)

        # New Slot Combobox
        self.new_slot_combobox = QComboBox()
        self.new_slot_combobox.addItem("Auto")
        self.new_slot_combobox.addItems([str(n) for n in range(1000)])
        layout.addWidget(self.new_slot_combobox)

        # Standard Buttons
        self.standard_buttons = QDialogButtonBox(
            standardButtons=QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        self.standard_buttons.accepted.connect(self.accept)
        self.standard_buttons.rejected.connect(self.reject)
        layout.addWidget(self.standard_buttons)

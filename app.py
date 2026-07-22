import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from views.retroarch_folder_dialog import RetroarchFolderDialog
from views.main_window import MainWindow

from settings import settings
import constants as c
import app_rc


# region QSS Style
def get_style() -> str:
    return """
    /* --- Base Variables & Global Widget --- */
    QWidget {
        background-color: #212121;
        color: #f0f0f0;
        font-family: "Segoe UI", "Helvetica Neue", sans-serif;
        font-size: 10pt;
    }

    /* --- GroupBoxes (Left & Right Panels) --- */
    QGroupBox {
        background-color: transparent;
        border: 1px solid #333333;
        border-radius: 6px;
        margin-top: 25px;
        padding-top: 15px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
        padding: 0 5px;
        color: #888888;
        font-weight: bold;
    }

    /* --- Left Panel: Game List --- */
    QListWidget#game_list_widget {
        background-color: transparent;
        border: none;
        outline: none;
        font-size: 12pt;
        font-weight: bold;
    }
    QListWidget#game_list_widget::item {
        padding: 12px 8px;
        border: 1px solid transparent;
        border-radius: 4px;
        color: #cccccc;
    }
    QListWidget#game_list_widget::item:hover {
        background-color: #2a2a2a;
    }
    QListWidget#game_list_widget::item:selected {
        border: 1px solid #00d4d0;
        background-color: rgba(0, 212, 208, 0.05);
        color: #00d4d0;
    }

    /* --- Right Panel: Header & Labels --- */
    QLabel#game_label {
        font-size: 22pt;
        font-weight: bold;
        color: #00d4d0;
        padding-bottom: 10px;
    }
    QLabel#state_number_label {
        color: #2ecc71;
        font-size: 12pt;
        font-weight: bold;
    }
    QLabel[class="description"] {
        color: #aaaaaa;
        font-size: 11pt;
        margin: 0 0 20px 0;
    }

    /* --- State Card (QFrame) --- */
    QFrame#state_frame {
        background-color: #181818;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 12px;
        margin: 5px;
    }

    /* --- ScrollArea & ScrollBars --- */
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    QScrollBar:horizontal {
        border: none;
        background: #2b2b2b;
        height: 12px;
        margin: 0px;
        border-radius: 6px;
    }
    QScrollBar::handle:horizontal {
        background: #555555;
        min-width: 30px;
        border-radius: 6px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #00d4d0;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }

    /* --- Buttons --- */
    QPushButton {
        background-color: #2a2a2a;
        color: #f0f0f0;
        border: 1px solid #444444;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #383838;
        border: 1px solid #666666;
    }
    QPushButton:pressed {
        background-color: #1c1c1c;
    }

    QPushButton#change_slot_button {
        background-color: #181818;
        color: #ffffff;
        border: 1px solid #00d4d0;
        margin-top: 10px;
    }
    QPushButton#change_slot_button:hover {
        background-color: rgba(0, 212, 208, 0.1);
    }

    QPushButton#delete_button {
        background-color: #6b1717;
        color: #ffffff;
        border: 1px solid #8f1f1f;
        margin-top: 5px;
    }
    QPushButton#delete_button:hover {
        background-color: #8f1f1f;
        border: 1px solid #b32727;
    }

    /* --- ComboBox (Dialog) --- */
    QComboBox {
        background-color: #181818;
        color: #ffffff;
        border: 1px solid #00d4d0;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 11pt;
        font-weight: bold;
        margin: 10px;
    }
    QComboBox:hover {
        background-color: #212121;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left-width: 0px;
    }
    QComboBox::down-arrow {
        image: url(:/assets/arrow_down.png);
        width: 14px;
        height: 14px;
    }
    QComboBox QAbstractItemView {
        background-color: #212121;
        color: #f0f0f0;
        border: 1px solid #00d4d0;
        selection-background-color: #00d4d0;
        selection-color: #000000;
        outline: none;
    }

    /* --- LineEdit (RetroarchFolderDialog) --- */
    QLineEdit {
        background-color: #181818;
        color: #ffffff;
        border: 1px solid #444444;
        border-radius: 4px;
        padding: 6px 10px;
    }
    QLineEdit:focus {
        border: 1px solid #00d4d0;
    }
    QLineEdit[hasError="true"] {
        border: 1px solid #e74c3c;
    }

    /* --- CheckBox --- */
    QCheckBox {
        color: #cccccc;
        spacing: 10px;
        font-size: 10pt;
    }
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 1px solid #555555;
        border-radius: 4px;
        background-color: #181818;
    }
    QCheckBox::indicator:hover {
        border: 1px solid #00d4d0;
    }
    QCheckBox::indicator:checked {
        background-color: rgba(0, 212, 208, 0.2);
        border: 1px solid #00d4d0;
        image: url(:/assets/check.png);
    }
    """


# endregion


if __name__ == "__main__":
    app = QApplication()
    app.setOrganizationName(c.ORGANISATION_NAME)
    app.setApplicationName(c.APP_NAME)
    app.setApplicationVersion(".".join(map(str, c.APP_VERSION)))
    app.setWindowIcon(QIcon(":/app.ico"))
    app.setStyleSheet(get_style())

    if not settings.retroarch_path:
        dialog = RetroarchFolderDialog()
        dialog.exec()
        if not settings.retroarch_path:
            sys.exit(0)

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())

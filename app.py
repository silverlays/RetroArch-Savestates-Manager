import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from views.retroarch_folder_dialog import RetroarchFolderDialog
from views.main_window import MainWindow

from settings import settings
import constants as c


# region QSS Style
def get_style():
    return """
QScrollArea {
    border: none;
    background-color: transparent;
}

QLineEdit {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 6px;
    padding: 6px 10px;
    color: #e0e0e0;
}

QLineEdit:focus {
    border: 1px solid #00e5ff;
}

QLineEdit[hasError="true"] {
    border: 1px solid #ff4444;
    background-color: #2a1515;
}

#game_label {
    font-size: 28px;
    font-weight: bold;
    color: #00e5ff;
}

#state_number_label {
    font-size: 16px;
    font-weight: bold;
    color: #2ecc71;
}

#picture_label {
    background-color: #111111;
    border: 1px solid #333333;
    border-radius: 8px;
}

#delete_button {
    font-size: 13px;
    font-weight: bold;
    min-height: 34px;
    color: #ffffff;
    background-color: #7a1515;
    border: 1px solid #991b1b;
    border-radius: 6px;
    padding: 0 16px;
}

#delete_button:hover {
    background-color: #991b1b;
    border-color: #ef4444;
}

#delete_button:pressed {
    background-color: #dc2626;
    border-color: #f87171;
}

#delete_button:disabled {
    background-color: #222222;
    border: 1px solid #333333;
    color: #555555;
}

QGroupBox {
    border: 1px solid #333333;
    border-radius: 8px;
    margin-top: 12px;
    font-weight: bold;
    color: #888888;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
}

#game_list_widget {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 4px;
    outline: none;
}

#game_list_widget::item {
    color: #b0b0b0;
    padding: 8px 10px;
    margin-bottom: 2px;
    border-radius: 5px;
    border-left: 3px solid transparent;
}

#game_list_widget::item:hover {
    background-color: #282828;
    color: #ffffff;
}

#game_list_widget::item:selected {
    background-color: #1e2d38;
    color: #00e5ff;
    border-left: 3px solid #00e5ff;
    font-weight: bold;
}

#game_list_widget QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 4px 2px;
}

#game_list_widget QScrollBar::handle:vertical {
    background: #3a3a3a;
    border-radius: 3px;
    min-height: 20px;
}

#game_list_widget QScrollBar::handle:vertical:hover {
    background: #00e5ff;
}

#game_list_widget QScrollBar::add-line:vertical,
#game_list_widget QScrollBar::sub-line:vertical {
    height: 0px;
}

#state_frame {
    background-color: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 8px;
}

#state_frame:hover {
    border: 1px solid #00e5ff; /* Illumination de la bordure en cyan néon */
    background-color: #222222; /* Légère clarification du fond */
}
"""


# endregion


if __name__ == "__main__":
    app = QApplication()
    app.setOrganizationName(c.ORGANISATION_NAME)
    app.setApplicationName(c.APP_NAME)
    app.setApplicationVersion(".".join(map(str, c.APP_VERSION)))
    app.setWindowIcon(QIcon("app.ico"))
    app.setStyleSheet(get_style())

    if not settings.retroarch_path:
        dialog = RetroarchFolderDialog()
        dialog.exec()
        if not settings.retroarch_path:
            sys.exit(0)

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())

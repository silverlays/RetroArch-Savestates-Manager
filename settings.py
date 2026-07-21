from pathlib import Path
from PySide6.QtCore import QSettings

import constants as c


class Settings(QSettings):
    def __init__(self):
        super().__init__(c.ORGANISATION_NAME, c.APP_NAME)

    @property
    def retroarch_path(self):
        path_settings = self.value("ra_path")
        if path_settings and Path(path_settings).exists():
            return Path(path_settings)

    @retroarch_path.setter
    def retroarch_path(self, value: str):
        path = Path(value)
        if path.exists():
            self.setValue("ra_path", str(path.resolve()))

    @property
    def states_path(self):
        if self.retroarch_path:
            return self.retroarch_path / "states"


settings = Settings()

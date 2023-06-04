from PySide6.QtCore import QObject, QSettings, Signal
from typing import Dict

from db.settings import settingEntries


class SettingsWrapper(QSettings):
    valueChanged = Signal(str, object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setValue(self, key, value):
        super().setValue(key, value)
        self.valueChanged.emit(key, value)

    def update(self):
        for i in self.allKeys():
            self.valueChanged.emit(
                i, self.value(i, type = type(settingEntries[i]))
            )

class GlobalSettings:
    instance: 'GlobalSettings' = None

    def __init__(self):
        self.settings = SettingsWrapper("MatCal", "preferences")
        self.settingsItems: Dict[str, 'GlobalSettingsItem'] = dict()

if GlobalSettings.instance is None:
    GlobalSettings.instance = GlobalSettings()

def gsettings():
    return GlobalSettings.instance.settings


class GlobalSettingsItem(QObject):
    valueChanged = Signal(object)
    def __init__(self, item: str):
        super().__init__()
        self.__item = item

    def get(self):
        return gsettings().value(
            self.__item, type = type(settingEntries[self.__item])
        )

    def set(self, value):
        gsettings().setValue(self.__item, value)

    def update(self):
        self.valueChanged.emit(self.get())


class GlobalSettingsItemInterfacer:

    def __init__(self):
        pass

    def item(self, item: str):
        assert (item in GlobalSettings.instance.settingsItems)
        return GlobalSettings.instance.settingsItems[item]

    def create(self, item: str):
        assert (item not in GlobalSettings.instance.settingsItems)
        GlobalSettings.instance.settingsItems[item] = GlobalSettingsItem(item)
        return GlobalSettings.instance.settingsItems[item]

    instance: 'GlobalSettingsItemInterfacer' = None

    @staticmethod
    def _updateConnections(item, value):
        if item in GlobalSettings.instance.settingsItems:
            GlobalSettings.instance.settingsItems[item].valueChanged.emit(value)


if GlobalSettingsItemInterfacer.instance is None:
    GlobalSettingsItemInterfacer.instance = GlobalSettingsItemInterfacer()
    for i in settingEntries:
        GlobalSettingsItemInterfacer.instance.create(i)
    GlobalSettings.instance.settings.valueChanged.connect(
        GlobalSettingsItemInterfacer._updateConnections
    )


def settings(item: str):
    assert (item in settingEntries)
    return GlobalSettingsItemInterfacer.instance.item(item)

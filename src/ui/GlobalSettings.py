from PySide6.QtCore import QCoreApplication, QObject, QSettings, Signal
from PySide6.QtWidgets import QApplication
from collections import defaultdict
from typing import overload, Union, Dict

from functools import singledispatch

from src.ui.settings import settingEntries


class SettingsWrapper(QSettings):
    valueChanged = Signal(str, object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setValue(self, key, value):
        super().setValue(key, value)
        self.valueChanged.emit(key, value)

    def update(self):
        # QSettings()
        for i in self.allKeys():
            self.valueChanged.emit(i, self.value(i))


# class GlobalSettings(QObject):
#     settings = SettingsWrapper()
#     settingsItems = defaultdict(set)
#
#
#     @staticmethod
#     def getSettingsItem(item):
#         return GlobalSettings.GlobalSettingsItem(item)

class GlobalSettings:
    instance: 'GlobalSettings' = None

    # @property
    # def instance():
    #     if GlobalSettings.__instance is None:
    #         GlobalSettings.__instance = GlobalSettings()
    #     return GlobalSettings.__instance

    def __init__(self):
        self.settings = SettingsWrapper()
        # self.settingsItems = defaultdict(set)
        self.settingsItems: Dict[str, 'GlobalSettingsItem'] = dict()

    # @staticmethod
    # def __setupInstance():
    #     # if GlobalSettings.__gs is None:
    #     #     GlobalSettings.__gs = GlobalSettings()
    #     # return GlobalSettings.__gs
    #     GlobalSettings.instance = GlobalSettings()
    #
    # __DISCARD_setup_instance_static__ = __setupInstance()


if GlobalSettings.instance is None:
    GlobalSettings.instance = GlobalSettings()

# def settings():
#     return GlobalSettings.instance().settings


def gsettings():
    return GlobalSettings.instance.settings


class GlobalSettingsItem(QObject):
    valueChanged = Signal(object)

    # @staticmethod
    # def __updateConnections(item, value):
    #     if item in GlobalSettings.instance().settingsItems:
    #         for settingsItem in GlobalSettings.instance().settingsItems[item]:
    #             # settingsItem.valueChanged.emit(settings().value(item))
    #             settingsItem.valueChanged.emit(value)
    #
    # __setupConnectDISCARD__ = GlobalSettings.instance(
    # ).settings.valueChanged.connect(__updateConnections)

    def __init__(self, item: str):
        super().__init__()
        self.__item = item

    def get(self):
        return gsettings().value(self.__item, type=type(settingEntries[self.__item]))

    def set(self, value):
        gsettings().setValue(self.__item, value)

    def update(self):
        self.valueChanged.emit(self.get())


class GlobalSettingsItemInterfacer:
    def __init__(self):
        pass

    def item(self, item: str):
        # if item in GlobalSettings.instance().settingsItems:
        #     return GlobalSettings.instance().settingsItems[item]
        assert (item in GlobalSettings.instance.settingsItems)
        # return GlobalSettingsItem(item)
        return GlobalSettings.instance.settingsItems[item]

    def create(self, item: str):
        assert (item not in GlobalSettings.instance.settingsItems)
        GlobalSettings.instance.settingsItems[item] = GlobalSettingsItem(item)
        return GlobalSettings.instance.settingsItems[item]

    instance: 'GlobalSettingsItemInterfacer' = None

    # @staticmethod
    # def _createItems():
    #     GlobalSettingsItemInterfacer.instance = GlobalSettingsItemInterfacer()
    #     for i in settingEntries:
    #         GlobalSettingsItemInterfacer.instance.create(i)

    @staticmethod
    def _updateConnections(item, value):
        if item in GlobalSettings.instance.settingsItems:
            GlobalSettings.instance.settingsItems[item].valueChanged.emit(
                value)


if GlobalSettingsItemInterfacer.instance is None:
    GlobalSettingsItemInterfacer.instance = GlobalSettingsItemInterfacer()
    for i in settingEntries:
        GlobalSettingsItemInterfacer.instance.create(i)
    GlobalSettings.instance.settings.valueChanged.connect(
        GlobalSettingsItemInterfacer._updateConnections)


def settings(item: str):
    assert (item in settingEntries)
    return GlobalSettingsItemInterfacer.instance.item(item)

# @settings.register
# def _(item: str):
#     return GlobalSettingsItem(item)

# def settings() -> GlobalSettings

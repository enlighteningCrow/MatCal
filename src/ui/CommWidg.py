from typing import Callable, List, Optional, Tuple, Union

from abc import ABC, abstractmethod
from PySide6.QtCore import Signal

from PySide6.QtWidgets import QWidget


class CommWidgPersistent():

    @abstractmethod
    def saveState(self):
        raise NotImplementedError()

    @abstractmethod
    def loadState(self, state: dict):
        raise NotImplementedError()


class CommWidg(QWidget):

    isChanged = Signal(CommWidgPersistent)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

    # def __init__(self, li: List[Tuple[str, Callable]]) -> None:
    #     self.lists = li

    # The following Tuples contain: the name of the button, the method it should activate in the widget, and whether it should receive a matrix as a parameter
    # def getButtons(self) -> List[Tuple[str, Callable, bool]]:
    #     raise NotImplementedError()

    #TODO: Make the widgets have this as a slot, and make it as the MainWindow instance to manipulate with the list methods
    @abstractmethod
    def setMainWindow(self, mainwindow) -> None:
        # pass
        raise NotImplementedError()

    @abstractmethod
    def getMainWindow(self):
        raise NotImplementedError()

    @abstractmethod
    def needsTensorsTab(self) -> bool:
        raise NotImplementedError()

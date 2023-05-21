from typing import Callable, List, Tuple

# from abc import ABC, abstractmethod


class CommWidg():

    # def __init__(self, li: List[Tuple[str, Callable]]) -> None:
    #     self.lists = li

    # The following Tuples contain: the name of the button, the method it should activate in the widget, and whether it should receive a matrix as a parameter
    # def getButtons(self) -> List[Tuple[str, Callable, bool]]:
    #     raise NotImplementedError()

    #TODO: Make the widgets have this as a slot, and make it as the MainWindow instance to manipulate with the list methods
    # @abstractmethod
    def setMainWindow(self, mainwindow) -> None:
        # pass
        raise NotImplementedError()

from generated.designer.easyUI.ui_BinaryCalculator import Ui_Form

from PySide6.QtWidgets import QWidget, QApplication, QLineEdit
from PySide6.QtCore import QCoreApplication, QPropertyAnimation
# from PySide6.QtCore import QPropertyAnimation

class TEST(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        # self.__ui.
        
        # self.__ui.lineEdit.focusInEvent

        assert(QApplication.instance() is not None)

        # self.__ui.widget.setInputLine(self.__)

        QApplication.instance().focusChanged.connect(self.animateNumpad)

        print(self.__ui.widget.maximumHeight())

        if not isinstance(QApplication.focusObject(), QLineEdit):
            self.__ui.widget.setMaximumHeight(0)
        else:
            self.__ui.widget.setMaximumHeight(1000)

    def animateNumpad(self, a, b):
        print(f"Animate from {a} to {b}")
        if isinstance(a, QLineEdit) != isinstance(b, QLineEdit):
            if isinstance(a, QLineEdit):
                print(f"Animate hide")
                # self.__ui.widget.aHide()
                anim = QPropertyAnimation(self.__ui.widget, b"maximumHeight", self)
                # anim = QPropertyAnimation(self.__ui.widget, b"height", self)
                anim.setDuration(1000)
                anim.setStartValue(1000)
                anim.setEndValue(0)
                anim.start()
                # self.__ui.widget
            else:
                print(f"Animate show")
                # self.__ui.widget.aShow()
                anim = QPropertyAnimation(self.__ui.widget, b"maximumHeight", self)
                # anim = QPropertyAnimation(self.__ui.widget, b"height", self)
                anim.setDuration(1000)
                anim.setStartValue(0)
                anim.setEndValue(1000)
                anim.start()




if __name__ == '__main__':
    a = QApplication()

    t = TEST()
    t.show()
    a.exec()
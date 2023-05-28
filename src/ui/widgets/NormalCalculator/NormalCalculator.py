from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QGridLayout, QPushButton

from ui.CommWidg import CommWidg, CommWidgPersistent

class NormalCalculator(CommWidg):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator")

        self.result_line_edit = QLineEdit()
        self.result_line_edit.setReadOnly(True)

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        layout = QVBoxLayout(self)
        layout.addWidget(self.result_line_edit)

        button_layout = QGridLayout()
        layout.addLayout(button_layout)

        row = 0
        col = 0
        for button_text in self.buttons:
            button = QPushButton(button_text)
            button.clicked.connect(self.handle_button_click)
            button_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.__mainwindow = None

    def handle_button_click(self):
        clicked_button = self.sender()
        button_text = clicked_button.text()

        if button_text == "=":
            expression = self.result_line_edit.text()
            try:
                result = eval(expression)
                self.result_line_edit.setText(str(result))
            except Exception:
                self.result_line_edit.setText("Error")
        else:
            current_text = self.result_line_edit.text()
            new_text = current_text + button_text
            self.result_line_edit.setText(new_text)

    def setMainWindow(self, mainwindow) -> None:
        self.__mainwindow = mainwindow

    def getMainWindow(self):
        return self.__mainwindow

    def needsTensorsTab(self) -> bool:
        return False

# #TODO: Continue this
# class NormalCalculatorPersistent(NormalCalculator, CommWidgPersistent):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Persistent Calculator")

#     def setMainWindow(self, mainwindow) -> None:
from PySide6.QtWidgets import QLineEdit, QComboBox, QHBoxLayout, QWidget

class NumberInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.number_input = QLineEdit(self)
        self.number_input.setPlaceholderText("Enter a number")

        self.number_format = QComboBox(self)
        self.number_format.addItems(["Decimal", "Binary", "Octal", "Hexadecimal"])

        layout = QHBoxLayout(self)
        layout.addWidget(self.number_input)
        layout.addWidget(self.number_format)

    def get_number(self):
        number_str = self.number_input.text()
        number_format = self.number_format.currentText()

        if number_format == "Decimal":
            return int(number_str)
        elif number_format == "Binary":
            return int(number_str, 2)
        elif number_format == "Octal":
            return int(number_str, 8)
        elif number_format == "Hexadecimal":
            return int(number_str, 16)

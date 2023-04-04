from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QStyledItemDelegate, QItemDelegate, QSpinBox, QTableView, QWidget, QVBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from NNIntSI import NNIntSI, NNIntSIM

# class SpinBoxDelegate(QStyledItemDelegate):

#     def createEditor(self, parent, option, index):
#         editor = QSpinBox(parent)
#         editor.setMinimum(0)
#         editor.setMaximum(2 ** 31 - 1)
#         editor.setButtonSymbols(QSpinBox.NoButtons)
#         editor.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
#         editor.setFrame(False)
#         editor.setKeyboardTracking(False)
#         editor.setLocale(Qt.CLocale())
#         editor.setValidator(QIntValidator(0, 2 ** 31 - 1, editor))
#         return editor

#     def setEditorData(self, editor, index):
#         value = index.model().data(index, Qt.EditRole)
#         editor.setValue(int(value))

#     def setModelData(self, editor, model, index):
#         model.setData(index, editor.value(), Qt.EditRole)


class SpinBoxDelegate(QStyledItemDelegate):

    def __init__(self, parent = None, minVal: int = 0, maxVal: int = 1_000_000):
        super().__init__(parent)
        self.minVal = minVal
        self.maxVal = maxVal

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setMinimum(self.minVal)
        editor.setMaximum(self.maxVal)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(int(value))

    def setModelData(self, editor, model, index):
        value = editor.value()
        print("Model data set on", index, "to", value)
        model.setData(index, value, Qt.EditRole)

    def setMax(self, maxVal: int):
        self.maxVal = maxVal

    def setMin(self, minVal: int):
        self.minVal = minVal


class IndexSpinBoxDelegate(QStyledItemDelegate):

    def __init__(self, parent = None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        if (index.model() is None):
            print("The model is None")
            editor.setMinimum(self.minVal)
            editor.setMaximum(self.maxVal)
        else:
            editor.setMinimum(1)
            # print(type(index.model()))
            item: NNIntSI = index.model().item(index.row(), 0)
            # print(item.text())
            # print(type(index.model().item(index.row(), 0)).getValue())
            # print("Value:", index.model().item(index.row, 0).getValue())
            editor.setMaximum(item.getValue())
        return editor


if __name__ == '__main__':
    app = QApplication([])
    table_model = QStandardItemModel(4, 2)
    table_model.setHorizontalHeaderLabels(['Name', 'Age'])
    table_view = QTableView()
    table_view.setModel(table_model)
    delegate = SpinBoxDelegate(table_view)
    table_view.setItemDelegateForColumn(1, delegate)
    for row in range(4):
        for column in range(2):
            item = QStandardItem(str(row + 5 * column))
            table_model.setItem(row, column, item)
    widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(table_view)
    widget.setLayout(layout)
    widget.show()
    app.exec()

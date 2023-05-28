from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication
import torch

from PySide6.QtCore import Qt


class TensorTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def setTensor(self, tensor):
        self.clear()
        if tensor.dim() == 0:
            self.setRowCount(1)
            self.setColumnCount(1)
            item = QTableWidgetItem(str(tensor.item()))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.setItem(0, 0, item)
        elif tensor.dim() == 1:
            self.setRowCount(tensor.size(0))
            self.setColumnCount(1)

            for i in range(self.rowCount()):
                item = QTableWidgetItem(str(tensor[i].item()))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.setItem(i, 0, item)
        elif tensor.dim() == 2:
            self.setRowCount(tensor.size(0))
            self.setColumnCount(tensor.size(1))

            for i in range(self.rowCount()):
                for j in range(self.columnCount()):
                    item = QTableWidgetItem(str(tensor[i, j].item()))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.setItem(i, j, item)
        else:
            self.setRowCount(1)
            self.setColumnCount(1)
            item = QTableWidgetItem("Invalid Tensor")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.setItem(0, 0, item)
# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QSpinBox, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QTableView

from PySide6.QtCore import QTimer, QModelIndex, Qt

from PySide6.QtGui import QStandardItem, QStandardItemModel

from FrameEditor import FrameEditor
from DIndexEditor import DIndexEditor
import torch

from typing import List

# from ui_DIndexLabels import Ui_Form
from ui_DimensionEditor import Ui_Form

from NNIntSI import NNIntSI, NNIntSIM
from SpinBoxDelegate import SpinBoxDelegate, IndexSpinBoxDelegate

# TODO: Use a stackedwidget or something to swap between with 0 dimensions (1 lineedit), 1 dimension (1 row/column of lineedit), 2 dimensions (matrix of lineedits), 3+ dimensions (matrix of lineedits in selectable dimensions for columns and rows, with other dimensions selected with the spinboxes)


class SizeBinding:

    def __init__(self, dimEdit: 'DimensionEditor', dim: int) -> None:
        self.dimEdit = dimEdit
        self.dim = dim

    def updateSize(self, val: int) -> None:
        # TODO: Make this change the dimensions
        if val < self.dimEdit.matrix.shape[self.dim]:
            self.dimEdit.matrix = self.dimEdit.matrix[tuple(
                (slice(None, None) if i != self.dim else slice(None, val))
                for i in range(self.dim)
            )]
        elif val < self.dimEdit.matrix.shape[self.dim]:
            shape = list(self.dimEdit.matrix.shape)
            shape[self.dim] = self.dimEdit.matrix.shape[self.dim] - val
            self.dimEdit.matrix = torch.cat(
                (
                    self.dimEdit.matrix,
                    torch.ones(shape, device = self.dimEdit.matrix.device)
                ), self.dim
            )

    def __call__(self, val: int) -> None:
        return self.updateSize(val)


class DimensionEditor(QWidget):

    def __init__(self, parent: 'MatrixEditor' = None):
        super().__init__(parent)
        self.initialized = False
        # self.dimensions = 0
        # self.dindEditors: List[DIndexEditor] = []
        self.matrix = torch.zeros(())
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.frameEditor = FrameEditor(self.matrix, self)
        self.__ui.scrollAreaFE.setWidget(self.frameEditor)
        self.dim0 = None
        self.dim1 = None
        # self.prevXVal = None
        # self.prevYVal = None

        self.xDimLabel = self.__ui.selectionXLabel
        self.xDimSpin = self.__ui.selectionXSpinbox
        self.xDimSpin.valueChanged.connect(self.updateDimensions_t)
        self.yDimLabel = self.__ui.selectionYLabel
        self.yDimSpin = self.__ui.selectionYSpinbox
        self.yDimSpin.valueChanged.connect(self.updateDimensions_t)
        # self.updateDimensionsTableMaxSize()

        # self.__ui.splitterEditor.setSizes(
        #     [self.__ui.dimensionsTable.width(), 0]
        # )
        self.__ui.dimensionsTable.horizontalHeader().geometriesChanged.connect(
            self.udtmsImpl
        )
        self.__ui.dimensionsTable.verticalHeader().geometriesChanged.connect(
            self.udtmsImpl
        )
        # self.__ui.dimensionsTable.layout().contentsMargins().connect(
        #     self.udtmsImpl
        # )
        """
        TODO: Make the assertions/exceptions inisde fo the NNIntSI.py such that 
        nonnegative integers from the setter throw an exception, which should be catched 
        by this class or somewhere else
        TODO: Set the below changeDimensions to not use inc, dec; use the below to clone the items needed, and connect them
        """
        self.model = NNIntSIM(self)
        # self.model = QStandardItemModel(self)
        self.__ui.dimensionsTable.setModel(self.model)
        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels(["Size", "Selection"])
        # self.__ui.dimensionsTable.setEditTriggers(QTableView.DoubleClicked)
        # self.__sizeItem = NNIntSI(1)
        # self.__selectionItem = NNIntSI(0)
        # self.model.item(1, 3).getValue()

        self.changeDimensions(parent.getDimensions())
        spbidIndex = IndexSpinBoxDelegate(self.__ui.dimensionsTable)
        spbidSize = SpinBoxDelegate(self.__ui.dimensionsTable, 1)
        self.__ui.dimensionsTable.setItemDelegateForColumn(0, spbidSize)
        self.__ui.dimensionsTable.setItemDelegateForColumn(1, spbidIndex)

        self.updateDimensionsCount(self.model.rowCount())
        # self.model.dataChanged.connect(
        #     lambda x: self.model.itemFromIndex(x).setValue()
        # )
        # self.model.dataChanged.connect(lambda x: print(self.model.data(x)))
        # self.__ui.dimensionsTable.edi
        # self.model.dataChanged.connect(lambda x: print(type(self.model.data(x))))
        self.model.dataChanged.connect(self.modelUpdateHandler)

        self.initialized = True

    def modelUpdateHandler(
        self, index0: QModelIndex, index1: QModelIndex, li: list
    ):
        # print(index0, index1, li)
        # print(index0.column())
        if index0.column() == 0:
            self.updateSize(self.model.itemFromIndex(index0).getValue())
        self.updateFrameMatrix()

    def udtmsImpl(self):
        margins = self.__ui.dimensionWidget.layout().contentsMargins()
        # print("width =", self.__ui.dimensionsTable.verticalHeader().width())
        # print(margins)
        self.__ui.dimensionWidget.setMaximumWidth(
            self.__ui.dimensionsTable.horizontalHeader().length() +
            self.__ui.dimensionsTable.verticalHeader().width() +
            self.__ui.dimensionsTable.frameWidth() * 2 + margins.left() +
            margins.right() + 6 + (
                self.__ui.dimensionsTable.verticalScrollBar().width() if
                self.__ui.dimensionsTable.verticalScrollBar().isVisible() else 0
            )
            # margins.left() + margins.right() + 2
        )

    def getCurrentFrame(self):
        currentFrame = tuple()
        for i in range(self.model.rowCount()):
            if self.dim0 is not None and self.dim0 == i or self.dim1 is not None and self.dim1 == i:
                currentFrame += tuple([slice(None, None)])
            else:
                currentFrame += tuple([self.model.item(i, 1).getValue()])
        print(currentFrame)
        return currentFrame

    def updateFrameMatrix(self, empty: bool = False):
        # mat = self.
        # print(self.matrix)
        # print(self.matrix.shape)
        # return
        if empty:
            #TODO: Maybe make this do the same as the below; remove the if empty completely
            self.frameEditor.updateMatrix(torch.zeros(()))
        else:
            # print(self.getCurrentFrame())
            print(self.getCurrentFrame())
            print(self.matrix)
            self.frameEditor.updateMatrix(self.matrix[self.getCurrentFrame()])

    def changeDimensions(self, dim):
        currentDimensions = self.model.rowCount()

        if currentDimensions == dim:
            return

        self.model.setRowCount(dim)
        if currentDimensions < dim:
            for i in range(currentDimensions, dim):
                self.model.setItem(
                    # i, 0, self.__sizeItem.clone()
                    i,
                    0,
                    NNIntSI(1)
                )
                self.model.setItem(
                    # i, 1, self.__selectionItem.clone()
                    i,
                    1,
                    NNIntSI(1)
                )
            #TODO: Fix this code and the below else code; find why it does not work
            self.matrix = self.matrix.reshape(
                self.matrix.shape +
                tuple((1 for i in range(self.matrix.dim(), dim)))
            )
        else:
            self.matrix = self.matrix.reshape(self.matrix.shape[: dim])

        # self.frameEditor.updateDimensionsCount(dim)
        print(currentDimensions, dim)
        self.updateDimensionsCount(dim)

        # self.frameEditor.updateBindings()
        # self.updateDimensionsTableMaxSize()

    # def __showHideDTWidgets(self, index: QModelIndex, show: bool):
    #     # op = QWidget.show if show else QWidget.hide
    #     # op(self.__ui.dimensionsTable.indexWidget(index))
    #     self.model.item

    def updateDimensions_t(self, _):
        return self.updateDimensions(self.model.rowCount())

    def updateDimensions(self, dimensions: int):
        # shape = self.dimensionEditor.matrix.shape
        # self.updateBindings()
        # self.dimensionEditor.updateDimensions(
        #     self.xDimSpin.value(), self.yDimSpin.value()
        # )

        # t = QTimer(self)
        # t.setSingleShot(True)

        setHide = set()
        setShow = set()

        if self.dim0 is not None and self.dim0 < dimensions:
            setShow.add(self.dim0)

        if self.dim1 is not None and self.dim1 < dimensions:
            setShow.add(self.dim1)

        if dimensions >= 1:
            setHide.add(self.xDimSpin.value())
            self.dim0 = self.xDimSpin.value()

        if dimensions >= 2:
            setHide.add(self.yDimSpin.value())
            self.dim1 = self.yDimSpin.value()

        for i in setHide.difference(setShow):
            self.model.item(i, 1).setVisibility(False)

        for i in setShow.difference(setHide):
            self.model.item(i, 1).setVisibility(True)

        #

        # if self.dim0 is not None and self.dim0 < dimensions:
        #     # t.timeout.connect(
        #     # self.model.item(self.dim0, 1).setData(Qt.ItemIsEnabled, True)
        #     self.model.item(self.dim0, 1).setVisibility(True)
        #     # self.model.setItem(self.dim0, 1, None)
        #     # self.model.item(self.dim0, 1).setFlags(Qt.ItemIsEditable)
        #     # self.model.item(self.dim0, 1).setData(0)
        #     # )
        #     # self.__ui.dimensionsTable.indexWidget(
        #     #     self.model.index(self.dim0, 1)
        #     # ).show()
        #     # dindEditors[self.dim0].showCurInd()
        #     # if currentDimensions == dimensions:
        #     #     self.dindEditors[self.dim0].setCurInd(0)

        # if self.dim1 is not None and self.dim1 < dimensions:
        #     # t.timeout.connect(
        #     # self.model.item(self.dim1, 1).setData(Qt.ItemIsEnabled, True)
        #     self.model.item(self.dim1, 1).setVisibility(True)
        #     # self.model.setItem(self.dim1, 1, None)
        #     # self.model.item(self.dim1, 1).setFlags(Qt.ItemIsEditable)
        #     # self.model.item(self.dim1, 1).setData(0)
        #     # )
        #     # self.__ui.dimensionsTable.indexWidget(
        #     #     self.model.index(self.dim1, 1)
        #     # ).show()
        #     # self.dindEditors[self.dim1].showCurInd()

        # if dimensions >= 1:
        #     # t.timeout.connect(
        #     # self.model.item(self.xDimSpin.value(), 1).setData(Qt.ItemIsEnabled, False)
        #     self.model.item(self.xDimSpin.value(), 1).setVisibility(False)
        #     # self.model.setItem(self.xDimSpin.value(), 1, None)
        #     # self.model.item(self.xDimSpin.value(), 1).setFlags(Qt.ItemIsEditable)
        #     # self.__ui.dimensionsTable.
        #     # self.model.item(self.xDimSpin.value(), 1).setData(0)
        #     # )
        #     # self.__ui.dimensionsTable.indexWidget(
        #     #     self.model.index(self.xDimSpin.value(), 1)
        #     # ).hide()
        #     # self.dindEditors[self.xDimSpin.value()].hideCurInd()
        #     self.dim0 = self.xDimSpin.value()

        # if dimensions >= 2:
        #     # t.timeout.connect(
        #     # self.model.item(self.yDimSpin.value(), 1).setData(Qt.ItemIsEnabled, False)
        #     self.model.item(self.yDimSpin.value(), 1).setVisibility(False)
        #     # self.model.setItem(self.yDimSpin.value(), 1, None)
        #     # self.model.item(self.yDimSpin.value(), 1).setFlags(Qt.ItemIsEditable)
        #     # self.model.item(self.yDimSpin.value(), 1).setData(0)
        #     # )
        #     # self.__ui.dimensionsTable.indexWidget(
        #     #     self.model.index(self.yDimSpin.value(), 1)
        #     # ).hide()
        #     # self.dindEditors[self.yDimSpin.value()].hideCurInd()
        #     self.dim1 = self.yDimSpin.value()

        # # print(
        # #     "(prevXVal: %d, prevYVal: %d)" %
        # #     (self.xDimSpin.value(), self.yDimSpin.value())
        # # )
        # # self.updateDimensions(
        # #     self.xDimSpin.value(), self.yDimSpin.value()
        # # )
        # # print(value)

        # # self.__ui.dimensionsTable.sethidden

        self.updateFrameMatrix(self.dim0 == self.dim1)
        # t.start(0)

    # def updateDimensions(self, dim0, dim1):
    #     # self.dindEditors[dim0].hideCurInd()
    #     # self.dindEditors[dim1].hideCurInd()
    #     self.dim0 = dim0
    #     self.dim1 = dim1
    #     self.updateFrameMatrix(dim0 == dim1)

    def updateDimensionsCount(self, dimensions: int):
        self.xDimSpin.setMaximum(max(0, dimensions - 1))
        self.yDimSpin.setMaximum(max(0, dimensions - 1))
        if dimensions >= 2:
            self.yDimLabel.show()
            self.yDimSpin.show()
            self.xDimLabel.show()
            self.xDimSpin.show()
        else:
            self.yDimLabel.hide()
            self.yDimSpin.hide()
            if dimensions >= 1:
                self.xDimLabel.show()
                self.xDimSpin.show()
            else:
                self.xDimLabel.hide()
                self.xDimSpin.hide()
            # pass
        if self.initialized:
            self.updateDimensions(dimensions)

    def updateSize(self, val: int) -> None:
        # TODO: Make this change the dimensions
        if val < self.matrix.shape[val]:
            self.matrix = self.matrix[tuple(
                (slice(None, None) if i != val else slice(None, val))
                for i in range(val)
            )]
        elif val < self.matrix.shape[val]:
            shape = list(self.matrix.shape)
            shape[val] = self.matrix.shape[val] - val
            self.matrix = torch.cat(
                (self.matrix, torch.ones(shape, device = self.matrix.device)),
                val
            )

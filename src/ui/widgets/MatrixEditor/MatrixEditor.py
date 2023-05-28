# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QWidget, QMessageBox

from PySide6.QtCore import QModelIndex, QSortFilterProxyModel

from .FrameEditor import FrameEditor
import torch
from torch import Tensor

from typing import Tuple, Union, Optional

# from ui_DIndexLabels import Ui_Form
from generated.designer.ui_MatrixEditor import Ui_Form

from ui.models.NNIntSI import NNIntSI, NNIntSIM
from ui.delegates.SpinBoxDelegate import SpinBoxDelegate, IndexSpinBoxDelegate

import logging

from ui.CommWidg import CommWidg, CommWidgPersistent

from ui.models.MatrixListModel import MatrixListModel

from ui.views.SearchListView import NameProxy

from ui.dialogs.MatrixListDialogs import saveMatrix, saveMatrixFile#, loadMatrixFile

from ui.utils import setMaxWidth

from types import SimpleNamespace

# - TODO: Use a stackedwidget or something to swap between with 0 dimensions (1 lineedit), 1 dimension (1 row/column of lineedit), 2 dimensions (matrix of lineedits), 3+ dimensions (matrix of lineedits in selectable dimensions for columns and rows, with other dimensions selected with the spinboxes)
# TODO: Make all the hardcoded values of the columns size and selection, and replace them with an attribute

if 0 != 0:
    from src.ui.MainWindow import MainWindow
    # from MainWindow import MainWindow


class MatrixEditor(CommWidg):

    def __init__(self, parent: Optional['MainWindow'] = None):
        super().__init__(parent)
        # super(CommWidg, self)
        # QWidget.__init__(self, parent)
        self.initialized = False
        self._matrix = torch.zeros(())
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self._frameEditor = FrameEditor(self._matrix, self)
        self.__ui.scrollAreaFE.setWidget(self._frameEditor)
        self.dim0 = None
        self.dim1 = None

        self.xDimLabel = self.__ui.selectionXLabel
        self.xDimSpin = self.__ui.selectionXSpinbox
        self.xDimSpin.valueChanged.connect(self.updateDimensions_t)
        self.yDimLabel = self.__ui.selectionYLabel
        self.yDimSpin = self.__ui.selectionYSpinbox
        self.yDimSpin.valueChanged.connect(self.updateDimensions_t)

        self.__ui.dimensionsTable.horizontalHeader().geometriesChanged.connect(
            self.udtmsImpl
        )
        self.__ui.dimensionsTable.verticalHeader().geometriesChanged.connect(
            self.udtmsImpl
        )
        """
        TODO: Make the assertions/exceptions inisde fo the NNIntSI.py such that 
        nonnegative integers from the setter throw an exception, which should be catched 
        by this class or somewhere else
        TODO: Set the below changeDimensions to not use inc, dec; use the below to clone the items needed, and connect them
        """
        self._model = NNIntSIM(self)
        # self.model = QStandardItemModel(self)
        self.__ui.dimensionsTable.setModel(self._model)
        self._model.setColumnCount(2)
        self._model.setHorizontalHeaderLabels(["Size", "Selection"])

        self.changeDimensions(self.__ui.dimCountSpinBox.value())
        spbidIndex = IndexSpinBoxDelegate(self.__ui.dimensionsTable)
        spbidSize = SpinBoxDelegate(self.__ui.dimensionsTable, 1)
        self.__ui.dimensionsTable.setItemDelegateForColumn(0, spbidSize)
        self.__ui.dimensionsTable.setItemDelegateForColumn(1, spbidIndex)

        self.updateDimensionsCount(self._model.rowCount())
        self._model.dataChanged.connect(self.modelUpdateHandler)

        self.__ui.dimCountSpinBox.valueChanged.connect(self.changeDimensions)

        self._frameEditor.matrixModel.dataChanged.connect(self.logMatrix)
        self.__ui.pbLoadFile.setVisible(False)
        self.initialized = True


    # TODO: Make a system to check if last change was saved

    def setMainWindow(self, mainwindow: 'MainWindow') -> None:
        self._mainwindow = mainwindow
        mainwindow.connectSelectionChangedSignal(self.updateLoadVisibility)
        self.__ui.loadMatrixButton.clicked.connect(self.setSelectedMatrix)
        self.__ui.saveMatrixButton.clicked.connect(self.saveMatrix)
        self.updateLoadVisibility()

    def updateLoadVisibility(self):
        self.__ui.loadMatrixButton.setEnabled(
            len(self._mainwindow.getSelectedMatrix()) == 1
        )

    def saveMatrix(self):
        saveMatrix(self._matrix, self._mainwindow, self)
        # result, status = QInputDialog.getText(
        #     self, "Matrix Name", "Enter matrix name:"
        # )
        # if status:
        #     try:
        #         self.__mainwindow.addMatrix(
        #             MatrixPair(result, self.matrix.clone())
        #         )
        #     except DuplicateValueError as e:
        #         QMessageBox.warning(self, "Error", str(e))
        #     except EmptyNameError as e:
        #         QMessageBox.warning(self, "Error", str(e))
        self.isChanged.emit(self)

    def setSelectedMatrix(self):
        sel = self._mainwindow.getSelectedMatrix()
        if len(sel) == 1:
            proxyS: QSortFilterProxyModel = sel[0].model()
            indexS: QModelIndex = proxyS.mapToSource(sel[0])
            proxy: NameProxy = indexS.model()
            index = proxy.mapToSource(indexS)
            logging.info(
                # "Model: {}, Type: {}".format(
                #     index.model(), type(index.model())
                # )
                f"Model: {index.model()}, Type: {type(index.model())}"
            )
            assert (isinstance(index.model(), MatrixListModel))
            pair = index.data()
            logging.info(pair)
            self.setMatrix(pair.matrix)

    def setMatrix(self, matrix: Tensor):
        self._matrix = matrix.clone()
        self._model.removeRows(0, self._model.rowCount())
        for i in matrix.shape:
            self._model.appendRow([NNIntSI(i), NNIntSI(0)])
        self.dim0 = None
        self.dim1 = None
        self.__ui.dimCountSpinBox.setValue(matrix.dim())
        self.updateDimensions_t()

    def logMatrix(self):
        logging.debug(self._matrix)
        # pass

    def modelUpdateHandler(
        self, index0: QModelIndex, index1: QModelIndex, li: list
    ):
        i = 0
        try:
            for i in range(index0.row(), index1.row() + 1):
                # if index0.column() == 0:
                self.updateSize(i, self._model.item(i, 0).getValue())
            self.updateFrameMatrix(
                self.dim0 == self.dim1,
                (self.dim0 is not None and self.dim1 is not None) and
                self.dim0 > self.dim1
            )
        except RuntimeError as e:
            QMessageBox.warning(self, "Error", str(e))
            logging.error(self._model.item(i, 0).getValue())
            self._model.item(i, 0).revertValue()

    def udtmsImpl(self):
        # margins = self.__ui.dimensionWidget.layout().contentsMargins()
        # self.__ui.dimensionWidget.setMaximumWidth(
        #     self.__ui.dimensionsTable.horizontalHeader().length() +
        #     self.__ui.dimensionsTable.verticalHeader().width() +
        #     self.__ui.dimensionsTable.frameWidth() * 2 + margins.left() +
        #     margins.right() + 6 + (
        #         self.__ui.dimensionsTable.verticalScrollBar().width() if self.
        #         __ui.dimensionsTable.verticalScrollBar().isVisible() else 0
        #     )
        # )
        setMaxWidth(self.__ui.dimensionWidget, self.__ui.dimensionsTable)

    def getCurrentFrame(self) -> Tuple[Union[int, slice]]:
        currentFrame = []
        for i in range(self._model.rowCount()):
            if self.dim0 is not None and self.dim0 == i or self.dim1 is not None and self.dim1 == i:
                currentFrame.append(slice(None, None))
            else:
                currentFrame.append(self._model.item(i, 1).getValue())
        logging.info(tuple(currentFrame))
        return tuple(currentFrame)

    def updateFrameMatrix(self, empty: bool = False, transpose: bool = False):
        logging.info(self.getCurrentFrame())
        logging.info(self._matrix)
        matrix = self._matrix[self.getCurrentFrame()]
        self._frameEditor.updateMatrix(matrix.T if transpose else matrix)

    def changeDimensionsMatrix(self, dim):
        currentDimensions = self._model.rowCount()

        if currentDimensions == dim:
            return
        if currentDimensions < dim:
            self._matrix = self._matrix.reshape(
                self._matrix.shape +
                tuple((1 for i in range(self._matrix.dim(), dim)))
            )
        else:
            logging.info(
                f"{self._matrix=}, {tuple(slice(None, None) for i in range(dim)) + tuple(0 for i in range(dim, currentDimensions))=}"
            )
            self._matrix = self._matrix[
                tuple(slice(None, None) for i in range(dim)) +
                tuple(0 for i in range(dim, currentDimensions))]

    def changeDimensionsTable(self, dim):
        currentDimensions = self._model.rowCount()
        if currentDimensions == dim:
            return
        if currentDimensions < dim:
            for i in range(currentDimensions, dim):
                self._model.appendRow([NNIntSI(1), NNIntSI(0)])
        else:
            self._model.setRowCount(dim)

    def changeDimensions(self, dim):
        currentDimensions = self._model.rowCount()
        # logging.info(f"From: {self.matrix}")
        self.changeDimensionsMatrix(dim)
        self.changeDimensionsTable(dim)
        # logging.info(f"To: {self.matrix}")
        # logging.info(
        #     f"{self.matrix=}, {tuple(slice(None, None) for i in range(dim))=}, tuple(0 for i in range(dim, currentDimensions))"
        # )
        logging.info(f"{currentDimensions=}, {dim=}")
        self.updateDimensionsCount(dim)
        return self.updateDimensions(self._model.rowCount())

    def updateDimensions_t(self, _ = None):
        return self.updateDimensions(self._model.rowCount())

    def updateDimensions(self, dimensions: int):
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
            if self._model.rowCount() > i:
                self._model.item(i, 1).setVisibility(False)

        for i in setShow.difference(setHide):
            if self._model.rowCount() > i:
                self._model.item(i, 1).setVisibility(True)

        # TODO: Refactor this function call out of this function; this function is doing too much
        self.updateFrameMatrix(
            self.dim0 == self.dim1,
            (self.dim0 is not None and self.dim1 is not None) and
            self.dim0 > self.dim1
        )

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

    def updateSize(self, dim: int, val: int) -> None:
        # TODO: Make this change the dimensions
        if val < self._matrix.size(dim):
            self._matrix = self._matrix[tuple(
                (slice(None, None) if i != dim else slice(None, val))
                for i in range(self._matrix.dim())
            )]
        elif val > self._matrix.size(dim):
            shape = list(self._matrix.shape)
            shape[dim] = val - self._matrix.size(dim)
            self._matrix = torch.cat(
                (self._matrix, torch.zeros(shape, device = self._matrix.device)),
                dim
            )

    def getMainWindow(self):
        return self._mainwindow

    def needsTensorsTab(self) -> bool:
        return True

    def useGPU(self, use: bool):
        if use:
            self._matrix = self._matrix.to("cuda")
        else:
            self._matrix = self._matrix.to("cpu")
        # self._frameEditor.updateMatrix(self._matrix[self.getCurrentFrame()].T)
        self.updateFrameMatrix(
            self.dim0 == self.dim1,
            (self.dim0 is not None and self.dim1 is not None) and
            self.dim0 > self.dim1
        )
        self.__ui.gpuCheckBox.setText("Use GPU" if use else "Use CPU")


    def saveFile(self):
        saveMatrixFile(self._matrix.clone(), self._mainwindow)


class MatrixEditorPersistent(MatrixEditor, CommWidgPersistent):

    def __init__(self, parent: Union['MainWindow', None] = None):
        super().__init__(parent)

    # Return an object containing all the information that has to be saved to be able to restore the state of the widget and all of the models and views of the widget
    def saveState(self):
        # return {
        #     "matrix": self._matrix,
        #     "dimensions": self._model.saveState(),
        #     "frameEditor": self._frameEditor.saveState()
        # }
        s = SimpleNamespace()
        s.matrix = self._matrix.to("cpu").clone()
        smodel, s.dimensions = self._model.saveState()
        sframeEditor, s.frameEditor = self._frameEditor.saveState()
        return sframeEditor, s

    # Restore the state of the widget and all of the models and views of the widget
    def loadState(self, state: SimpleNamespace):
        # self.setMatrix(state["matrix"])
        # self._model.loadState(state["dimensions"])
        # self._frameEditor.loadState(state["frameEditor"])
        self.setMatrix(state.matrix)
        self._model.loadState(state.dimensions)
        self._frameEditor.loadState(state.frameEditor)
        self.__ui.gpuCheckBox.setChecked(self._matrix.is_cuda)
        # self._frameEditor.updateMatrix(self._matrix[self.getCurrentFrame()].T)

    # def loadFile(self):
    #     self.loadS


# TODO: Continue implementing this to support having states stored to a list (Use copilot)

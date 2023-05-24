from PySide6.QtWidgets import QMessageBox, QInputDialog, QWidget

from ui.models.MatrixListModel import MatrixPair, MatrixListModel, DuplicateValueError, EmptyNameError

from typing import Optional

import os

import logging

import torch


def saveMatrix(matrix, mainWindow, parent: Optional[QWidget] = None):
    result, status = QInputDialog.getText(
        parent, "Matrix Name", "Enter matrix name:"
    )
    if status:
        try:
            mainWindow.addMatrix(MatrixPair(result, torch.clone(matrix)))
        except DuplicateValueError as e:
            QMessageBox.warning(parent, "Error", str(e))
        except EmptyNameError as e:
            QMessageBox.warning(parent, "Error", str(e))


def saveMatrixFile(tensor, parent: Optional[MatrixListModel] = None):
    filename, status = QFileDialog.getSaveFileName(
        parent, 'Save tensor', os.getcwd(), 'TSR files (*.tsr)'
    )

    logging.info(f"status of save dialogue: {status}")

    # Check if the user cancelled the dialog box
    if not filename:
        return

    try:
        # Save the tensor to the selected file
        torch.save(tensor, filename)
        QMessageBox.information(parent, 'Saved', f'Tensor saved to {filename}')
    except Exception as e:
        QMessageBox.critical(parent, 'Error', f'Error saving tensor: {str(e)}')

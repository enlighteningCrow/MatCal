from PySide6.QtWidgets import QDialog, QAbstractButton, QApplication
from PySide6.QtCore import QSettings
from generated.designer.ui_PreferencesDialog import Ui_Dialog
from src.ui.settings import settingEntries
from src.ui.misc.setTheme import setTheme


class PreferencesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)

    def updateAxisCheckboxLabel(self, checked: bool):
        self.__ui.checkBoxAxis.setText("Use axis " + ('X' if checked else 'Y'))

    def updateIndexCheckboxLabel(self, checked: bool):
        self.__ui.checkBoxIndex.setText(
            "Use " + ('1' if checked else '0') + "-based indexing")

    def applyPreferences(self, button: QAbstractButton):
        settings = QSettings()
        if settings.value("theme") != self.__ui.comboBoxTheme.currentText():
            settings.setValue("theme", self.__ui.comboBoxTheme.currentText())
            setTheme(QApplication.instance(), settings)
        if settings.value("axis") != self.__ui.checkBoxAxis.isChecked():
            settings.setValue("axis", self.__ui.checkBoxAxis.isChecked())
            # TODO: Use the setAxis method of MatrixDataModel to change the axis it is shown
        if settings.value("index") != self.__ui.checkBoxIndex.isChecked():
            settings.setValue("index", self.__ui.checkBoxIndex.isChecked())
            # TODO: Set the index basing of the matrix models and the dimension models and the spinboxes and the connected slots
        # if self.__ui.check

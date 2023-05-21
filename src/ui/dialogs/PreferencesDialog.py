from PySide6.QtWidgets import QDialog, QDialogButtonBox
from generated.designer.ui_PreferencesDialog import Ui_Dialog

from db.GlobalSettings import settings
from utils.themes import getThemes
import logging


class PreferencesDialog(QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.populateThemes()
        settings("theme").valueChanged.connect(
            self.updateThemeComboBoxSelection
        )
        settings("theme").update()
        settings("axis").valueChanged.connect(self.updateAxisCheckbox)
        settings("axis").update()
        settings("indexing").valueChanged.connect(self.updateIndexCheckbox)
        settings("indexing").update()
        # self.__ui.buttonBox.clicked.connect(self.buttonClicked)
        self.__ui.buttonBox.button(QDialogButtonBox.Apply
                                  ).clicked.connect(self.applyPreferences)
        self.__ui.buttonBox.button(QDialogButtonBox.Ok
                                  ).clicked.connect(self.applyPreferences)

    def populateThemes(self):
        # QComboBox().clear()
        # QComboBox().
        self.__ui.comboBoxTheme.clear()
        for i in getThemes():
            self.__ui.comboBoxTheme.addItem(i)
        # self.__ui.comboBoxTheme.update()
        # self.__ui.comboBoxTheme.repaint()

    def updateThemeComboBoxSelection(self):
        self.__ui.comboBoxTheme.setCurrentText(settings("theme").get())

    def updateAxisCheckboxLabel(self, checked: bool):
        self.__ui.checkBoxAxis.setText("Use axis " + ('X' if checked else 'Y'))

    def updateAxisCheckbox(self, checked: bool):
        self.__ui.checkBoxAxis.setChecked(checked)
        self.updateAxisCheckboxLabel(checked)

    def updateIndexCheckboxLabel(self, checked: bool):
        self.__ui.checkBoxIndex.setText(
            "Use " + ('1' if checked else '0') + "-based indexing"
        )

    def updateIndexCheckbox(self, checked: bool):
        self.__ui.checkBoxIndex.setChecked(checked)
        self.updateIndexCheckboxLabel(checked)

    # def buttonClicked(self, button: QAbstractButton):
    #     if button in (self.__ui.buttonBox.button(QDialogButtonBox.Apply), self.__ui.buttonBox.button(QDialogButtonBox.Ok)):
    #         self.applyPreferences()

    def applyPreferences(self):
        # settings = QSettings()
        logging.info("Preferences applied")
        if settings("theme").get() != self.__ui.comboBoxTheme.currentText():
            settings("theme").set(self.__ui.comboBoxTheme.currentText())
            # setTheme(QApplication.instance(), settingbs)
        if settings("axis").get() != self.__ui.checkBoxAxis.isChecked():
            settings("axis").set(self.__ui.checkBoxAxis.isChecked())
            # TODO: Use the setAxis method of MatrixDataModel to change the axis it is shown
        if settings("indexing").get() != self.__ui.checkBoxIndex.isChecked():
            settings("indexing").set(self.__ui.checkBoxIndex.isChecked())
            # TODO: Set the index basing of the matrix models and the dimension models and the spinboxes and the connected slots
        # if self.__ui.check

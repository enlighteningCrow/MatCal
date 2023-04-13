# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MatrixEditor.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpinBox, QSplitter,
    QTableView, QVBoxLayout, QWidget)

from UniqueSpinBox import UniqueSpinBox

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(747, 461)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(self.widget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.dimensionWidget = QGroupBox(self.splitter)
        self.dimensionWidget.setObjectName(u"dimensionWidget")
        self.verticalLayout_2 = QVBoxLayout(self.dimensionWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.dimensionsTable = QTableView(self.dimensionWidget)
        self.dimensionsTable.setObjectName(u"dimensionsTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.dimensionsTable.sizePolicy().hasHeightForWidth())
        self.dimensionsTable.setSizePolicy(sizePolicy1)
        self.dimensionsTable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.dimensionsTable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.verticalLayout_2.addWidget(self.dimensionsTable)

        self.splitter.addWidget(self.dimensionWidget)
        self.matrixWidget = QGroupBox(self.splitter)
        self.matrixWidget.setObjectName(u"matrixWidget")
        self.gridLayout = QGridLayout(self.matrixWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.selectionXSpinbox = UniqueSpinBox(self.matrixWidget)
        self.selectionXSpinbox.setObjectName(u"selectionXSpinbox")
        self.selectionXSpinbox.setMinimum(0)
        self.selectionXSpinbox.setMaximum(0)

        self.gridLayout.addWidget(self.selectionXSpinbox, 0, 1, 1, 1)

        self.selectionYLabel = QLabel(self.matrixWidget)
        self.selectionYLabel.setObjectName(u"selectionYLabel")

        self.gridLayout.addWidget(self.selectionYLabel, 1, 0, 1, 1)

        self.selectionXLabel = QLabel(self.matrixWidget)
        self.selectionXLabel.setObjectName(u"selectionXLabel")
        self.selectionXLabel.setEnabled(True)

        self.gridLayout.addWidget(self.selectionXLabel, 0, 0, 1, 1)

        self.selectionYSpinbox = UniqueSpinBox(self.matrixWidget)
        self.selectionYSpinbox.setObjectName(u"selectionYSpinbox")
        self.selectionYSpinbox.setMinimum(0)
        self.selectionYSpinbox.setMaximum(0)

        self.gridLayout.addWidget(self.selectionYSpinbox, 1, 1, 1, 1)

        self.scrollAreaFE = QScrollArea(self.matrixWidget)
        self.scrollAreaFE.setObjectName(u"scrollAreaFE")
        sizePolicy1.setHeightForWidth(self.scrollAreaFE.sizePolicy().hasHeightForWidth())
        self.scrollAreaFE.setSizePolicy(sizePolicy1)
        self.scrollAreaFE.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 174, 256))
        self.scrollAreaFE.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollAreaFE, 2, 0, 1, 2)

        self.splitter.addWidget(self.matrixWidget)

        self.gridLayout_2.addWidget(self.splitter, 2, 0, 1, 2)

        self.dimCountLabel = QLabel(self.widget)
        self.dimCountLabel.setObjectName(u"dimCountLabel")

        self.gridLayout_2.addWidget(self.dimCountLabel, 0, 0, 1, 1)

        self.dimCountSpinBox = QSpinBox(self.widget)
        self.dimCountSpinBox.setObjectName(u"dimCountSpinBox")
        self.dimCountSpinBox.setMaximum(1000000)

        self.gridLayout_2.addWidget(self.dimCountSpinBox, 0, 1, 1, 1)


        self.horizontalLayout.addWidget(self.widget)

        self.saveLoadButtons = QWidget(Form)
        self.saveLoadButtons.setObjectName(u"saveLoadButtons")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.saveLoadButtons.sizePolicy().hasHeightForWidth())
        self.saveLoadButtons.setSizePolicy(sizePolicy2)
        self.gridLayout_3 = QGridLayout(self.saveLoadButtons)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.loadMatrixButton = QPushButton(self.saveLoadButtons)
        self.loadMatrixButton.setObjectName(u"loadMatrixButton")

        self.gridLayout_3.addWidget(self.loadMatrixButton, 0, 0, 1, 1)

        self.saveMatrixButton = QPushButton(self.saveLoadButtons)
        self.saveMatrixButton.setObjectName(u"saveMatrixButton")

        self.gridLayout_3.addWidget(self.saveMatrixButton, 1, 0, 1, 1)


        self.horizontalLayout.addWidget(self.saveLoadButtons)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.dimensionWidget.setTitle(QCoreApplication.translate("Form", u"Dimensions", None))
        self.matrixWidget.setTitle(QCoreApplication.translate("Form", u"Matrix", None))
        self.selectionYLabel.setText(QCoreApplication.translate("Form", u"Selection Y:", None))
        self.selectionXLabel.setText(QCoreApplication.translate("Form", u"Selection X:", None))
        self.dimCountLabel.setText(QCoreApplication.translate("Form", u"Number of Dimensions", None))
        self.loadMatrixButton.setText(QCoreApplication.translate("Form", u"Load Matrix", None))
        self.saveMatrixButton.setText(QCoreApplication.translate("Form", u"Save Matrix", None))
    # retranslateUi


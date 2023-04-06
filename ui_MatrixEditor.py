# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MatrixEditor.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QGroupBox, QHeaderView, QLabel, QScrollArea,
    QSizePolicy, QSpinBox, QSplitter, QTableView,
    QVBoxLayout, QWidget)

from UniqueSpinBox import UniqueSpinBox

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.dimCountLabel = QLabel(self.frame)
        self.dimCountLabel.setObjectName(u"dimCountLabel")

        self.gridLayout_2.addWidget(self.dimCountLabel, 0, 0, 1, 1)

        self.dimCountSpinBox = QSpinBox(self.frame)
        self.dimCountSpinBox.setObjectName(u"dimCountSpinBox")
        self.dimCountSpinBox.setMaximum(1000000)

        self.gridLayout_2.addWidget(self.dimCountSpinBox, 0, 1, 1, 1)

        self.splitterEditor = QSplitter(self.frame)
        self.splitterEditor.setObjectName(u"splitterEditor")
        self.splitterEditor.setOrientation(Qt.Horizontal)
        self.dimensionWidget = QGroupBox(self.splitterEditor)
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

        self.splitterEditor.addWidget(self.dimensionWidget)
        self.matrixWidget = QGroupBox(self.splitterEditor)
        self.matrixWidget.setObjectName(u"matrixWidget")
        self.gridLayout = QGridLayout(self.matrixWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.selectionXLabel = QLabel(self.matrixWidget)
        self.selectionXLabel.setObjectName(u"selectionXLabel")
        self.selectionXLabel.setEnabled(True)

        self.gridLayout.addWidget(self.selectionXLabel, 0, 0, 1, 1)

        self.selectionYLabel = QLabel(self.matrixWidget)
        self.selectionYLabel.setObjectName(u"selectionYLabel")

        self.gridLayout.addWidget(self.selectionYLabel, 1, 0, 1, 1)

        self.selectionXSpinbox = UniqueSpinBox(self.matrixWidget)
        self.selectionXSpinbox.setObjectName(u"selectionXSpinbox")

        self.gridLayout.addWidget(self.selectionXSpinbox, 0, 1, 1, 1)

        self.selectionYSpinbox = UniqueSpinBox(self.matrixWidget)
        self.selectionYSpinbox.setObjectName(u"selectionYSpinbox")

        self.gridLayout.addWidget(self.selectionYSpinbox, 1, 1, 1, 1)

        self.scrollAreaFE = QScrollArea(self.matrixWidget)
        self.scrollAreaFE.setObjectName(u"scrollAreaFE")
        sizePolicy1.setHeightForWidth(self.scrollAreaFE.sizePolicy().hasHeightForWidth())
        self.scrollAreaFE.setSizePolicy(sizePolicy1)
        self.scrollAreaFE.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 135, 93))
        self.scrollAreaFE.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollAreaFE, 2, 0, 1, 2)

        self.splitterEditor.addWidget(self.matrixWidget)

        self.gridLayout_2.addWidget(self.splitterEditor, 1, 0, 1, 2)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.dimCountLabel.setText(QCoreApplication.translate("Form", u"Number of Dimensions", None))
        self.dimensionWidget.setTitle(QCoreApplication.translate("Form", u"Dimensions", None))
        self.matrixWidget.setTitle(QCoreApplication.translate("Form", u"Matrix", None))
        self.selectionXLabel.setText(QCoreApplication.translate("Form", u"Selection X:", None))
        self.selectionYLabel.setText(QCoreApplication.translate("Form", u"Selection Y:", None))
    # retranslateUi


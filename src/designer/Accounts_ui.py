# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Accounts.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lUsername = QLabel(Form)
        self.lUsername.setObjectName(u"lUsername")

        self.verticalLayout.addWidget(self.lUsername)

        self.leUsername = QLineEdit(Form)
        self.leUsername.setObjectName(u"leUsername")

        self.verticalLayout.addWidget(self.leUsername)

        self.lPassword = QLabel(Form)
        self.lPassword.setObjectName(u"lPassword")

        self.verticalLayout.addWidget(self.lPassword)

        self.lePassword = QLineEdit(Form)
        self.lePassword.setObjectName(u"lePassword")

        self.verticalLayout.addWidget(self.lePassword)

        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plLogin = QPushButton(self.page)
        self.plLogin.setObjectName(u"plLogin")

        self.verticalLayout_2.addWidget(self.plLogin)

        self.plCreateAccount = QPushButton(self.page)
        self.plCreateAccount.setObjectName(u"plCreateAccount")

        self.verticalLayout_2.addWidget(self.plCreateAccount)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_3 = QVBoxLayout(self.page_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pcAccountType = QLabel(self.page_2)
        self.pcAccountType.setObjectName(u"pcAccountType")

        self.verticalLayout_3.addWidget(self.pcAccountType)

        self.pcCbAccountType = QComboBox(self.page_2)
        self.pcCbAccountType.setObjectName(u"pcCbAccountType")

        self.verticalLayout_3.addWidget(self.pcCbAccountType)

        self.pcCreateAccount = QPushButton(self.page_2)
        self.pcCreateAccount.setObjectName(u"pcCreateAccount")

        self.verticalLayout_3.addWidget(self.pcCreateAccount)

        self.pcLogin = QPushButton(self.page_2)
        self.pcLogin.setObjectName(u"pcLogin")

        self.verticalLayout_3.addWidget(self.pcLogin)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lUsername.setText(QCoreApplication.translate("Form", u"Username:", None))
        self.lPassword.setText(QCoreApplication.translate("Form", u"Password", None))
        self.plLogin.setText(QCoreApplication.translate("Form", u"Login", None))
        self.plCreateAccount.setText(QCoreApplication.translate("Form", u"Create Account", None))
        self.pcAccountType.setText(QCoreApplication.translate("Form", u"Account Type", None))
        self.pcCreateAccount.setText(QCoreApplication.translate("Form", u"Create Account", None))
        self.pcLogin.setText(QCoreApplication.translate("Form", u"Login", None))
    # retranslateUi


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from db.Storage import getProperty

from persistent.list import PersistentList as plist

from BTrees.OOBTree import OOBTree

from ui.MainWindow import MainWindow

from generated.designer.ui_Accounts import Ui_Form

import persistent

class Account(persistent.Persistent):
    accountTypes = {"Admin" : ["Manage"], "School Student": ["Calculator"], "Computer Scientist": ["Calculator", "Graphing", "Programming"], "Mathematician": ["Calculator", "Graphing", "Programming", "Statistics"], "Data Scientist": ["Calculator", "Matrix Editor", "Matrix Calculation"]}
    def __init__(self, username, password, account_type):
        self.username = username
        self.password = password
        self.account_type = account_type
        self.states = plist()

    def __str__(self):
        return f"Username: {self.username}\nPassword: {self.password}\nAccount Type: {self.account_type}"


class Accounts(QWidget):
    # List the account types of users of a calculator system and the tabs that should be shown to them
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__ui.pcCbAccountType.addItems(Account.accountTypes.keys())
        self.__ui.pcCreateAccount.clicked.connect(self.create_account)
        self.__ui.plLogin.clicked.connect(self.login)
        self.__ui.pcLogin.clicked.connect(lambda : self.__ui.stackedWidget.setCurrentIndex(0))
        self.__ui.plCreateAccount.clicked.connect(lambda : self.__ui.stackedWidget.setCurrentIndex(1))

    def create_account(self):
        username = self.__ui.leUsername.text()
        password = self.__ui.lePassword.text()
        account_type = self.__ui.pcCbAccountType.currentText()

        # Check if an account with the username already exists
        account_list = getProperty('accounts', OOBTree())
        if account_list.get(username) is not None:
            QMessageBox.critical(self, "Error", "Username already exists.")
            return

        # Create a new account object
        new_account = Account(username, password, account_type)
        account_list[username] = new_account

        print("Accounts:")
        for i in account_list:
            print(f"{i}: {account_list[i]}")

    def login(self):
        username = self.__ui.leUsername.text()
        password = self.__ui.lePassword.text()

        # Check if the username and password match an account
        account_list = getProperty('accounts', OOBTree())
        if username in account_list:
            if account_list[username].password == password:
                main_window = MainWindow()
                main_window.show()
                # sleep(1000)
                self.hide()
                return

        QMessageBox.critical(self, "Error", "Invalid username or password.")
        print("Accounts:")
        for i in account_list:
            print(f"{i}: {account_list[i]}")
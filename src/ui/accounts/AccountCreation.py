from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from db.Storage import getProperty

from persistent.list import PersistentList as plist

from BTrees.OOBTree import OOBTree

from generated.designer.ui_Accounts import Ui_Form

import persistent

from typing import List

DEBUG = True

class Account(persistent.Persistent):
    accountTypes = {"Admin": ["AdminPage"], "School Student": ["Calculator", "LinearSolver"], "Computer Scientist": ["Calculator", "MatrixEditor", "MatrixCalculation", "BinaryCalculator"], "Mathematician": ["Calculator", "LinearSolver"], "Data Scientist": ["Calculator", "MatrixEditor", "MatrixCalculation", "LinearSolver", "BinaryCalculator"]}
    def __init__(self, username, password, account_type):
        self.username = username
        self.password = password
        self.account_type = account_type
        self.states : List[State] = plist()

    def __str__(self):
        return f"Username: {self.username}\nPassword: {self.password}\nAccount Type: {self.account_type}"

    def getTabs(self):
        return Account.accountTypes[self.account_type]


from ui.models.StatesListModel import State

class Accounts(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__ui.pcCbAccountType.addItems(Account.accountTypes.keys())
        self.__ui.pcCreateAccount.clicked.connect(self.create_account)
        self.__ui.plLogin.clicked.connect(self.login)
        self.__ui.pcLogin.clicked.connect(lambda: self.__ui.stackedWidget.setCurrentIndex(0))
        self.__ui.plCreateAccount.clicked.connect(lambda: self.__ui.stackedWidget.setCurrentIndex(1))

    def create_account(self):
        username = self.__ui.leUsername.text()
        password = self.__ui.lePassword.text()

        if min(len(username), len(password)) == 0:
            QMessageBox.critical(self, "Error", "Username and password cannot be empty.")
            return
        account_type = self.__ui.pcCbAccountType.currentText()

        # Check if an account with the username already exists
        account_list = getProperty('accounts', OOBTree())
        if account_list.get(username) is not None:
            QMessageBox.critical(self, "Error", "Username already exists.")
            return

        # Create a new account object
        new_account = Account(username, password, account_type)
        account_list[username] = new_account
        account_list._p_changed = True

        if DEBUG:
            print("Accounts:")
            for username, account in account_list.items():
                print(f"{username}: {account}")

        # Show the login page
        self.__ui.stackedWidget.setCurrentIndex(0)
        QMessageBox.information(self, "Success", "Account created successfully.")

    def login(self):
        username = self.__ui.leUsername.text()
        password = self.__ui.lePassword.text()

        # Check if the username and password match an account
        account_list = getProperty('accounts', OOBTree())
        if username in account_list:
            account = account_list[username]
            if account.password == password:
                if not isinstance(account.states, plist):
                    account.states = plist()
                else:
                    # for i in range(len(account.states)):
                    #     if not isinstance(account.states[i], State):
                    #         account.states[i] = State()
                    # Iterate over the list in reverse order
                    for i in range(len(account.states) - 1, -1, -1):
                        if not isinstance(account.states[i], State):
                            account.states.pop(i)

                    # print(account.states)


                from main import onLoginComplete
                onLoginComplete(account)
                self.hide()
                return

        QMessageBox.critical(self, "Error", "Invalid username or password.")

        if DEBUG:
            print("Accounts:")
            for username, account in account_list.items():
                print(f"{username}: {account}")

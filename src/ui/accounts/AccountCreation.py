from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from db.Storage import getProperty

from persistent.list import PersistentList as plist

from BTrees.OOBTree import OOBTree

from ui.MainWindow import MainWindow

class CreateAccountPage(QWidget):
    def __init__(self, login_page):
        super().__init__()

        self.login_page = login_page

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Username input
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        # Password input
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        # Account type selection
        type_label = QLabel("Account Type:")
        self.type_input = QLineEdit()
        layout.addWidget(type_label)
        layout.addWidget(self.type_input)

        # Create account button
        create_button = QPushButton("Create Account")
        create_button.clicked.connect(self.create_account)
        layout.addWidget(create_button)

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()
        account_type = self.type_input.text()

        # Check if the username already exists
        account_list = getProperty('accounts', PersistentList())
        for account in account_list:
            if account['username'] == username:
                QMessageBox.critical(self, "Error", "Username already exists.")
                return

        # Create a new account dictionary
        new_account = {'username': username, 'password': password, 'type': account_type}
        account_list.append(new_account)
        transaction.commit()

        # Show login page
        self.login_page.show()
        self.close()

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Username input
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        # Password input
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        # Create account button
        create_button = QPushButton("Create Account")
        create_button.clicked.connect(self.create_account)
        layout.addWidget(create_button)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Check if the username and password match an account
        account_list = getProperty('accounts', PersistentList())
        for account in account_list:
            if account['username'] == username and account['password'] == password:
                # Close login page and show MainWindow
                self.close()
                main_window = MainWindow()
                main_window.show()
                return

        QMessageBox.critical(self, "Error", "Invalid username or password.")

    def create_account(self):
        # Show create account page
        create_page = CreateAccountPage(self)
        create_page.show()
        self.hide()


from generated.designer.ui_Accounts import Ui_Form

class Account:
    def __init__(self, username, password, account_type):
        self.username = username
        self.password = password
        self.account_type = account_type

    def __str__(self):
        return f"Username: {self.username}\nPassword: {self.password}\nAccount Type: {self.account_type}"



class Accounts(QWidget):
    # List the account types of users of a calculator system and the tabs that shuold be shown to them
    accountTypes = {"Admin" : ["Manage"], "School Student": ["Calculator"], "Computer Scientist": ["Calculator", "Graphing", "Programming"], "Mathematician": ["Calculator", "Graphing", "Programming", "Statistics"], "Data Scientist": ["Calculator", "Matrix Editor", "Matrix Calculation"]}
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.__ui.pcCbAccountType.addItems(self.accountTypes.keys())
        self.__ui.pcCreateAccount.clicked.connect(self.create_account)
        self.__ui.plLogin.clicked.connect(self.login)
        self.__ui.pcLogin.clicked.connect(lambda : self.__ui.stackedWidget.setCurrentIndex(0))
        self.__ui.plCreateAccount.clicked.connect(lambda : self.__ui.stackedWidget.setCurrentIndex(1))

    # def 

    def create_account(self):
        username = self.__ui.leUsername.text()
        password = self.__ui.lePassword.text()
        account_type = self.__ui.pcCbAccountType.currentText()

        # Check if the username already exists
        account_list = getProperty('accounts', OOBTree())
        if account_list.get(username) is not None:
            QMessageBox.critical(self, "Error", "Username already exists.")
            return
        # for account in account_list:
        #     if account['username'] == username:
        #         QMessageBox.critical(self, "Error", "Username already exists.")
        #         return

        # Create a new account dictionary
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
        # for account in account_list:
        #     if account['username'] == username and account['password'] == password:
        #         # Close login page and show MainWindow
        #         main_window = MainWindow()
        #         main_window.show()
        #         # sleep(1000)
        #         self.hide()
        #         return
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
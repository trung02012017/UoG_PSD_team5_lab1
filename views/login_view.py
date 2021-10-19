import time

from views.view import View
from views.customer_view import CustomerView
from views.operator_view import OperatorView
from views.manager_view import ManagerView

from utils.util_funcs import *


class LoginView(View):
    def __init__(self):
        super().__init__()
        self.option_mapping = {
            "1": {
                "option_name": "Customer",
                "option_view": CustomerView()
            },
            "2": {
                "option_name": "Operator",
                "option_view": OperatorView()
            },
            "3": {
                "option_name": "Manager",
                "option_view": ManagerView()
            },
            "4": {
                "option_name": "Exit"
            }
        }

    def show_input_screen(self):
        while True:
            role = input("Your role is: ")

            try:
                if role == "4":
                    exit()
                role_view = self.option_mapping[role]["option_view"]
                clear_console()
                while self.login_status is not True:
                    self.login_status, message = role_view.show_login()
                    print(message)
                    time.sleep(1)

                clear_console()
                role_view.show_menu()
                role_view.show_input_screen()
                self.login_status = False
                self.redirect()
            except KeyError:
                print("Cannot specify your role. Please try again")
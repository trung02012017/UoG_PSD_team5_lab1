from utils.util_funcs import *


class View:
    def __init__(self):
        self.login_status = False
        self.option_mapping = {}

    def show_login(self):
        pass

    def show_menu(self):
        for k, v in self.option_mapping.items():
            print(f"{k}. {v['option_name']}")

    def show_input_screen(self):
        pass

    def redirect(self):
        clear_console()
        self.show_menu()
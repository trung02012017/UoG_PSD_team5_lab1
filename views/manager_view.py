from views.view import View


def report_view():
    pass


def log_out_view():
    pass


class ManagerView(View):
    def __init__(self):
        super().__init__()
        self.option_mapping = {
            "1": {
                "option_name": "Report",
                "option_func": report_view
            },
            "2": {
                "option_name": "Log out",
                "option_func": log_out_view
            },
        }

    def show_input_screen(self):
        while True:
            option = input("Enter your option: ")

            try:
                option_func = self.option_mapping[option]["option_func"]
                print(option_func.__name__)
                option_func()
                if option_func.__name__ == "log_out_view":
                    break
                self.redirect()
            except KeyError:
                print("Cannot specify your option. Please try again")
from utils.util_funcs import connect_database
from models.manager import ManagerModel


class ManagerController:
    def __init__(self):
        self.conn = connect_database()
        self.customer_model = ManagerModel(self.conn)

    def report(self):
        pass


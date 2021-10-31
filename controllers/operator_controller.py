from utils.util_funcs import connect_database
from models.operator import OperatorModel

from datetime import datetime


class OperatorController:
    def __init__(self):
        self.conn = connect_database()
        self.operator_model = OperatorModel(self.conn)

    def track_bike(self):
        return self.operator_model.get_all_bikes_info()

    def get_postcode_by_location_id(self, location_id):
        return self.operator_model.get_postcode_by_location_id(location_id)

    def get_bike_rental_status(self, bike_id):
        check_rental = self.operator_model.get_bike_rental_status(bike_id)
        return check_rental

    def get_broken_bikes(self):
        return self.operator_model.get_broken_bikes()

    def repair_bike(self, bike_id):
        self.operator_model.update_repaired_bike(bike_id)
        action_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.operator_model.insert_operator_activity(bike_id,
                                                     action_name='repair',
                                                     action_time=action_time)

    def get_all_locations(self):
        return self.operator_model.get_all_locations()

    def move_bike(self, bike_id, location_id):
        self.operator_model.update_bike_location(bike_id, location_id)
        action_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.operator_model.insert_operator_activity(bike_id,
                                                     action_name='move',
                                                     action_time=action_time)

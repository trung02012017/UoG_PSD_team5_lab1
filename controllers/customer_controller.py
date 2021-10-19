import pandas as pd

from datetime import datetime

from utils.util_funcs import connect_database, check_username
from models.customer import CustomerModel

import time


class CustomerController:
    def __init__(self):
        self.conn = connect_database()
        self.customer_model = CustomerModel(self.conn)
        self.customer_info = {}

    def check_login(self, username, password):
        found_customer = self.customer_model.find_customer(username, password)
        if found_customer.shape[0] == 0:
            return False, 'username or password is wrong !'
        else:
            customer_info = found_customer.columns
            for info in customer_info:
                self.customer_info[info] = found_customer.iloc[0][info]
            return True, 'Login successfully'

    def sign_up(self, username, password, confirm_password, card_number):
        if not check_username(username):
            return False, 'Invalid email, sign up failed !!!'
        if password != confirm_password:
            return False, 'Password confirmation failed !!!'
        found_customer = self.customer_model.find_customer_by_username(username)
        if found_customer.shape[0] > 0:
            return False, 'Email existed, sign up failed !!!'
        else:
            new_customer = self.customer_model.add_new_customer(username, password, card_number)
            customer_info = new_customer.columns
            for info in customer_info:
                self.customer_info[info] = new_customer.iloc[0][info]
            return True, 'Sign up successfully !'

    def check_rent(self):
        customer = self.customer_model.find_customer_by_id(self.customer_info['customerID'])
        rental_status = customer.iloc[0]['rental_status']

        if rental_status == 1:
            return True
        else:
            return False

    def get_all_locations(self):
        return self.customer_model.get_all_locations()

    def get_bikes_by_location(self, location_id):
        return self.customer_model.get_bikes_by_location(location_id)

    def rent_bike(self, bike_id, location_id):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.customer_model.add_new_customer_act(self.customer_info['customerID'], bike_id, start_time, location_id)
        self.customer_model.update_customer_rental_status(self.customer_info['customerID'], 1)

    def get_latest_act(self):
        return self.customer_model.get_latest_act(self.customer_info['customerID'])

    def get_account_total(self):
        return self.customer_model.get_account_total(self.customer_info['customerID'])

    def return_bike(self, act_id,
                    bike_id,
                    end_time,
                    end_location,
                    charged,
                    remaining_account,
                    paid,
                    rental_status):
        self.customer_model.update_return_act(act_id, end_time, end_location, charged, paid)
        self.customer_model.update_bike_location(bike_id, end_location)
        self.customer_model.update_customer_account(self.customer_info['customerID'], remaining_account, rental_status)

    def manage_account(self):
        pass

    def report_bike(self, bike_id, bike_cond):
        self.customer_model.update_bike_status(bike_id, bike_cond)

    def write_review(self):
        pass

    def update_details(self, field_name, value):
        self.customer_model.update_details(self.customer_info['customerID'], field_name, value)
        self.customer_info[field_name] = value

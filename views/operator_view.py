import time
import pandas as pd

from configs.other_config import operator_password
from views.view import View

from controllers.operator_controller import OperatorController


def log_in_view():
    password = input("Enter password: ")
    if password == operator_password:
        return True
    else:
        return False


def show_locations(operator_controller: OperatorController):

    bike_stops = operator_controller.get_all_locations()

    print("List of location: ")
    for i, row in bike_stops.iterrows():
        location_id = row['locationID']
        location_postcode = row['postCode']
        print(f"{location_id}. {location_postcode} bike stops - location ID: {location_id}")

    while True:
        location_id = input("Please enter the number related to your current location: ")

        if location_id not in [str(i) for i in bike_stops['locationID']]:
            continue
        else:
            return location_id


def track_bike_view(operator_controller: OperatorController):
    bikes_info = operator_controller.track_bike()
    bike_locations = []

    for i, row in bikes_info.iterrows():
        bike_id = row['bikeID']
        check_rental_status = operator_controller.get_bike_rental_status(bike_id)

        if check_rental_status == 'Available':
            bike_locations.append(row['locationID'])
        else:
            bike_locations.append('Currently rent')

    bikes_info['locationID'] = bike_locations

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(bikes_info)

    _ = input('Press something to redirect to main menu: ')
    print("redirecting....")
    time.sleep(1)


def repair_bike_view(operator_controller: OperatorController):
    broken_bikes = operator_controller.get_broken_bikes()
    if broken_bikes.shape[0] == 0:
        print("All bikes are in a good condition")
        _ = input("Enter something to redirect to the main menu: ")
        print("Redirecting ...")
        time.sleep(1)
    else:
        while True:
            print("List of broken bikes:")
            for i, row in broken_bikes.iterrows():
                print(f"{i + 1}. BikeID: {row['bikeID']}, currently in locationID: {row['locationID']}")

            option = input("Choose a bike to repair: ")
            if option not in [str(i + 1) for i in range(broken_bikes.shape[0])]:
                print("Cannot specify your option. Please try again")
                continue
            else:
                bike_id = broken_bikes.iloc[int(option) - 1]['bikeID']
                print("Repairing...")
                operator_controller.repair_bike(bike_id)
                time.sleep(1)
                print("Repair done !")
                break


def move_bike_view(operator_controller: OperatorController):
    bikes_info = operator_controller.track_bike()
    bike_locations = []

    for i, row in bikes_info.iterrows():
        bike_id = row['bikeID']
        check_rental_status = operator_controller.get_bike_rental_status(bike_id)

        if check_rental_status == 'Available':
            bike_locations.append(row['locationID'])
        else:
            bike_locations.append('Currently rent')

    bikes_info['locationID'] = bike_locations

    while True:
        print("List of bikes")
        for i, row in bikes_info.iterrows():
            print(f"{i + 1}. BikeID: {row['bikeID']}, currently in locationID: {row['locationID']}")

        option = input("Choose a bike to move: ")
        if option not in [str(i + 1) for i in range(bikes_info.shape[0])]:
            print("Cannot specify your option. Please try again")
            continue
        else:
            bike_id = bikes_info.iloc[int(option) - 1]['bikeID']
            if bikes_info.iloc[int(option) - 1]['locationID'] == 'Currently rent':
                print('Cannot move the bike because it is currently in use !!!')
            else:
                location_id = show_locations(operator_controller)
                print("Moving bike ...")
                operator_controller.move_bike(bike_id, location_id)
                time.sleep(1)
                print("Done moving !")
            break


def log_out_view(operator_controller: OperatorController = None):
    pass


class OperatorView(View):
    def __init__(self):
        super().__init__()
        self.operator_controller = OperatorController()
        self.option_mapping = {
            "1": {
                "option_name": "Track bike",
                "option_func": track_bike_view
            },
            "2": {
                "option_name": "Repair bike",
                "option_func": repair_bike_view
            },
            "3": {
                "option_name": "Move bike",
                "option_func": move_bike_view
            },
            "4": {
                "option_name": "Log out",
                "option_func": log_out_view
            }
        }

    def show_login(self):
        print("Hello Operator! ")
        print("1. Enter password")
        print("2. Log out")
        while True:
            option = input("Enter your option: ")

            if option == "1":
                check_pass = log_in_view()
                if check_pass:
                    print("Login successfully !")
                    time.sleep(1)
                    return True, ''
                else:
                    return False, 'Login failed because of wrong password !'
            elif option == "2":
                return False, 'Log out'
            else:
                print("Cannot specify your option. Please try again")

    def show_input_screen(self):
        while True:
            option = input("Enter your option: ")

            try:
                option_func = self.option_mapping[option]["option_func"]
                print(option_func.__name__)
                option_func(self.operator_controller)
                if option_func.__name__ == "log_out_view":
                    time.sleep(1)
                    break
                self.redirect()
            except KeyError:
                print("Cannot specify your option. Please try again")
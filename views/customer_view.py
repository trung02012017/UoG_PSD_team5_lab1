import math
from datetime import datetime

from configs.other_config import *
from views.view import View
from controllers.customer_controller import CustomerController


def log_in_view(customer_controller: CustomerController):
    print("Please enter your username and password:")

    username = input("USERNAME: ")
    password = input("PASSWORD: ")

    check_res, message = customer_controller.check_login(username, password)
    return check_res, message


def sign_up_view(customer_controller: CustomerController):
    username = input("USERNAME: ")
    password = input("PASSWORD: ")
    confirm_password = input("Confirm password: ")
    card_number = input("Card number: ")

    check_sign_up, message = customer_controller.sign_up(username, password, confirm_password, card_number)
    return check_sign_up, message


def top_up_account_view(customer_controller: CustomerController):
    print(f"Your current account balance: £{customer_controller.customer_info['account_total']}")
    print(f"Your card number: {customer_controller.customer_info['card_details']}")
    expired_date = input("Enter card expired date: ")
    cvv_code = input("Enter cvv code: ")

    while True:
        try:
            amount_top_up = input("Amount to top up: £")
            amount_top_up = float(amount_top_up)
            customer_controller.manage_account(amount_top_up)
            print(f"Top up done ! Your account balance is now £{customer_controller.customer_info['account_total']}")
            input("Press something to redirect to main menu ...")
            break
        except Exception as e:
            print("Please enter a valid number !!!")


def manage_account_view(customer_controller: CustomerController):
    print(f"Your current account balance: £{customer_controller.customer_info['account_total']}")
    while True:
        print("1. Top up your account")
        print("2. Main menu")

        option = input("Select one: ")

        if option not in ['1', '2']:
            print("Please enter 1 or 2")
        else:
            if option == '1':
                top_up_account_view(customer_controller)
            else:
                input("Press something to redirect to main menu ...")
            break


def show_locations(customer_controller: CustomerController):

    bike_stops = customer_controller.get_all_locations()

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


def show_bike_by_location(customer_controller: CustomerController, location_id):
    bikes = customer_controller.get_bikes_by_location(location_id)

    for i, row in bikes.iterrows():
        bike_id = row['bikeID']
        print(f"{bike_id}. Bike {bike_id}")

    while True:
        bike_id = input("Please enter the bike number: ")

        if bike_id not in [str(i) for i in bikes['bikeID']]:
            continue
        else:
            return bike_id


def rent_bike_view(customer_controller: CustomerController):
    rental_status = customer_controller.check_rent()

    if rental_status:
        print("You are renting a bike. Please return it before renting another one !!!")
    else:
        location_id = show_locations(customer_controller)
        bike_id = show_bike_by_location(customer_controller, location_id)

        customer_controller.rent_bike(bike_id, location_id)
        print("Rent done ! Thank you")
    input("Press something to redirect to main menu ...")


def pay_charged_view(current_amount, time_duration_in_h, charged):

    print(f"Your current account: £{current_amount}")
    print(f"Real time renting bike: {time_duration_in_h} hours")
    print(f"Charged time renting bike: {math.ceil(time_duration_in_h)} hours")
    print(f"You have to pay: £{charged} (with £{pay_per_hour} per hour)")

    _ = input("Enter somthing to make payment: ")

    print("Making payment done !")
    input("Press something to redirect to main menu ...")


def return_bike_view(customer_controller: CustomerController):
    latest_act = customer_controller.get_latest_act()
    if latest_act.shape[0] > 0:
        location_id = show_locations(customer_controller)

        act_id = latest_act.iloc[0]['ActID']
        bike_id = latest_act.iloc[0]['bikeID']
        start_time = latest_act.iloc[0]['startTime']
        end_time = datetime.now()

        time_duration_in_s = (end_time - start_time).total_seconds()
        time_duration_in_h = time_duration_in_s / 3600
        charged = pay_per_hour * int(math.ceil(time_duration_in_h))

        current_amount = customer_controller.get_account_total()

        pay_charged_view(current_amount, time_duration_in_h, charged)

        check_account = current_amount >= charged
        if check_account:
            customer_controller.return_bike(act_id,
                                            bike_id,
                                            end_time,
                                            location_id,
                                            charged,
                                            current_amount - charged,
                                            1,
                                            0)
            print("Return done completely !")
        else:
            print("Your current account is too low. Please top up your account")
    else:
        print("You are not renting a bike !!!")
    input("Enter something to redirect to the main menu ...")


def report_bike_view(customer_controller: CustomerController):
    latest_act = customer_controller.get_latest_act_done()
    bike_id = latest_act.iloc[0]['bikeID']

    print(f"Your latest journey is with bike id: {bike_id}. Is the bike now broken ?")
    print("1. No")
    print("2. Yes")

    while True:
        bike_cond_input = input("Select one: ")

        if bike_cond_input not in ['1', '2']:
            print("Please select '1' or '2' ")
        else:
            if bike_cond_input == '1':
                bike_cond = "good"
            else:
                bike_cond = "broken"

            break

    print("Updating bike status ...")
    customer_controller.report_bike(bike_id, bike_cond)
    input("Press something to redirect to main menu ...")


def write_review_view(customer_controller: CustomerController):
    last_journey = customer_controller.get_latest_act_done()
    if last_journey.shape[0] == 0:
        print("You have not had any journey. Please take a bike !")
        _ = input("Enter something to exit: ")
    else:
        bike_id = last_journey.iloc[0]['bikeID']
        star = 5
        while True:
            star = input("Rating your last journey (Rating 1-5): ")
            if star not in ['1', '2', '3', '4', '5']:
                print("Please enter a number in 1-5 !!!")
            else:
                break

        review = input("Write a review: ")

        customer_controller.write_review(bike_id, star, review)
        print("Thanks for your review !")
        _ = input("Enter something to exit: ")


def update_details_view(customer_controller: CustomerController):
    print(f"1. Password: {customer_controller.customer_info['password']}")
    print(f"2. Card detail: {customer_controller.customer_info['card_details']}")
    print("3. Return")
    while True:
        option = input("Select one: ")

        if option == '3':
            break

        if option not in ['1', '2']:
            print("Please select 1 or 2")
        else:
            if option == '1':
                while True:
                    new_pass = input("New password: ")
                    confirm_pass = input("Confirm password: ")

                    if new_pass == confirm_pass:
                        customer_controller.update_details('password', new_pass)
                        break
                    else:
                        print("confirm password failed !!!")
                        continue

            else:
                while True:
                    new_pass = input("New card number: ")
                    confirm_pass = input("Confirm card number: ")

                    if new_pass == confirm_pass:
                        customer_controller.update_details('card_details', new_pass)
                        break
                    else:
                        print("confirm card number failed !!!")
                        continue
            print("Information updated")
            input("Press something to redirect to main menu ...")
            break


def log_out_view(customer_controller):
    customer_controller.customer_info = {}
    pass


class CustomerView(View):
    def __init__(self):
        super().__init__()
        self.customer_controller = CustomerController()
        self.option_mapping = {
            "1": {
                "option_name": "Top up account",
                "option_func": manage_account_view
            },
            "2": {
                "option_name": "Rent bike",
                "option_func": rent_bike_view
            },
            "3": {
                "option_name": "Return bike",
                "option_func": return_bike_view
            },
            "4": {
                "option_name": "Report bike",
                "option_func": report_bike_view
            },
            "5": {
                "option_name": "Write review",
                "option_func": write_review_view
            },
            "6": {
                "option_name": "Update details",
                "option_func": update_details_view
            },
            "7": {
                "option_name": "Log out",
                "option_func": log_out_view
            }
        }

    def show_login(self):
        print(
            "Hello Customer! I hope you are having a nice day today. Are you an Existing Customer or a new one?"
            "\n 1.Sign in \n 2.New account!")
        while True:

            option = input("Enter your option: ")

            if option == "1":
                return log_in_view(self.customer_controller)
            elif option == "2":
                return sign_up_view(self.customer_controller)
            else:
                print("Cannot specify your option. Please try again")

    def show_input_screen(self):
        while True:
            option = input("Enter your option: ")

            try:
                option_func = self.option_mapping[option]["option_func"]
                option_func(self.customer_controller)
                if option_func.__name__ == "log_out_view":
                    break
                self.redirect()
            except KeyError:
                print("Cannot specify your option. Please try again")
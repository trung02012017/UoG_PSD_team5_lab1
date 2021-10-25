import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from datetime import datetime

from views.view import View
from controllers.manager_controller import ManagerController
from configs.other_config import manager_password
from utils.util_funcs import validate_date


def log_in_view():
    password = input("Enter password: ")
    if password == manager_password:
        return True
    else:
        return False


def show_get_time_view():
    print("Please enter time period for the report ! (Time format should follow YYYY-mm-dd format)")
    while True:
        start_time = input("Enter report date: ")

        if not validate_date(start_time):
            print("Your inputs are in wrong format !!!!")
            print("Please try again")
            print("==========")
        else:
            return datetime.strptime(start_time, '%Y-%m-%d')


def usage_daily_line(manager_controller: ManagerController):
    # start_time, end_time = show_get_time_view()
    while True:
        try:
            month_select = int(input("Select Month: "))
            if month_select not in range(1, 13, 1):
                print("Month must be a number from 1-12 !!!")
                continue
            else:
                manager_controller.show_usage_daily_line(month_select)
                break
        except Exception as e:
            print(e)
            print("Month must be a number from 1-12 !!!")
            continue


def user_daily_pie(manager_controller: ManagerController):
    while True:
        try:
            month_select = int(input("Select Month: "))
            if month_select not in range(1, 13, 1):
                print("Month must be a number from 1-12 !!!")
                continue
            else:
                manager_controller.show_user_daily_pie(month_select)
                break
        except Exception as e:
            print(e)
            print("Month must be a number from 1-12 !!!")
            continue


def revenue_daily_line(manager_controller: ManagerController):
    while True:
        try:
            month_select = int(input("Select Month: "))
            if month_select not in range(1, 13, 1):
                print("Month must be a number from 1-12 !!!")
                continue
            else:
                manager_controller.show_revenue_daily_line(month_select)
                break
        except Exception as e:
            print(e)
            print("Month must be a number from 1-12 !!!")
            continue


def route_daily_heatmap(manager_controller: ManagerController):
    while True:
        try:
            month_select = int(input("Select Month: "))
            if month_select not in range(1, 13, 1):
                print("Month must be a number from 1-12 !!!")
                continue
            else:
                manager_controller.show_route_daily_heatmap(month_select)
                break
        except Exception as e:
            print(e)
            print("Month must be a number from 1-12 !!!")
            continue


def rating_daily_bar(manager_controller: ManagerController):
    while True:
        try:
            month_select = int(input("Select Month: "))
            if month_select not in range(1, 13, 1):
                print("Month must be a number from 1-12 !!!")
                continue
            else:
                manager_controller.show_rating_daily_bar(month_select)
                break
        except Exception as e:
            print(e)
            print("Month must be a number from 1-12 !!!")
            continue


def comment_daily_wordcloud(manager_controller: ManagerController):
    while True:
        try:
            month_select = int(input("Select Month: "))
            if month_select not in range(1, 13, 1):
                print("Month must be a number from 1-12 !!!")
                continue
            else:
                manager_controller.show_comment_daily_wordcloud(month_select)
                break
        except Exception as e:
            print(e)
            print("Month must be a number from 1-12 !!!")
            continue


def log_out_view(manager_controller: ManagerController):
    pass


class ManagerView(View):
    def __init__(self):
        super().__init__()
        self.manager_controller = ManagerController()
        self.option_mapping = {
            "1": {
                "option_name": "Rents report",
                "option_func": usage_daily_line
            },
            "2": {
                "option_name": "User rents report",
                "option_func": user_daily_pie
            },
            "3": {
                "option_name": "Daily revenue",
                "option_func": revenue_daily_line
            },
            "4": {
                "option_name": "Daily routes report",
                "option_func": route_daily_heatmap
            },
            "5": {
                "option_name": "Daily rating report",
                "option_func": rating_daily_bar
            },
            "6": {
                "option_name": "Daily comments report",
                "option_func": comment_daily_wordcloud
            },
            "7": {
                "option_name": "Log out",
                "option_func": log_out_view
            }
        }

    def show_login(self):
        print("Hello Manager! ")
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
                option_func(self.manager_controller)
                if option_func.__name__ == "log_out_view":
                    break
                self.redirect()
            except KeyError:
                print("Cannot specify your option. Please try again")
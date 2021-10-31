from utils.util_funcs import connect_database
from models.manager import ManagerModel

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from datetime import datetime


class ManagerController:
    def __init__(self):
        self.conn = connect_database()
        self.manager_model = ManagerModel(self.conn)

    def show_usage_daily_line(self, month_select):

        df = self.manager_model.get_customer_activity()

        df['Date'] = df['endTime'].dt.date
        df['Time'] = df['endTime'].dt.time
        df['Month'] = df['endTime'].dt.month
        df['Year'] = df['endTime'].dt.year
        df['Day'] = df['endTime'].dt.day

        day31 = [1, 3, 5, 7, 8, 10, 12]
        day30 = [4, 6, 9, 11]
        day28 = [2]
        if month_select in day31:
            day = np.arange(32)
        elif month_select in day30:
            day = np.arange(31)
        else:
            day = np.arange(28)

        month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                      6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
        day_name = pd.DataFrame(day[1:], columns=['Day'])

        df_month = df.loc[df['Month'] == month_select]
        day_group = df_month.groupby(['Day']).size().reset_index(name='Freq').sort_values('Day', ascending=True)
        axis = pd.merge(day_name, day_group, on="Day", how="outer").fillna(0)
        x_axis = day_name
        y_axis = axis['Freq']

        sns.set_style("whitegrid")
        plt.title('Daily Rental Usage: ' + month_name[month_select], fontsize=10, loc='center',
                  fontdict=dict(weight='bold'))
        plt.xlabel('Day')
        plt.ylabel('Usage')
        plt.plot(x_axis, y_axis, color='c')
        plt.show()

    def show_user_daily_pie(self, month_select):
        df = self.manager_model.get_activity_by_user()

        df['Date'] = df['endTime'].dt.date
        df['Time'] = df['endTime'].dt.time
        df['Month'] = df['endTime'].dt.month
        df['Year'] = df['endTime'].dt.year
        df['Day'] = df['endTime'].dt.day
        month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                      6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        df_month = df.loc[df['Month'] == month_select]
        axis = df_month.groupby(['customerID']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)

        usernames = []
        for i, row in axis.iterrows():
            usernames.append(self.manager_model.get_username_by_id(row['customerID']))
        axis['username'] = usernames
        x_axis = axis['username']
        y_axis = axis['Freq']
        # exp_val = list(np.zeros(len(x_axis)))
        # exp_val[:3] = [0.2, 0.15, 0.13]

        plt.title("Proportion of Monthly Rental by User: " + month_name[month_select])
        plt.pie(y_axis, labels=x_axis, explode=None, shadow=True, autopct='%1.1f%%', startangle=300)
        plt.axis('equal')
        plt.show()

    def show_revenue_daily_line(self, month_select):

        df = self.manager_model.get_revenue_customer_activity()

        df['Date'] = df['endTime'].dt.date
        df['Time'] = df['endTime'].dt.time
        df['Month'] = df['endTime'].dt.month
        df['Year'] = df['endTime'].dt.year
        df['Day'] = df['endTime'].dt.day

        day31 = [1, 3, 5, 7, 8, 10, 12]
        day30 = [4, 6, 9, 11]
        day28 = [2]
        if month_select in day31:
            day = np.arange(32)
        elif month_select in day30:
            day = np.arange(31)
        else:
            day = np.arange(28)

        day_name = pd.DataFrame(day[1:], columns=['Day'])
        month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                      6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        df['month'] = pd.DatetimeIndex(df['endTime']).month
        df_paid = df.loc[(df['paid'] == 1) & (df['month'] == float(month_select))]
        day_group_paid = df_paid.groupby(['Day'])['charged'].sum().reset_index()
        axis_paid = pd.merge(day_name, day_group_paid, on="Day", how="outer").fillna(0)

        df_unpaid = df.loc[df['paid'] == 0 & (df['month'] == float(month_select))]
        day_group_unpaid = df_unpaid.groupby(['Day'])['charged'].sum().reset_index()
        axis_unpaid = pd.merge(day_name, day_group_unpaid, on="Day", how="outer").fillna(0)

        x_axis = day_name
        y_axis_paid = axis_paid['charged']
        y_axis_unpaid = axis_unpaid['charged']
        y_total = y_axis_paid + y_axis_unpaid

        sns.set_style("whitegrid")
        plt.title('Daily Rental Revenue: ' + month_name[month_select], fontsize=10, loc='center',
                  fontdict=dict(weight='bold'))
        plt.xlabel('Day')
        plt.ylabel('GBP')
        plt.plot(x_axis, y_axis_paid, linestyle='--', color='c')
        plt.plot(x_axis, y_axis_unpaid, linestyle='--', color='r')
        plt.plot(x_axis, y_total, marker='o', color='b')
        plt.legend(["Paid", "Unpaid", "Total"])
        plt.show()

    def show_route_daily_heatmap(self, month_select):
        df = self.manager_model.get_route_daily_heatmap()

        df['Date'] = df['endTime'].dt.date
        df['Time'] = df['endTime'].dt.time
        df['Month'] = df['endTime'].dt.month
        df['Year'] = df['endTime'].dt.year
        df['Day'] = df['endTime'].dt.day
        month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                      6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        df_month = df.loc[df['Month'] == month_select]
        df_location = df_month.groupby(['startLocation', 'endLocation']).size().reset_index(name='Freq')
        axis = df_location.pivot(index='endLocation', columns='startLocation', values='Freq').fillna(0)

        sns.heatmap(axis, annot=True, fmt='g', cmap='Blues')
        plt.title('Monthly Route Heat Map: ' + month_name[month_select], fontsize=10, loc='center',
                  fontdict=dict(weight='bold'))
        plt.show()

    def show_rating_daily_bar(self, month_select):

        df = self.manager_model.get_rating_daily()

        df['Date'] = df['reviewTime'].dt.date
        df['Time'] = df['reviewTime'].dt.time
        df['Month'] = df['reviewTime'].dt.month
        df['Year'] = df['reviewTime'].dt.year
        df['Day'] = df['reviewTime'].dt.day
        df_month = df.loc[df['Month'] == month_select]
        month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                      6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        star_num = pd.DataFrame(np.arange(1, 6), columns=['starRating'])

        month_group = df_month.groupby(['starRating']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
        axis = pd.merge(star_num, month_group, on="starRating", how="outer").fillna(0)
        x_axis = star_num['starRating']
        y_axis = axis['Freq']

        def addlabels(x_axis, y_axis):
            for i in range(len(x_axis)):
                plt.text(i + 1, y_axis[i], y_axis[i], ha='center')

        sns.set_style("darkgrid")
        plt.title('Monthly Rental Rating: ' + month_name[month_select], fontsize=10, loc='center',
                  fontdict=dict(weight='bold'))
        plt.xlabel('starRating')
        plt.ylabel('Frequency')
        plt.bar(x_axis, y_axis, color='c')
        addlabels(x_axis, y_axis)
        plt.show()

    def show_comment_daily_wordcloud(self, month_select):

        df = self.manager_model.get_comment_daily()

        df['Date'] = df['reviewTime'].dt.date
        df['Time'] = df['reviewTime'].dt.time
        df['Month'] = df['reviewTime'].dt.month
        df['Year'] = df['reviewTime'].dt.year
        df['Day'] = df['reviewTime'].dt.day

        month_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                      6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        df_month = df.loc[df['Month'] == month_select]
        comment_words = ''
        for val in df_month['comments']:
            val = str(val)
            tokens = val.split()
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()
            comment_words += " ".join(tokens) + " "

        wordcloud = WordCloud(background_color='#f2f2f2').generate(comment_words)

        plt.figure(figsize=(10, 8), facecolor=None)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.title('Monthly Sentiment Analysis: ' + month_name[month_select], fontsize=10, loc='center',
                  fontdict=dict(weight='bold'))
        plt.axis("off")
        plt.show()


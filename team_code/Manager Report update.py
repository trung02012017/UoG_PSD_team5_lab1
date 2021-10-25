import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
 
cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='project')

cursor = cnx.cursor()


def usage_monthly_bar():
    x = "select endTime from customeractivity"
    cursor.execute(x)
 
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
 
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=['endTime'])

    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day

    month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
              'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_num = pd.DataFrame(np.arange(1, 13), columns=['Month'])
    month_group = df.groupby(['Month']).size().reset_index(
    name='Freq').sort_values('Month', ascending=True)
    axis = pd.merge(month_num, month_group, on="Month", how="outer").fillna(0)
    x_axis = month_name
    y_axis = axis['Freq']

    def add_labels(x_axis, y_axis):
        for i in range(len(x_axis)):
            plt.text(i,y_axis[i],y_axis[i], ha='center')
    
    sns.set_style("darkgrid")
    plt.title('Monthly Rental Usage', fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.xlabel('Month')
    plt.ylabel('Frequency')
    plt.bar(x_axis,y_axis, color='c')
    add_labels(x_axis, y_axis)
    plt.show()

def usage_daily_line():
    x = ("select endTime from customeractivity")
    cursor.execute(x)
 
    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=['endTime'])

    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    month_select = int(input("Select Month: "))
    day31 = [1,3,5,7,8,10,12]
    day30 = [4,6,9,11]
    day28 = [2]
    if month_select in day31:
        day = np.arange(32)
    elif month_select in day30:
        day = np.arange(31)
    else:
        day = np.arange(28)
    
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    day_name = pd.DataFrame(day[1:], columns=['Day'])
    
    df_month = df.loc[df['Month'] == month_select]
    day_group = df_month.groupby(['Day']).size().reset_index(name='Freq').sort_values('Day', ascending=True)
    axis = pd.merge(day_name, day_group, on="Day", how="outer").fillna(0)
    x_axis = day_name
    y_axis = axis['Freq']
    
    sns.set_style("whitegrid")
    plt.title('Daily Rental Usage: ' + month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.xlabel('Day')
    plt.ylabel('Usage')
    plt.plot(x_axis, y_axis, color='c')
    plt.show()


def user_yearly_pie():
    x = ("select customerID, endTime from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['customerID','endTime'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    axis = df.groupby(['customerID']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
    x_axis = axis['customerID']
    y_axis = axis['Freq']
    exp_val = list(np.zeros(len(x_axis)))
    exp_val[:3] = [0.2,0.15,0.13]
    
    plt.title("Proportion of Yearly Rental by User")
    plt.pie(y_axis, labels=x_axis, explode=exp_val, shadow=True, autopct='%1.1f%%', startangle=300)
    plt.axis('equal')
    plt.show()


def user_monthly_pie():
    x = ("select customerID, endTime from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['customerID','endTime'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    month_select = int(input("Select Month: "))
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    df_month = df.loc[df['Month'] == month_select]
    axis = df_month.groupby(['customerID']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
    x_axis = axis['customerID']
    y_axis = axis['Freq']
    exp_val = list(np.zeros(len(x_axis)))
    exp_val[:3] = [0.2,0.15,0.13]
    
    plt.title("Proportion of Monthly Rental by User: " + month_name[month_select])
    plt.pie(y_axis, labels=x_axis, explode=exp_val, shadow=True, autopct='%1.1f%%', startangle=300)
    plt.axis('equal')
    plt.show()

def user_daily_pie():
    x = ("select customerID, endTime from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['customerID','endTime'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    month_select = int(input("Select Month: "))
    day_select = int(input("Select Day: "))
    
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    df_month = df.loc[df['Month'] == month_select]
    df_day = df_month.loc[df['Day'] == day_select]
    axis = df_day.groupby(['customerID']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
    x_axis = axis['customerID']
    y_axis = axis['Freq']
    exp_val = list(np.zeros(len(x_axis)))
    exp_val[:3] = [0.2,0.15,0.13]
    
    plt.title("Proportion of Daily Rental by User: " + str(day_select) + " " + month_name[month_select])
    plt.pie(y_axis, labels=x_axis, explode=exp_val, shadow=True, autopct='%1.1f%%', startangle=300)
    plt.axis('equal')


def revenue_monthly_bar():
    x = ("select charged, paid, endTime from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
 
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['charged','paid','endTime'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    month_name = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_num = pd.DataFrame(np.arange(1,13), columns=['Month'])
    
    df_paid = df.loc[df['paid'] == 1]
    month_group_paid = df_paid.groupby(['Month'])['charged'].sum().reset_index()
    axis_paid = pd.merge(month_num, month_group_paid, on="Month", how="outer").fillna(0)
    print(axis_paid)
    
    df_unpaid = df.loc[df['paid'] == 0]
    month_group_unpaid = df_unpaid.groupby(['Month'])['charged'].sum().reset_index()
    axis_unpaid = pd.merge(month_num, month_group_unpaid, on="Month", how="outer").fillna(0)
    
    x_axis = month_name
    y_axis_paid = axis_paid['charged']
    y_axis_unpaid = axis_unpaid['charged']
 
    plt.title('Monthly Rental Revenue', fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.xlabel('Month')
    plt.ylabel('GBP')
    plt.bar(x_axis, y_axis_paid, color='c')
    plt.bar(x_axis, y_axis_unpaid, bottom = y_axis_paid, color='r')
    plt.legend(["Paid", "Unpaid"])
    plt.show()

    
def revenue_daily_line():
    x = ("select charged, paid, endTime from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['charged','paid','endTime'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    month_select = int(input("Select Month: "))
    day31 = [1,3,5,7,8,10,12]
    day30 = [4,6,9,11]
    day28 = [2]
    if month_select in day31:
        day = np.arange(32)
    elif month_select in day30:
        day = np.arange(31)
    else:
        day = np.arange(28)
    
    day_name = pd.DataFrame(day[1:], columns=['Day'])
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    df_paid = df.loc[df['paid'] == 1]
    day_group_paid = df_paid.groupby(['Day'])['charged'].sum().reset_index()
    axis_paid = pd.merge(day_name, day_group_paid, on="Day", how="outer").fillna(0)
    
    df_unpaid = df.loc[df['paid'] == 0]
    day_group_unpaid = df_unpaid.groupby(['Day'])['charged'].sum().reset_index()
    axis_unpaid = pd.merge(day_name, day_group_unpaid, on="Day", how="outer").fillna(0)
    
    x_axis = day_name
    y_axis_paid = axis_paid['charged']
    y_axis_unpaid = axis_unpaid['charged']
    y_total = y_axis_paid + y_axis_unpaid
    
    sns.set_style("whitegrid")
    plt.title('Daily Rental Revenue: '+ month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.xlabel('Day')
    plt.ylabel('GBP')
    plt.plot(x_axis, y_axis_paid, linestyle='--', color='c')
    plt.plot(x_axis, y_axis_unpaid, linestyle='--', color='r')
    plt.plot(x_axis, y_total, marker='o', color='b')
    plt.legend(["Paid", "Unpaid","Total"])
    plt.show()


def route_yearly_heatmap():
    x = ("select endTime, startLocation, endLocation from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['endTime', 'Start Location', 'End Location'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    df_location = df.groupby(['Start Location','End Location']).size().reset_index(name='Freq')
    axis = df_location.pivot(index='End Location', columns='Start Location', values='Freq').fillna(0)
    
    sns.heatmap(axis, annot=True, fmt='g', cmap='Greens')
    plt.title('Yearly Route Heat Map', fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.show()


def route_monthly_heatmap():
    x = ("select endTime, startLocation, endLocation from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['endTime', 'startLocation', 'endLocation'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    month_select = int(input("Select Month: "))
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    df_month = df.loc[df['Month'] == month_select]
    df_location = df_month.groupby(['startLocation','endLocation']).size().reset_index(name='Freq')
    axis = df_location.pivot(index='endLocation', columns='startLocation', values='Freq').fillna(0)
    
    sns.heatmap(axis, annot=True, fmt='g', cmap='Blues')
    plt.title('Monthly Route Heat Map: ' + month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.show()


def route_daily_heatmap():
    x = ("select endTime, startLocation, endLocation from customeractivity")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    
    df = pd.DataFrame(rows, columns=['endTime', 'startLocation', 'endLocation'])
    
    df['Date'] = df['endTime'].dt.date
    df['Time'] = df['endTime'].dt.time
    df['Month'] = df['endTime'].dt.month
    df['Year'] = df['endTime'].dt.year
    df['Day'] = df['endTime'].dt.day
    
    month_select = int(input("Select Month: "))
    day_select = int(input("Select Day: "))
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    df_month = df.loc[df['Month'] == month_select]
    df_day = df_month.loc[df['Day'] == day_select]
    df_location = df_day.groupby(['startLocation','endLocation']).size().reset_index(name='Freq')
    axis = df_location.pivot(index='endLocation', columns='startLocation', values='Freq').fillna(0)
    
    sns.heatmap(axis, annot=True, fmt='g', cmap='Blues')
    plt.title('Daily Route Heat Map: ' + str(day_select) + " " + month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.show()


def rating_yearly_bar():
    x = ("select rating, reviewTime from reviews")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    rows
    
    df = pd.DataFrame(rows, columns=['rating','reviewTime'])
    
    df['Date'] = df['reviewTime'].dt.date
    df['Time'] = df['reviewTime'].dt.time
    df['Month'] = df['reviewTime'].dt.month
    df['Year'] = df['reviewTime'].dt.year
    df['Day'] = df['reviewTime'].dt.day
    
    axis = df.groupby(['rating']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
    x_axis = axis['rating']
    y_axis = axis['Freq']
    
    star_num = pd.DataFrame(np.arange(1,6), columns=['rating'])

    group = df.groupby(['rating']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
    axis = pd.merge(star_num, group, on="rating", how="outer").fillna(0)
    x_axis = star_num['rating']
    y_axis = axis['Freq']

    def addlabels(x_axis,y_axis):
        for i in range(len(x_axis)):
            plt.text(i+1,y_axis[i],y_axis[i], ha='center')
            
    sns.set_style("darkgrid")
    plt.title('Yearly Rental Rating', fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.bar(x_axis,y_axis, color='c')
    addlabels(x_axis, y_axis)
    
def rating_monthly_bar():
    x = ("select rating, reviewTime from reviews")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    rows
    
    df = pd.DataFrame(rows, columns=['rating','reviewTime'])
    
    df['Date'] = df['reviewTime'].dt.date
    df['Time'] = df['reviewTime'].dt.time
    df['Month'] = df['reviewTime'].dt.month
    df['Year'] = df['reviewTime'].dt.year
    df['Day'] = df['reviewTime'].dt.day
    
    month_select = int(input("Select Month: "))
    df_month = df.loc[df['Month'] == month_select]
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    star_num = pd.DataFrame(np.arange(1,6), columns=['rating'])

    month_group = df_month.groupby(['rating']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
    axis = pd.merge(star_num, month_group, on="rating", how="outer").fillna(0)
    x_axis = star_num['rating']
    y_axis = axis['Freq']

    def addlabels(x_axis,y_axis):
        for i in range(len(x_axis)):
            plt.text(i+1,y_axis[i],y_axis[i], ha='center')
            
    sns.set_style("darkgrid")
    plt.title('Monthly Rental Rating: ' + month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.bar(x_axis,y_axis, color='c')
    addlabels(x_axis, y_axis)

def rating_daily_bar():
    x = ("select rating, reviewTime from reviews")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    rows
    
    df = pd.DataFrame(rows, columns=['rating','reviewTime'])
    
    df['Date'] = df['reviewTime'].dt.date
    df['Time'] = df['reviewTime'].dt.time
    df['Month'] = df['reviewTime'].dt.month
    df['Year'] = df['reviewTime'].dt.year
    df['Day'] = df['reviewTime'].dt.day
    
    month_select = int(input("Select Month: "))
    day_select = int(input("Select Day: "))
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    df_day = df.loc[df['Day'] == day_select]
    
    star_num = pd.DataFrame(np.arange(1,6), columns=['rating'])

    day_group = df_day.groupby(['rating']).size().reset_index(name='Freq').sort_values('Freq', ascending=False)
    axis = pd.merge(star_num, day_group, on="rating", how="outer").fillna(0)
    x_axis = star_num['rating']
    y_axis = axis['Freq']

    def addlabels(x_axis,y_axis):
        for i in range(len(x_axis)):
            plt.text(i+1,y_axis[i],y_axis[i], ha='center')
    
    sns.set_style("darkgrid")
    plt.title('Daily Rental Rating: ' + str(day_select) + " " + month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.bar(x_axis,y_axis, color='c')
    addlabels(x_axis, y_axis)

def comment_yearly_wordcloud():
    x = ("select comments, reviewTime from reviews")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    rows
    
    df = pd.DataFrame(rows, columns=['comments','reviewTime'])
    
    df['Date'] = df['reviewTime'].dt.date
    df['Time'] = df['reviewTime'].dt.time
    df['Month'] = df['reviewTime'].dt.month
    df['Year'] = df['reviewTime'].dt.year
    df['Day'] = df['reviewTime'].dt.day
    
    comment_words = ''
    for val in df['comments']:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens)+" "
                               
    wordcloud = WordCloud(background_color='#f2f2f2').generate(comment_words)
    
    plt.figure(figsize=(10,8), facecolor = None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

def comment_monthly_wordcloud():
    x = ("select comments, reviewTime from reviews")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    rows
    
    df = pd.DataFrame(rows, columns=['comments','reviewTime'])
    
    df['Date'] = df['reviewTime'].dt.date
    df['Time'] = df['reviewTime'].dt.time
    df['Month'] = df['reviewTime'].dt.month
    df['Year'] = df['reviewTime'].dt.year
    df['Day'] = df['reviewTime'].dt.day
    
    month_select = int(input("Select Month: "))
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    df_month = df.loc[df['Month'] == month_select]
    comment_words = ''
    for val in df_month['comments']:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens)+" "
                               
    wordcloud = WordCloud(background_color='#f2f2f2').generate(comment_words)
    
    plt.figure(figsize=(10,8), facecolor = None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title('Monthly Sentiment Analysis: ' + month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))       
    plt.axis("off")

def comment_daily_wordcloud():
    x = ("select comments, reviewTime from reviews")
    cursor.execute(x)
     
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
     
    rows = cursor.fetchall()
    rows
    
    df = pd.DataFrame(rows, columns=['comments','reviewTime'])
    
    df['Date'] = df['reviewTime'].dt.date
    df['Time'] = df['reviewTime'].dt.time
    df['Month'] = df['reviewTime'].dt.month
    df['Year'] = df['reviewTime'].dt.year
    df['Day'] = df['reviewTime'].dt.day
    
    month_select = int(input("Select Month: "))
    day_select = int(input("Select Day: "))
    
    df_month = df.loc[df['Month'] == month_select]
    df_day = df.loc[df['Day'] == day_select]
    month_name = {1:'January',2:'February',3:'March',4:'April',5:'May',
              6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
    
    comment_words = ''
    for val in df_day['comments']:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens)+" "
                               
    wordcloud = WordCloud(background_color='#f2f2f2').generate(comment_words)
    
    plt.figure(figsize=(10,8), facecolor = None)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.title('Daily Sentiment Analysis: ' + str(day_select) + " " + month_name[month_select], fontsize = 10, loc='center', fontdict=dict(weight='bold'))       
    plt.axis("off")

# usage_monthly_bar()
# usage_daily_line()
# user_yearly_pie()
# user_monthly_pie()
# user_daily_pie()
# revenue_monthly_bar()
# revenue_daily_line()
# route_yearly_heatmap()
# route_monthly_heatmap()
# route_daily_heatmap()
# rating_yearly_bar()
# rating_monthly_bar()
# rating_daily_bar()
# comment_yearly_wordcloud()
# comment_monthly_wordcloud()
# comment_daily_wordcloud()
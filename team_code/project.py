# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 11:16:31 2021

@author: raman
"""

import mysql.connector # to connect db
import sys # for sys.exit() function used in account balance
from datetime import datetime # to get system datetime

#connecting to db
cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='project')

#setting up the cursor
cursor = cnx.cursor()

def account_balance():
    #fetch customerID from login
    customerID=1    #declared it as 1 just to check if the code is working
    #declaring outstanding_amount  = 0 as there should be no outstanding amount for customers who already paid for their trip
    outstanding_amount = 0 
    #fetching the account balance of the customer
    cursor.execute("""SELECT account_total FROM customer WHERE customerID = %s""" %(customerID))
    #storing the account balance in variable called balance
    balance = cursor.fetchone() #balance is a tuple with a single value
    #converting balance to int from tuple
    balance = balance[0]
    #printing balance to the user
    print(balance)
    #fetching the rental_status of the customer
    cursor.execute("""SELECT rental_status FROM customer WHERE customerID = %s""" %(customerID))
    #storing the rental_status in variable called rental_status
    rental_status = cursor.fetchone()#rental_status is a tuple with a single value
    #converting rental_status to int from tuple
    rental_status = rental_status[0]
    #printing rental_status to the user
    print(rental_status)
    #checking if the user is currently renting a bike
    if rental_status == 1:
        #fetching the outstanding charges for the user
        cursor.execute("""SELECT charged FROM customeractivity WHERE customerID = %s AND paid = 0""" %(customerID))
        #storing the charged amount in outstading_charges
        outstanding_charges = cursor.fetchone() #outstanding_charges is a tuple with a single value
        #converting to int and storing in outstanding amount
        outstanding_amount = outstanding_charges[0]
        #printing the value for my reference
        print(outstanding_charges)
    #checking if balance amount is less than outstanding_amount
    if balance < outstanding_amount:
        #letting the user know that their balance is low and asking them to topup their account
        choice = int(input("Your balance is too low! Please enter 1 to top-up your account: "))
        if choice == 1:
            #while loop asking the user to topup until all the outstanding charges are paid
            while balance < outstanding_amount:
                #storing the topup amount
                topup = int(input("Enter the amount to topup (Outstanding amount is more than your account balance): "))
                #updating the account balance
                balance = balance + topup
        else:
            #As the user didn't want to topup printed a message asking them to topup before renting another bike
            print("Kindly topup your account before renting a bike")
            #printing the user's account balance
            print("Your account balance is:", balance)
            #exiting the program as outstanding charges are not paid
            sys.exit()
    #calculating the new balance
    balance = balance - outstanding_amount
    #fetching the total amount paid by the user until now
    cursor.execute("""SELECT totalPaid FROM customer WHERE customerID = %s""" %(customerID))
    totalPaid = cursor.fetchone() #storing the tuple
    totalPaid = totalPaid[0] # convert to int
    totalPaid = totalPaid + outstanding_amount #calculating the new total amount that is paid
    #updating the rental_status to 0 as the customer paid the outstanding charges
    cursor.execute("""UPDATE customer SET rental_status = 0 WHERE customerID = %s""" %(customerID))
    #updating paid to 1 as the customer paid the outstanding charges
    cursor.execute("""UPDATE customeractivity SET paid = 1 WHERE customerID = %s AND paid = 0""" %(customerID))
    #updating the new account baance in the db
    cursor.execute("""UPDATE customer SET account_total = %s WHERE customerID = %s""" %(balance,customerID))
    #updating the total amount paid in the db
    cursor.execute("""UPDATE customer SET totalPaid = %s WHERE customerID = %s""" %(totalPaid,customerID))
    #commiting all the changes
    cnx.commit()
    #if there was no outstanding balance then display the account balance to the user
    if(outstanding_amount==0):
        print("Your balance is:", balance)
    #Display the new balance after charges are paid
    else:
        print("Transaction Successfull!")
        print("Outstanding charges are paid")
        print("Your new account balance is:", balance)
            
def review():
    #fetch customerID and bikeID from rent a bike
    customerID=3 # declared as 3 for checking the working of the code
    bikeID=4 # declared as 4 for checking the working of the code

    # datetime object containing current date and time
    now = datetime.now()

    # formatting the datetime object dd/mm/YY H:M:S
    reviewTime = now.strftime("%Y/%m/%d %H:%M:%S")
    print("date and time =", reviewTime)
    
    #collecting the star rating from the user
    star = int(input("How would you rate your trip out of 5 stars: "))
    #run the loop until the user enters rating between 1 and 5
    while star > 5 or star < 1:
        star=int(input("Please enter a number between 1 and 5 only: "))
    #taking a comment from the user regarding their trip
    comment = input("Please enter any comments you have about your trip: ")
    #push the data to the db
    #insert variable contains the query
    insert = ("""INSERT INTO reviews(customerID, bikeID, starRating, comments, reviewTime) VALUES (%s,%s,%s,%s,%s)""")
    #data variable contains the information that needs to be pushed to the db
    data = (customerID,bikeID,star,comment,reviewTime)
    #executing the query
    cursor.execute(insert, data)
    #committing all changes
    cnx.commit()
        
account_balance()  #calling account_balance function
review() #calling review function

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 09:08:54 2021

@author: poojakurup
"""

# Sign in

import re # regular expression for the email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def check(email):
 
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        print("Valid Email")
    else:
        print("Invalid Email")


#CREATE DATABASE IF NOT EXISTS CUSTOMER
a=int(input("Hello Customer! I hope you are having a nice day today. Are you an Existing Customer or a new one?\n 1.Sign in \n 2.New account!\n Enter:"))
if a==1:
    print("Please enter your username and password:")

    user=input("USERNAME:")
    password=input("PASSWORD:")
    INSERT INTO CUSTOMER(USERNAME, PASSWORD)VALUES (user,password)
   # if #username and password should match the previous database
    
else:
    print("Hi! Happy to help you join the BikeStop Team!")   
    print("Could you please Enter the details below.")
    Fname=input("Enter First Name:")
    Lname=input("Enter Last Name:")
    while True:
        try:
            #if __name__ == '__main__':
            email=input("Enter Email:")
            if __name__ == '__main__':
                check(email)
                break;
            else:
                print(" Invalid card")
        except ValueError:
            print("Provide correct Email address:")
 

    print("Just a few more details to go.")
    INSERT INTO CUSTOMER(FIRST,LAST,EMAIL,CARDNO)VALUES (Fname,Lname,email,cardn)
    #Generate Customer ID
    #INSERT INTO CUSTOMER(CUSTOMER ID)VALUES(CustID)
    print("Your customer ID is:", CustID)

    #limit to 12 digits, the card
    while True:
        try:
            Cardn=input("Enter Card no:")
            n=len(Cardn)
            if n==12:
                    print("Thank You for joining BikeStop.")
                    break;
            else:
                    print("Invalid Card")     
        except ValueError:
             print("Provide an integer value.")
a=input(" Would you like to Rent a bike.(Y/N")
a.lower()
if a==y:
    # take them to rent function
else:
    print("Have a nice day!")
            
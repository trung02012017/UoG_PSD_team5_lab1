# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 11:22:01 2021

@author: Suki
"""

import mysql.connector

cnx = mysql.connector.connect(user='root',password='',host='localhost',database='project')
cursor = cnx.cursor()

query = ("select * from customer")

cursor.execute(query)
num_fields = len(cursor.description)

field_names = [i[0] for i in cursor.description]

print(field_names)

for r in cursor.fetchall():
    print(r)

customerID =1


#Return Bike
#- 	Enters new bike location, end time, calculates and enters charge in table, display charge to customer, charges account or bank card if account is empty
#-	Writes paid against the journey
#-  Sets rental status to not renting
#-	If account is low, suggests that they top up
#-  Report bike
#-	Updates bike table with broken against bike number
#-	Enter a comment about what is wrong?







# customerID should be set by login  

def returnbike():
    # ask user to input location to set location id
    print("1) Location1 \n2) Location2\n")
    locationID = int(input("Please enter the number related to your current location: ")) 
    
    ActID = cursor.execute("""SELECT activityID FROM customeractivity WHERE customerID = %s""" %(customerID)) 
    
    # find starttime and bikenum from database 
    startTime = cursor.execute("""SELECT startTime FROM customeractivity WHERE ActID = %s""" %(ActID)) 
    bikeID = cursor.execute("""SELECT bikeID FROM customer WHERE customerID =%s""" %(customerID))
    # set endTime from system
    from datetime import datetime
    now = datetime.now() 
    endTime = now.strftime("%H:%M:%S")
    # set new bike location, bike status to not in use
    cursor.execute("""UPDATE bike SET locationID = %s, status = %s where bikeID = %s""" %(locationID,0,bikeID))
    # set endtime
    cursor.execute("""UPDATE customeractivity SET endTime = %s, where ActID = %s""" %(endTime,ActID))
    cursor.commit()
    #Calculate all the hours, mins and seconds elapsed
    end_hours = int(endTime[0:2])
    start_hours = int(startTime[0:2])
    end_mins = int(endTime[3:5])
    start_mins = int(startTime[3:5])
    
    ###useful for testing so we don't have to sit around waiting between renting and returning 
    #end_sec = int(endTime[6:8])
    #start_sec = int(startTime[6:8])
    
    #set the number of hours
    if end_mins - start_mins <0:
        hours = end_hours- start_hours
    else:
        hours = end_hours - start_hours +1
        
    #this is here for us to test with as we might not want to wait several mins to test
    #if hours == 0:
    #   hours =1
        
    # charge £3 per hour
    charged = 3*hours
    # put charge amount in database
    cursor.execute("""UPDATE customeractivity SET charged = %s, where ActID = %s""" %(charged,ActID))
    cursor.commit()
    # tell customer what they are charged
    print("You will be charged £",charged,"for this journey")
    # find current customer account total
    account_total = cursor.execute("""SELECT account_total FROM customer WHERE customerID =?""" %(customerID)) 
    
    # if they have enough money, charge account
    if charged <= account_total:
        account_total = account_total-charged
        cursor.execute("""UPDATE customer SET account_total = %s WHERE customerID = %s""" %(account_total,customerID))
        cursor.commit()
    
    # if they don't have enough, tell them to top up account
    else:
        print("You need to top up your account before you can hire another bike")
    #### need a break statement for this option    

    #### at this point they are still renting and journey is not yet paid, when do we deal with that
    
    
 #paid/rental status/ deduct charge account
    # if they have enough in their account, set journey to paid
    if account_total >= 0:
        cursor.execute("""UPDATE customeractivity SET paid = 1, WHERE ActID = %s""" %(ActID))
        cursor.commit()
     
    # if they have paid, update rental status to not renting    
    paid = cursor.execute("""SELECT paid FROM customeractvity WHERE ActID =?""" %(ActID)) 
    if paid == 1:
        cursor.execute("""UPDATE customer SET rental_status = 0, WHERE customerID = %s""" %(customerID))
        cursor.commit()
        
    # if their account balance is less than £5, tell them to top up
    account_total = cursor.execute("""SELECT account_total FROM customer WHERE customerID =?""" %(customerID)) 
    if account_total < 5:
        print('Account is running low. Please top up')
   
    print("If you have any issues with the bike you rented, please report immediately using the report option in the menu.")
    #### do we need to clear bike number from account? Would be better if bike number is written over when rented so the bike number is there once they've returned it if they need to report issues
    #### takes back to menu

def reportbike():
     #### do they have to return bike before they can report? If so we need to check whether the customer is renting currently
     #### or do we put the report bike as part of the return process?
     
   
     
     # finds bike ID
     bikeID = cursor.execute("""SELECT bikeID FROM customer where customerID =?""" %(customerID))
     # Updates bike code to broken
     cursor.execute("""UPDATE bike SET bikeStatus = 1 where bikeID = %s""" %(bikeID))
     cursor.commit()
     # customer enters commeny
     comment = input("Enter what was wrong with the bike: ")
     # comment inserted into database
     cursor.execute("""INSERT INTO bike (comment) VALUES ?""" %comment)
     cursor. commit()
     
     #### back to menu
     


###### ignore this!!
# while entry != quit option:
#    print("Menu options")
# for each menu option call function
#    else:
#        print('invalid entry, try again')
import pandas as pd


class CustomerModel:
    def __init__(self, connection):
        self.conn_db = connection

    def find_customer(self, username, password):
        query = f"select * from customer where email = '{username}' and password = '{password}'"
        return pd.read_sql(query, self.conn_db)

    def find_customer_by_username(self, username):
        query = f"select * from customer where email = '{username}'"
        return pd.read_sql(query, self.conn_db)

    def add_new_customer(self, username, password, card_number):

        latest_customer_query = "select * from customer order by customerID desc"
        latest_customer = pd.read_sql(latest_customer_query, self.conn_db)
        latest_id = latest_customer.iloc[0]['customerID']

        query = f"insert into customer (customerID, totalPaid, email, password, account_total, rental_status, " \
                f"card_details) values ({latest_id + 1}, 0, '{username}', '{password}', 0, 0, " \
                f"'{card_number}')"
        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

        return self.find_customer(username, password)

    def find_customer_by_id(self, customer_id):
        query = f"select * from customer where customerID = {customer_id}"
        return pd.read_sql(query, self.conn_db)

    def get_bikes_by_location(self, location_id):
        query = f"select * from bike where locationID = {location_id}"
        return pd.read_sql(query, self.conn_db)

    def add_new_customer_act(self, customer_id, bike_id, start_time, location_id):
        query = f"insert into customeractivity " \
                f"(customerID, bikeID, startTime, endTime, startLocation, endLocation, charged, paid) " \
                f"values " \
                f"({customer_id}, {bike_id}, '{start_time}', null,{location_id}, null, null, 0)"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def update_customer_rental_status(self, customer_id, rental_status):
        query = f"update customer set rental_status = {rental_status} where customerID = {customer_id}"
        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def get_latest_act(self, customer_id):
        query = f"select * from customeractivity " \
                f"where customerID = {customer_id} " \
                f"and endTime is null " \
                f"order by ActID desc " \
                f"limit 1"
        return pd.read_sql(query, self.conn_db)

    def get_latest_act_done(self, customer_id):
        query = f"select * from customeractivity " \
                f"where customerID = {customer_id} " \
                f"order by ActID desc " \
                f"limit 1"
        return pd.read_sql(query, self.conn_db)

    def get_all_locations(self):
        query = "select * from location order by locationID"
        return pd.read_sql(query, self.conn_db)

    def get_account_total(self, customer_id):
        query = f"select * from customer where customerID = {customer_id}"
        df = pd.read_sql(query, self.conn_db)
        return df.iloc[0]['account_total']

    def update_return_act(self, act_id, end_time, end_location, charged, paid):
        query = f"update customeractivity " \
                f"set endTime = '{end_time.strftime('%Y-%m-%d %H:%M:%S')}', " \
                f"endLocation = {end_location}, " \
                f"charged = {charged}, " \
                f"paid = {paid} " \
                f"where ActID = {act_id}"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def update_customer_account(self, customer_id, remaining_account, rental_status, total_paid):
        query = f"update customer " \
                f"set account_total = {remaining_account}, " \
                f"totalPaid = {total_paid}, " \
                f"rental_status = {rental_status} " \
                f"where customerID = {customer_id}"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def update_bike_location(self, bike_id, location_id):
        query = f"update bike " \
                f"set locationID = {location_id} " \
                f"where bikeID = {bike_id}"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def update_bike_status(self, bike_id, bike_cond):
        query = f"update bike " \
                f"set bikeStatus = '{bike_cond}' " \
                f"where bikeID = {bike_id}"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def update_details(self, customer_id, field_name, value):
        query = f"update customer " \
                f"set {field_name} = '{value}' " \
                f"where customerID = {customer_id}"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def update_account_total(self, customer_id, amount):
        query = f"update customer " \
                f"set account_total = {amount} " \
                f"where customerID = {customer_id}"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def add_customer_review(self, customer_id, bike_id, star, review, review_time):
        query = f"insert into reviews " \
                f"(customerID, bikeID, starRating, comments, reviewTime) " \
                f"values " \
                f"({customer_id}, {bike_id}, {star}, '{review}', '{review_time}')"

        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()
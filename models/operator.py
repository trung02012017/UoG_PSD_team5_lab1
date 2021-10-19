import pandas as pd


class OperatorModel:
    def __init__(self, connection):
        self.conn_db = connection

    def insert_operator_activity(self, bike_id, action_name, action_time):
        query = f"insert into operatoractivity (bikeID, actionName, action_time) " \
                f"values ({bike_id}, '{action_name}', '{action_time}')"
        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def get_all_bikes_info(self):
        query = "select * from bike"
        return pd.read_sql(query, self.conn_db)

    def get_bike_rental_status(self, bike_id):
        query = f"select * from customeractivity where bikeID = {bike_id} and endLocation = null"
        df = pd.read_sql(query, self.conn_db)
        if df.shape[0] == 0:
            return 'Available'
        else:
            return 'Rented'

    def get_broken_bikes(self):
        query = "select * from bike where bikeStatus = 'broken'"
        return pd.read_sql(query, self.conn_db)

    def update_repaired_bike(self, bike_id):
        query = f"update bike set bikeStatus = 'good' where bikeID = {bike_id}"
        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()

    def get_all_locations(self):
        query = "select * from location order by locationID"
        return pd.read_sql(query, self.conn_db)

    def update_bike_location(self, bike_id, location_id):
        query = f"update bike set locationID = {location_id} where bikeID = {bike_id}"
        cursor = self.conn_db.cursor()
        cursor.execute(query)
        self.conn_db.commit()
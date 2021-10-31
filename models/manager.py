import pandas as pd


class ManagerModel:
    def __init__(self, connection):
        self.conn_db = connection

    def get_customer_activity(self):
        query = f"select endTime from customeractivity"
        return pd.read_sql(query, self.conn_db)

    def get_activity_by_user(self):
        query = "select customerID, endTime from customeractivity"
        return pd.read_sql(query, self.conn_db)

    def get_route_daily_heatmap(self):
        query = "select endTime, startLocation, endLocation from customeractivity"
        return pd.read_sql(query, self.conn_db)

    def get_revenue_customer_activity(self):
        query = "select charged, paid, endTime from customeractivity where endTime is not null"
        return pd.read_sql(query, self.conn_db)

    def get_rating_daily(self):
        query = "select starRating, reviewTime from reviews"
        return pd.read_sql(query, self.conn_db)

    def get_comment_daily(self):
        query = "select comments, reviewTime from reviews"
        return pd.read_sql(query, self.conn_db)

    def get_username_by_id(self, customer_id):
        query = f"select email from customer where customerID = {customer_id}"
        df = pd.read_sql(query, self.conn_db)
        return df.iloc[0]['email']

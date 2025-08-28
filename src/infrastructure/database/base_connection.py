from sqlalchemy import create_engine

class DBServerConn:
    def __init__(self, sql_uri):
        self.uri = sql_uri
        self.engine = self.return_engine()

    def return_engine(self):
        return create_engine(self.uri)  
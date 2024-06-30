from db.config.database import Database

class BlackListToken(Database):

    def __init__(self):
        super().__init__()
        self.start()        

    def start(self):
        self.connect()
        self.create_table()

    def create_table(self):
        query = """
                CREATE TABLE IF NOT EXISTS blacklist_token (
                    id SERIAL PRIMARY KEY,
                    refresh_token VARCHAR(500) UNIQUE NOT NULL,
                    blacklisted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
        
        self.cur.execute(query)
        self.conn.commit()

    def blacklist_token(self, refresh_token):
        query = """
                INSERT INTO blacklist_token (refresh_token)
                    VALUES (%s)
                    RETURNING *;
                """
        param = refresh_token
        
        self.cur.execute(query, (param,))
        self.conn.commit()
        new_blacklist = self.cur.fetchone()

        return new_blacklist
    
    def refresh_token_exists(self, attribute, value):
        query = f"SELECT EXISTS (SELECT 1 FROM blacklist_token WHERE {attribute} = '{value}');"
        self.cur.execute(query)
        refresh_token_exists = self.cur.fetchone()
        return refresh_token_exists[0]

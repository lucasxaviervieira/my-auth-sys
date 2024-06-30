from db.config.database import Database

class BlackListToken(Database):

    def __init__(self):
        super().__init__()
        self.start()        

    def start(self):
        self.connect()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS blacklist_token (
                id SERIAL PRIMARY KEY,
                refresh_token VARCHAR(500) UNIQUE NOT NULL,
                blacklisted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.conn.commit()

    def blacklist_token(self, refresh_token):
        self.cur.execute(
            """
            INSERT INTO blacklist_token (refresh_token)
                VALUES (%s)
                RETURNING *;
            """,
            (refresh_token,),
        )
        self.conn.commit()
        new_blacklist = self.cur.fetchone()

        return new_blacklist
    
    def delete_blacklist_token(self):
        self.cur.execute(f"DROP TABLE blacklist_token;")
        self.conn.commit()       

    def delete_user(self, id):
        self.cur.execute(f"DELETE FROM blacklist_token WHERE id = {id};")
        self.conn.commit()       

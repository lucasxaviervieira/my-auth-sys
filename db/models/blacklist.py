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
                access_token VARCHAR(500) UNIQUE NOT NULL,
                refresh_token VARCHAR(500) UNIQUE NOT NULL,
                blacklisted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.conn.commit()

    def create_blacklist(self, auth):
        access_token, refresh_token = auth.values()

        self.cur.execute(
            """
            INSERT INTO blacklist_token (access_token, refresh_token)
                VALUES (%s, %s)
                RETURNING *;
            """,
            (access_token, refresh_token),
        )
        self.conn.commit()
        new_blacklist = self.cur.fetchone()

        return new_blacklist

    def delete_user(self, id):
        self.cur.execute(f"DELETE FROM blacklist_token WHERE id = {id};")
        self.conn.commit()
        

from db.config.database import Database

class User(Database):

    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        self.connect()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE if not exists users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_verified BOOLEAN DEFAULT FALSE,
                profile_picture VARCHAR(255)
            );
            """
        )
        self.conn.commit()

    def get_user(self, attribute, value):
        self.cur.execute(f"SELECT * FROM users WHERE {attribute} = '{value}';")
        user = self.cur.fetchone()
        user = self.api_response(user)
        return user        

    def get_users(self):
        self.cur.execute("SELECT * FROM users;")
        users = self.cur.fetchall()
        users_list = []
        for user in users:
            dict_user = self.api_response(user)
            users_list.append(dict_user)
        return users_list        

    def create_user(self, new_user_obj):
        username, password, email, full_name, profile_picture = new_user_obj.values()
        self.cur.execute(
            """
            INSERT INTO users (username, password, email, full_name, role, is_verified, profile_picture)
                VALUES (%s, %s, %s, %s, default, default, %s)
                RETURNING *;
            """,
            (username, password, email, full_name, profile_picture),
        )
        self.conn.commit()
        new_user = self.cur.fetchone()
        new_user = self.api_response(new_user)
        return new_user

    def delete_user(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id = {id};")
        self.conn.commit()

    def user_exists(self, attribute, value):
        self.cur.execute(
            f"SELECT EXISTS (SELECT 1 FROM users WHERE {attribute} = '{value}');"
        )
        user_exists = self.cur.fetchone()
        return user_exists[0]

    def api_response(self, user):
        dict_user = {
            "id": user[0],
            "username": user[1],
            "password": user[2],
            "email": user[3],
            "full_name": user[4],
            "role": user[5],
            "registration_date": user[6],
            "last_login": user[7],
            "is_verified": user[8],
            "profile_picture": user[9],
        }
        return dict_user
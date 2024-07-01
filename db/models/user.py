from db.config.database import Database

class User(Database):

    def __init__(self):
        super().__init__()
        self.start()

    def start(self):
        self.connect()
        self.create_table()

    def create_table(self):
        query = """
                CREATE TABLE if not exists users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    salt VARCHAR(255) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    role VARCHAR(20) DEFAULT 'user',
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_verified BOOLEAN DEFAULT FALSE,
                    profile_picture VARCHAR(255)
                );
                """
        
        self.cur.execute(query)
        self.conn.commit()

    def get_user(self, attribute, value):
        query = f"SELECT * FROM users WHERE {attribute} = '{value}';"      
        self.cur.execute(query)
        user = self.cur.fetchone()
        user = self.api_response(user)
        return user        

    def get_users(self):
        query = "SELECT * FROM users;"
        self.cur.execute(query)
        users = self.cur.fetchall()
        users_list = []
        for user in users:
            dict_user = self.api_response(user)
            users_list.append(dict_user)
        return users_list        

    def create_user(self, new_user_obj):
        username, password, salt, email, full_name, profile_picture = new_user_obj.values()
        
        query = """
                INSERT INTO users (username, password, salt, email, full_name, role, is_verified, profile_picture)
                    VALUES (%s, %s, %s, %s, %s, default, default, %s)
                    RETURNING *;
                """
        param = (username, password, salt, email, full_name, profile_picture)
        
        self.cur.execute(query, param)
        self.conn.commit()
        new_user = self.cur.fetchone()
        new_user = self.api_response(new_user)
        return new_user

    def delete_user(self, id):
        query = f"DELETE FROM users WHERE id = {id};"
        self.cur.execute(query)
        self.conn.commit()

    def user_exists(self, attribute, value):
        query = f"SELECT EXISTS (SELECT 1 FROM users WHERE {attribute} = '{value}');"
        self.cur.execute(query)
        user_exists = self.cur.fetchone()
        return user_exists[0]

    def api_response(self, user):
        dict_user = {
            "id": user[0],
            "username": user[1],
            "password": user[2],
            "salt": user[3],
            "email": user[4],
            "full_name": user[5],
            "role": user[6],
            "registration_date": user[7],
            "last_login": user[8],
            "is_verified": user[9],
            "profile_picture": user[10],
        }
        return dict_user
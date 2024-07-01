import bcrypt

class HashPass:
    def hash_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8'), salt.decode('utf-8')

    def verify_password(input_password, stored_hashed_password, stored_salt):
        hashed_input_password = bcrypt.hashpw(input_password.encode('utf-8'), stored_salt.encode('utf-8'))
        return hashed_input_password == stored_hashed_password.encode('utf-8')
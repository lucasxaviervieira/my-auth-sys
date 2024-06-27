
from flask import Blueprint, jsonify, request
from db.models.user import User

bp = Blueprint(
    "url",
    __name__,
)   

class Situation:
    USER_EXISTS = 'USER_EXISTS'
    USER_NOT_EXISTS = 'USER_NOT_EXISTS'
    PASS_WRONG = 'PASS_WRONG'
    MAX_LENGTH = 'MAX_LENGTH'

@bp.route("/createuser", methods=["POST"])
def create_user():
    try:
        # conn
        user_table = User()
        user_table.start()

        inp_user = request.json["username"]
        inp_pass = request.json["password"]
        inp_email = request.json["email"]
        inp_full_name = request.json["full_name"]
        inp_prof_pict = request.json["profile_picture"]

        new_user_obj = {
            "username": inp_user, 
            "password": inp_pass, 
            "email": inp_email, 
            "full_name": inp_full_name, 
            "profile_picture": inp_prof_pict, 
        }
        
        
        is_user = user_table.user_exists("username",inp_user)
        is_email = user_table.user_exists("email",inp_email)

        situation = Situation.USER_EXISTS if is_user or is_email else Situation.USER_NOT_EXISTS

        match situation:
            case Situation.USER_EXISTS:
                user_table.disconnect()
                message_error = f"Error: Username {inp_user} or Email {inp_email} exists"
                return jsonify(message_error), 400
            case Situation.USER_NOT_EXISTS:
                new_user = user_table.create_user(new_user_obj)
                user_table.disconnect()
                message = "Success: Account created"
                return jsonify(message,new_user), 200
            
    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400

@bp.route("/token/", methods=["POST"])
def verify_user():
    try:
        # conn
        user_table = User()
        user_table.start()

        inp_user = request.json["username"]
        inp_pass = request.json["password"]

        is_user = user_table.user_exists("username",inp_user)

        if is_user:
            user = user_table.get_user("username",inp_user)
            curr_pass = user['password']
            if curr_pass == inp_pass:
                situation = Situation.USER_EXISTS
            else: 
                situation = Situation.PASS_WRONG                
        else:
            situation = Situation.USER_NOT_EXISTS
        
        match situation:
            case Situation.USER_EXISTS:
                user_table.disconnect()
                message = 'User correct'
                return jsonify(message,user)
            case Situation.PASS_WRONG:
                user_table.disconnect()
                message_error = "Error: Invalid password"
                return jsonify(message_error), 400
            case Situation.USER_NOT_EXISTS:
                user_table.disconnect()
                message_error = "Error: Invalid username"
                return jsonify(message_error), 400
            
    except:
        message_error = {"message": "Some error has occured"}
        return jsonify(message_error), 400


from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import bcrypt

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# Add a user in
    @classmethod
    def register_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, user_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(user_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL('books_db').query_db(query, data)

    @classmethod
    def get_one_user(cls, data):
        query = """
        SELECT * FROM users 
        WHERE id = %(id)s;
        """
        results = connectToMySQL('books_db').query_db(query, data)
        found_user_id = cls(results[0])
        return found_user_id

    @classmethod
    def get_one_user_by_email(cls, data):
        query = """
        SELECT * FROM users 
        WHERE email = %(email)s;
        """
        results = connectToMySQL('books_db').query_db(query, data)
        if len(results) == 0:
            return None
        else:
            found_user_id = cls(results[0])
            return found_user_id

    @staticmethod
    def validate_registration(data):
        print(data)
        is_valid = True

        if len(data['first_name']) < 2:
            is_valid = False
            flash("First name must be 2 or more characters!")

        if len(data['last_name']) < 2:
            is_valid = False
            flash("Last name must be 2 or more characters!")
        
        if len(data['user_name']) < 2:
            is_valid = False
            flash("User name must be 2 or more characters!")

        #Validation for email
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Check email formatting!")

        found_user_or_none = User.get_one_user_by_email({'email': data['email']})
        if found_user_or_none != None:
            is_valid = False
            flash("Email is taken!")

        #Check tha password length and if they match
        if len(data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters")

        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Passwords do not match!")
        return is_valid

    @staticmethod
    def validate_login(form_data):
        print(form_data)
        is_valid = True    
        user = User.get_one_user_by_email({'email': form_data['email']})
        session['user_id'] = user.id
        print(user.id)
        if user == None:
            is_valid = False
            flash("Invalid email or password!")
        elif not bcrypt.check_password_hash(user.password, form_data['password']):
            is_valid = False
            flash("Invalid email or password!")
        return is_valid
            


    
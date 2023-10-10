from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__(self,db_data):
        self.id = db_data['id']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.magazines = []
    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('pythonbelt').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def update_by_id(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s"
        return connectToMySQL('pythonbelt').query_db(query,data)
    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('pythonbelt').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def save_user(cls,data):
        query ="INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL('pythonbelt').query_db(query,data)
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name'])< 3 :
            flash('First Name is too short, needs to be at least 3 characters')
            is_valid = False
        if len(user['last_name'])< 3:
            flash('First Name is too short, needs to be at least 3 characters')
            is_valid = False
        if not str.isalpha(user['first_name']):
            is_valid = False
        if not str.isalpha(user['last_name']):
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) < 8:
            flash('Invalid password, needs to be at least 8 characters')
            is_valid = False
        return is_valid
    
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
class Magazine:
    def __init__(self,db_data) -> None:
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None
        self.subscribers = []
    @classmethod
    def show_magazines_w_creator(cls):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id"
        results = connectToMySQL('pythonbelt').query_db(query)
        new_results = []
        if results:
            for row in results:
                magazine = cls(row)
                data = {
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at'],
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password']
                }
                creator = user.User(data)
                magazine.creator = creator
                new_results.append(magazine)
        return new_results
    @classmethod
    def add_one_magazine(cls,data):
        query = "INSERT INTO magazines (title,description,user_id) VALUES (%(title)s,%(description)s,%(user_id)s)"
        return connectToMySQL('pythonbelt').query_db(query,data)
    
    @classmethod
    def get_one_mag_by_id(cls,data):
        query = "SELECT * FROM magazines WHERE id = %(id)s"
        result = connectToMySQL('pythonbelt').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_mags_by_user_id(cls,data):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE magazines.user_id = %(user_id)s"
        results = connectToMySQL('pythonbelt').query_db(query,data)
        new_results = []
        if results:
            for row in results:
                magazine = cls(row)
                data = {
                    'created_at':row['users.created_at'],
                    'updated_at':row['users.updated_at'],
                    'id':row['users.id'],
                    'first_name':row['first_name'],
                    'last_name':row['last_name'],
                    'email':row['email'],
                    'password':row['password']
                }
                creator = user.User(data)
                magazine.creator = creator
                new_results.append(magazine)
        return new_results
    
    @classmethod
    def destroy_mag_by_id(cls,data):
        query = "DELETE FROM magazines WHERE id = %(id)s"
        return connectToMySQL('pythonbelt').query_db(query,data)
    
    @staticmethod
    def validate_mag(magazine):
        is_valid = True
        if len(magazine['title']) < 2:
            flash('invalid Title, must be at least 2 characters')
            is_valid = False
        if len(magazine['description']) < 10:
            flash('invalid Description, must be at least 10 characters')
            is_valid = False
        return is_valid

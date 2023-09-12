from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash
from flask_app import bcrypt

class Book:   
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.genre = data['genre']
        self.review = data['review']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_review(cls, data):
        query = """
        INSERT INTO books 
        (title, author, genre, review, user_id)
        VALUES
        (%(title)s, %(author)s, %(genre)s, %(review)s, %(user_id)s)
        """
        return connectToMySQL('books_db').query_db(query, data)
    
    @classmethod
    def get_all_reviews(cls):
        query = """
        SELECT * FROM books
        JOIN users
        ON books.user_id = users.id;
        """
        results = connectToMySQL('books_db').query_db(query)
        books_object_list = [] 
        for each_book_review in results:
            print(each_book_review)
            new_sighting_object = cls(each_book_review)
            #Create the User object
            new_user_dictionary = {
                'id' : each_book_review['users.id'],
                'first_name' : each_book_review['first_name'],
                'last_name' : each_book_review['last_name'],
                'user_name' : each_book_review['user_name'],
                'email' : each_book_review['email'],
                'password' : "",
                'created_at' : each_book_review['users.created_at'],
                'updated_at' : each_book_review['users.updated_at']
            }
            new_user_object = User(new_user_dictionary)
            new_sighting_object.user = new_user_object
            books_object_list.append(new_sighting_object)
        return books_object_list
    
    @classmethod
    def get_one_review_with_user(cls, data):
        query = """
        SELECT * FROM books
        JOIN users
        ON books.user_id = users.id
        WHERE books.id = %(id)s;
        """
        results = connectToMySQL('books_db').query_db(query, data)
        get_one_review = results[0]
        review = cls(get_one_review)
        new_user_dictionary = {
                'id' : get_one_review['users.id'],
                'first_name' : get_one_review['first_name'],
                'last_name' : get_one_review['last_name'],
                'user_name' : get_one_review['user_name'],
                'email' : get_one_review['email'],
                'password' : "",
                'created_at' : get_one_review['users.created_at'],
                'updated_at' : get_one_review['users.updated_at']
            }
        user_object = User(new_user_dictionary)
        review.user = user_object
        return get_one_review
    
    @classmethod
    def create_review(cls, data):
        query = """
        INSERT INTO books 
        (title, author, genre, review, user_id)
        VALUES
        (%(title)s, %(author)s, %(genre)s, %(review)s, %(user_id)s)
        """
        return connectToMySQL('books_db').query_db(query, data)
    
    @classmethod
    def edit_review(cls, data):
        query = """
        UPDATE books
        SET title = %(title)s,
        author = %(author)s,
        genre = %(genre)s,
        review = %(review)s
        WHERE id = %(id)s;
        """
        return connectToMySQL('books_db').query_db(query, data)
    
    @classmethod
    def delete_review(cls, data):
        query = """
        DELETE FROM books
        WHERE id = %(id)s;
        """
        return connectToMySQL('books_db').query_db(query, data)
    
    @staticmethod
    def validate_review(form_data):
        print(form_data)
        is_valid = True
        if len(form_data['title']) < 5:
            is_valid = False
            flash('Title must be at least 5 characters long')
        if len(form_data['author']) < 3:
            is_valid = False
            flash('Author name must be at least 3 characters long')
        if form_data['genre'] == "":
            is_valid = False
            flash('Please select a genre')
        if len(form_data['review']) < 10:
            is_valid = False
            flash('Review must be at least 10 characters long')
        return is_valid       
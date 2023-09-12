from flask_app import app, bcrypt
from flask_app.models.user import User
from flask_app.models.book import Book
from flask import render_template, redirect, request, session

@app.route('/')
def members():
    return render_template('members.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        print(request.form)
        return redirect('/sign_up')
    new_user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "user_name": request.form['user_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.register_user(new_user_data)
    return redirect ('/home')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/members_login', methods=['POST'])
def user_login():
    if not User.validate_login(request.form):
        print('A')
        print(request.form)
        return redirect('/login')
    return redirect ('/home')

@app.route('/logout')
def logout():
        session.clear()
        return redirect('/')
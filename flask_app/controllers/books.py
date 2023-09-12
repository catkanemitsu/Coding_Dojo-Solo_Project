from flask_app import app
from flask_app.models.user import User
from flask_app.models.book import Book
from flask import render_template, redirect, request, session

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
        }
    return render_template('home.html', logged_user = User.get_one_user(data), all_reviews = Book.get_all_reviews())

@app.route('/add_review')
def add_review():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    return render_template('add.html', logged_user = User.get_one_user(data))

@app.route('/create/review', methods=['POST'])
def create_new_review():
    if "user_id" not in session:
        return redirect('/')
    if not Book.validate_review(request.form):
        return redirect('/add_review')
    print(request.form)
    Book.create_review(request.form)
    return redirect('/home')

@app.route('/edit_review/<int:id>')
def edit_review(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id' : id,
    }
    return render_template('edit.html', one_review = Book.get_one_review_with_user(data), logged_user = User.get_one_user(data))

@app.route('/edit/<int:id>', methods=['POST'])
def update_review(id):
    if "user_id" not in session:
        return redirect('/')
    if not Book.validate_review(request.form):
        return redirect(f"/edit/{id}")
    Book.edit_review(request.form)
    print(request.form)
    return redirect('/home')

@app.route('/review/<int:id>')
def review(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id' : id,
    }
    return render_template('view.html', one_review = Book.get_one_review_with_user(data))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_review(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : id,
    }
    Book.delete_review(data)
    return redirect('/home')
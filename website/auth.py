from flask import Blueprint, render_template, flash, redirect, request, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!', category='success')
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email does not exits.', category='error')
            
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return '<h1>Logout<h1>'

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords dont Match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email,first_name=first_name,password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='sucess')
            
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

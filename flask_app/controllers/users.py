from flask_app.models.magazine import Magazine
from flask_app import app
from flask import render_template, redirect, request, session,flash,url_for
from flask_app.models.user import User # import your model files
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')# this route will render the template for the login page
def index():
    return render_template('login.html')

@app.route('/register/process',methods=['POST'])#this route will process the post request for the register form
def register_post():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {"email":request.form['email']}
    user_in_db = User.get_one_by_email(data)
    if user_in_db:
        flash('Email already exists!')
        return redirect('/') 
    if request.form['confirm_pw'] != request.form['password']:
        flash('passwords do not match')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    
    user_in_db = User.save_user(data)
    session['user_in_db'] = user_in_db
    
    return redirect('/')

@app.route('/login/process',methods= ['POST'])#this route will process the post request for the login form
def login_post():
    data = {"email":request.form['login_email']}
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['login_pw']):
        flash('incorrect email/password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    
    return redirect('/dashboard')

@app.route('/user/account/<int:id>')
def show_user_profile(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id':id
    }
    mags = Magazine.get_mags_by_user_id(data={'user_id':session['user_id']})
    user = User.get_one_by_id(data)
    return render_template('user_profile.html',user = user,mags=mags) #this will have the update form and the sidebar that shows all the magazines

@app.route('/user/<int:id>/edit', methods = ['POST'])
def update_user(id):
    data ={
        'id':id,
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email']
    }
    User.update_by_id(data)
    return redirect(url_for('show_user_profile',id=session['user_id']))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
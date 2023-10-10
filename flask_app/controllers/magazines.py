from flask_app import app
from flask import render_template, redirect, request, session,flash,url_for
from flask_app.models.magazine import Magazine # import your model files
from flask_app.models.user import User

@app.route('/dashboard')#main page of website, most links need to redirect here, make sure to check wireframe
def show_all_mags():
    if 'user_id' not in session:
        return redirect ('/')
    mags = Magazine.show_magazines_w_creator()
    user = User.get_one_by_id(data ={'id':session['user_id']})
    return render_template('dashboard.html',mags=mags, user = user)

@app.route('/magazine/new')# renders the template to create a new magazine
def create_magazine():
    if 'user_id' not in session:
        return redirect ('/')
    
    return render_template('CreateOne.html')

@app.route('/magazine/create',methods=['POST'])# post route to add new magazine
def magazine_post():
    if not Magazine.validate_mag(request.form):
        flash('check your inputs and try again')
        return redirect('/magazine/new')
    data ={
        'title':request.form["title"],
        'description':request.form["description"],
        'user_id':session["user_id"]
    }
    Magazine.add_one_magazine(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')# shows a magazine by its id
def show_one_mag(id):
    mag = Magazine.get_one_mag_by_id(data = {'id':id})
    user = User.get_one_by_id(data={'id':session['user_id']})
    return render_template('ShowOne.html',mag = mag,user=user)

@app.route('/delete/<int:id>')
def destroy_magazine(id):
    Magazine.destroy_mag_by_id(data={'id':id})
    
    return redirect('/dashboard')

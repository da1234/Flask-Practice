#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:51:58 2019

@author: RamanSB
"""


import functools
'''
#session is a dict that stores data across requests
#flash allows errors/messages to be displayed
#Blueprint an object that contains several related views/view functions.
#redirect (used in conjunction with url_for), render_template - as it says.

#url_for() function generates the URL to a view based on a name and arguments. 
 The name associated with a view is also called the endpoint, and by default it’s 
 the same as the name of the view function.
 '''
from flask import (
        Blueprint, flash, g, redirect, render_template, request, session, url_for
    )

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

#A view is a function that is programme to respond to a request within the flask 
#application. Views return data that Flask turns in to an outbound response

#Related views are oganized and grouped in to a Blueprint, which is registered 
#with the Flask Application.


#This will need to be registered with the application, within application factory
bp = Blueprint('auth', __name__, url_prefix='/auth') 
#creating blueprint obj with name auth, all urls associated with blueprint will be prepended with /auth

#First view - Register: auth/register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if(request.method == 'POST'): #If user submits request form , http request will = POST, then begin validations....
        username = request.form['username'] #requests.form is a dict
        password = request.form['password']
        db = get_db()
        error = None
        
        if(not username):
            error = "Username is required."
        if(not password):
            error = "Password is required."
        #Checking if username already exists.
        elif(db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None): #fetchone returns 1 record (row), fetchall, returns all matching records.
            error = 'User {} is already registered.'.format()
        #Validations done.
        if(error is None):
             db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                   (username, generate_password_hash(password))
        )
             db.commit() #hashing modifies the data, hence a commit is needed to verify the change.
             return redirect(url_for('auth.login'))
         
        flash(error) #flash stores messages that can be retrieved  when rendering template
    
    return render_template('auth/register.html') #renders html template
        
#Accessing '0.0.0.0:5000/auth/register' before the html template is created, throws
#jinja2.exceptions.TemplateNotFound
    

#Second view - login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if(request.method == 'POST'): #Begin validation
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
    
        if(user is None): #if db/sql(ite) query doesn't return any record for user, does not exist.
            error = "Incorrect username"
        elif(not check_password_hash(user['password'], password)): #checks hashed password in db, against password in form
            error = "Incorrect password"
        #end validation
    
    
        if(error is None):
            session.clear()
            session['user_id'] = user['id'] #session (imported) is also a dict, mapping session user_id key
            #to user's id (from db record).
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('auth/login.html') #renders html template
    
   
#If a user is logged in their information should be loaded and made available to other views.
#bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id') #Retreiving user_id from session object
    
    if(user_id is None):
        g.user = None
    else:
        g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?', (user_id, )
                ).fetchone()
        
#Logging out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_from('index'))        
     


'''
This decorator returns a new view function that wraps the original view it’s applied to. 
The new function checks if a user is loaded and redirects to the login page otherwise.
 If a user is loaded the original view is called and continues normally. 
You’ll use this decorator when writing the blog views.
https://docs.python.org/3/library/functools.html
'''
#Other functionality (view functions) requires user to be logged in, A decorater (annotation) 
#can be used to check this for each view it's applied to.
def login_required(view): 
    '''How this works: When we have a view function that requires the user to be logged in, we need to check
    if the user is logged in first, the wrapper function below checks this. In order for this to be called
    we simply add the annotation @login_required to all view functions that require users to be logged in.
    the wrapped_view function will be executed first and then subsequently (if logged in) the view function will be
    called.
        '''
    @functools.wraps(view) 
    def wrapped_view(**kwargs): #
        if(g.user is None):
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view
        
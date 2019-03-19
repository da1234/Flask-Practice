#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 00:33:06 2019

@author: RamanSB
"""

import os
from flask import Flask

message = "This is a practice python script to configure a flask application instance and host it locally"
#ApplicationFactory
'''This function will setup/configure a flask application and return the 
instance'''
def create_app(test_config=None):
    #create and configure app
    app = Flask(__name__, instance_relative_config=True) #File paths will be relative to the flaskr directory
    app.config.from_mapping(
                            SECRET_KEY='dev',
                            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if(test_config is None):
        #load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    
    from . import db #from this directory import db.py
    db.init_app(app) #this method registers the closing of db and initialization with the flask application.
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from .import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index') # app.add_url_rule() associates the endpoint name 'index' with the / url so that url_for('index') or url_for('blog.index') will both work, generating the same / URL either way.
    
    
    return app

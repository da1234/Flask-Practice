#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 21:08:20 2019

@author: RamanSB
"""

import sqlite3

import click
from flask import current_app, g #g is a special object
from flask.cli import with_appcontext


#Registering functions marked with ***  with the Application
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)




'''
This function initializes the database, current_app is used to open the schema.sql
file (relative to flaskr package/directory) which is then executed by the database
instance, (g.db).execute_script...
'''
def init_db():
    db = get_db() #essentially is g.db - our connection.
    
    with current_app.open_resource('schema.sql') as reso: 
        db.executescript(reso.read().decode('utf8'))
        
#Calls the above function (init_db)
@click.command('init-db') # defines a command line command called init-db that calls the init_db
@with_appcontext
def init_db_command(): #*** - Must be registered with application instance in order to be used.
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


#we store the connection to the database in one of g's attributes, (allows for reuse)
def get_db():
    if('db' not in g):
        g.db = sqlite3.connect( #Returns a Connection object: See (16.6.2.4): https://docs.python.org/2/library/multiprocessing.html#Connection
                current_app.config['DATABASE'], #current_app.config is a map, the key database maps to value of a file
                detect_types=sqlite3.PARSE_DECLTYPES # sqlite3 module parse the declared type for each column it return, i.e. for INTEGER PRIMARY KEY - will parse INTEGER[DECLARE TYPES]
                )
        g.db.row_factory = sqlite3.Row #returns rows that act as dicts, records are accessible via column name 
        
    return g.db

'''
 #will mention this method in the application factory within __init__.py,
  so that the db will be closed after each request.
 '''
def close_db(e=None): #*** - Must be registered with application instance in order to be used.
    db = g.pop('db', None) #checks if db exists as a key in the map, if the key
    # exists, then return the value, and remove the key-value in the map.
    
    if(db is not None): #if db exists then close
        db.close()
        
        


        
        
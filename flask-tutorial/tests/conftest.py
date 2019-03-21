#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 00:23:50 2019

@author: RamanSB
"""

import os
import tempfile #self-explanatory

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

#'rb' mode - read binary
with open(os.path.join(os.path.dir_name(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')
    

@pytest.fixture #remember, fixture is just a term for (SETUP function)
def app():
    db_fd, db_path = tempfile.mkstemp() #creates and opens a temporary file, returning both [file obj & file_path]
    
    #create_app takes 1 parameter, test_config (Dictionary)
    app = create_app({
            'TESTING': True, #Let's flask app know we are in test mode.
            'DATABASE': db_path,
            })
    
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
        
    yield app #what does the yield keyword do?
    
    os.close(db_fd)
    os.unlink(db_path) #check docs for this method
    
@pytest.fixture #Another set up function (for the client)
def client(app): #client will make requests to the application w/out running the server.
    return app.test_client()

@pytest.fixture
def runner(app): #creates a runner that can call the Click commands registered with the application
    return app.test_cli_runner()
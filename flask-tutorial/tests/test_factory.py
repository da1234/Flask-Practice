#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 17:37:12 2019

@author: RamanSB
"""

from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING' : True}).testing
    
def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
    
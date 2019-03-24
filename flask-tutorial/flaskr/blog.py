#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 19:01:13 2019

@author: RamanSB
"""

from flask import(
    Blueprint, flash, g, redirect, render_template, url_for, request        
)
from werkzeug.exceptions import abort #abort() will raise a special exception that returns an HTTP status code.
from flaskr.auth import login_required
from flaskr.db import get_db



bp = Blueprint('blog', __name__) #Need our flask instance to register this blueprint (see __init__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
            ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required 
def create():
    if(request.method == 'POST'):
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if(not title):
            error = "Title is required."
            
        if(error is not None):
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'INSERT INTO post (title, body, author_id)'
                    ' VALUES (?, ?, ?)',
                    (title, body, g.user['id'])
                    )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
            'SELECT p.id, title, body, created, author_id, username, p.likes'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?',
            (id, )
            ).fetchone()
    
    if(post is None):
        abort(404, "Post id {0} doesn't exist.".format(id))
        
    if(check_author and (post['author_id'] != g.user['id'])):
        abort(403)
        
    return post
            
@bp.route('/<int:id>/update', methods=('GET', 'POST')) #<int:id> corresponds to the integer id parameter to update function
@login_required
def update(id):
    post = get_post(id)
    
    if(request.method == 'POST'):
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if(not title):
            error = 'Title is required.'
            
        if(error is not None):
            flash(error)
        else:
            db = get_db()
            db.execute(
                    'UPDATE post'
                    ' SET title = ?,'
                    ' body = ?'
                    ' WHERE id = ?'
                    ,(title, body, id)
                    )
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/detail/<int:id>', methods=('GET',))
@login_required
def detail(id):
    post = get_post(id)
    return render_template('blog/detail.html', post=post)

@bp.route('/detail/<int:id>', methods=('POST',))
@login_required
def like_post(id):
    post = get_post(id)
    current_no_of_likes = post['likes']
    if(request.method=='POST'):
        db=get_db()
        db.execute('UPDATE post '
                   'SET likes = ? '
                   'WHERE id = ?'
                   , (current_no_of_likes+1, id)
                   )
        db.commit()
    
    return redirect(url_for('blog.detail', id=id))
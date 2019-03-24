from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    request
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

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
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
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
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    # getting post just to check that we are authorised to
    # delete the post
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


# view to show single blog post
@bp.route('/<int:id>/view', methods=('GET','POST'))
@login_required
def view_post(id):
    db = get_db()
    if request.method == 'GET':
        post = db.execute(
        'SELECT p.id, p.title, p.body, p.created, p.author_id, p.likes, u.username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id=?'
        ' ORDER BY created DESC',
        (id,)).fetchone()
        if db.execute(
        'SELECT user_id, post_id'
        ' FROM userPostReaction'
        ' WHERE user_id=? AND post_id = ?',
        (g.user['id'],id,)).fetchone() == None:
            return render_template('blog/view.html',post=post,liked=False)
        else:
            return render_template('blog/view.html',post=post,liked=True)
    elif request.method == 'POST':
        postId = request.form.get('id')
        userId = g.user['id']
        print(request.form.get('like'))
        if request.form.get('like') == 'true':
            print("post liked")
            db.execute(
                'INSERT INTO userPostReaction (user_id,post_id)'
                ' VALUES (?, ?)',
                (userId, postId,)
            )
            db.execute(
                'UPDATE post SET likes = likes + 1'
                ' WHERE id = ?', (id,)
            )
        else:
            print("post unliked")
            db.execute(
                'DELETE FROM userPostReaction'
                ' WHERE user_id = ? AND post_id = ?',
                (userId, postId,)
            )
            db.execute(
                'UPDATE post SET likes = likes - 1'
                ' WHERE id = ?', (id,)
            )
        db.commit()
        return redirect(url_for('blog.view_post',id=id))        

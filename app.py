from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb
from werkzeug.exceptions import abort

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'PABD_Projeto'
app.config['SECRET_KEY'] = '04130211'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = get_connection()
    cursor.execute('SELECT * FROM posts')
    posts = cursor.fetchall()
    cursor.close()
    return render_template('index.html', posts=posts)

def get_connection():
    cursor = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    return cursor

def get_post(post_id):
    cursor = get_connection()
    cursor.execute('SELECT * FROM posts WHERE id = %s', [post_id])
    post = cursor.fetchone()
    cursor.close()
    
    if post is None:
        abort(404)

    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('item.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    title=None

    if request.method == 'POST': 
        title = request.form['title'] 
        content = request.form['content'] 
        owner = request.form['owner'] 
    if not title:
        flash('Title is required!') 
    else:
        cursor = get_connection()
        cursor.execute('INSERT INTO posts (post_name, message, owner) VALUES (%s, %s, %s)', [title, content, owner])
        mysql.connection.commit()
        cursor.close()
        flash('Created Post') 
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    title=None
    post = get_post(id) # Pega o post referente
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        owner = request.form['owner']
    if not title:
        flash('Title is required!')
    else:
        cursor = get_connection()
        cursor.execute('UPDATE posts SET post_name = %s, message = %s, owner = %s WHERE id = %s',[title, content, owner, id])
        mysql.connection.commit()
        cursor.close()
        flash('Edited Post')
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    cursor = get_connection()
    cursor.execute('DELETE FROM posts WHERE id = %s', [id])
    mysql.connection.commit()
    cursor.close()
    flash("{} was successfully deleted!".format(post['post_name']))
    return redirect(url_for('index'))
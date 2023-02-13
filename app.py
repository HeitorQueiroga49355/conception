from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb
from werkzeug.exceptions import abort
from datetime import datetime

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

    current_datetime = datetime.now()
    current_date = str(current_datetime.day) + '/'+ str(current_datetime.month) + '/' + str(current_datetime.year) + ' - ' + str(current_datetime.hour) + ':' + str(current_datetime.minute)

    if request.method == 'POST': 
        title = request.form['title'] #
        author = request.form['author'] #
        creation_date = current_date ##
        begin_date = request.form['begin_date'] #
        finish_date = request.form['finishing_date'] #
        content = request.form['content'] # 
        last_time_edited = current_date ##
        priority = request.form['priority'] #
    if not title:
        flash('Title is required!') 
    else:
        cursor = get_connection()
        cursor.execute('INSERT INTO posts (title, author, creation_date, begining_date, finishing_date, content, last_time_edited, priority) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', [title, author, creation_date, begin_date, finish_date, content, last_time_edited, priority])
        mysql.connection.commit()
        cursor.close()
        flash('Created Post') 
        return redirect(url_for('index'))
    return render_template('create.html')

@app.errorhandler(404)
def erro(e):
    return render_template('404.html'), 404

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    title=None
    post = get_post(id)

    current_datetime = datetime.now()
    current_date = str(current_datetime.day) + '/'+ str(current_datetime.month) + '/' + str(current_datetime.year) + ' - ' + str(current_datetime.hour) + ':' + str(current_datetime.minute)
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        begin_date = request.form['begining_date']
        finish_date = request.form['finishing_date']
        content = request.form['content'] 
        last_time_edited = current_date
        priority = request.form['priority']
    if not title:
        flash('Title is required!')
    else:
        cursor = get_connection()
        cursor.execute('UPDATE posts SET title = %s, author = %s, begining_date = %s, finishing_date = %s, content = %s, last_time_edited = %s, priority = %s WHERE id = %s',[title, author, begin_date, finish_date, content, last_time_edited, priority, id])
        mysql.connection.commit()
        cursor.close()
        flash('Edited Post')
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    post = get_post(id)
    cursor = get_connection()
    cursor.execute('DELETE FROM posts WHERE id = %s', [id])
    mysql.connection.commit()
    cursor.close()
    flash("{} was successfully deleted!".format(post['title']))
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')
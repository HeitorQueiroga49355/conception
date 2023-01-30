import mysql.connector

conn = mysql.connector.connect(user='root',
                                password='',
                                host='127.0.0.1')

cursor = conn.cursor()

cursor.execute('CREATE DATABASE PABD_Projeto;')
cursor.execute('USE PABD_Projeto;')
cursor.execute('CREATE TABLE posts (id INT AUTO_INCREMENT PRIMARY KEY,'
                'title VARCHAR(255) NOT NULL,'
                'author VARCHAR(50) NOT NULL,'
                'creation_date VARCHAR(50) NOT NULL,'
                'is_reminder BOOLEAN DEFAULT FALSE,'
                'begining_date VARCHAR(50) NOT NULL,'
                'finishing_date VARCHAR(50),'
                'content VARCHAR(255) NOT NULL,'
                'last_time_edited VARCHAR(50) NOT NULL,'
                'priority VARCHAR(20) NOT NULL);')

conn.commit()
cursor.close()
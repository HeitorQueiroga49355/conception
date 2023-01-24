import mysql.connector

conn = mysql.connector.connect(user='root',
                                password='',
                                host='127.0.0.1')

cursor = conn.cursor()

cursor.execute('CREATE DATABASE PABD_Projeto;')
cursor.execute('USE PABD_Projeto;')
cursor.execute('CREATE TABLE posts (id INT AUTO_INCREMENT PRIMARY KEY,'
                'post_name VARCHAR(20) NOT NULL,'
                'message VARCHAR(50) NOT NULL,'
                'owner VARCHAR(20) NOT NULL);')

conn.commit()
cursor.close()
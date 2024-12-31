import mysql.connector #mariadb
#from flask import Flask, render_template, request, session, redirect

try:
	#連線DB
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="flappy_bird"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e)
	print("Error connecting to DB")
	exit(1)
	
def show_table():
	sql="SELECT p_id,name,score FROM `player` ORDER BY score DESC;"
	cursor.execute(sql,)
	return cursor.fetchall()

def insert_table(name, max_score):
	sql="INSERT INTO `player` (`p_id`, `name`, `score`) VALUES (NULL, %s, %s);"
	param=(name,max_score)
	cursor.execute(sql,param)
	conn.commit()
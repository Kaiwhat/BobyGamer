import mysql.connector

try:
    # 連線資料庫
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="flappy_bird"
    )
    # 建立 cursor 並設定回傳結果為 dictionary 型態
    cursor = conn.cursor(dictionary=True)
except mysql.connector.Error as e:
    print(e)
    print("Error connecting to DB")
    exit(1)
    
def show_table():
    sql = "SELECT p_id, name, score FROM `player` ORDER BY score DESC;"
    cursor.execute(sql)
    return cursor.fetchall()

def insert_table(name, max_score):
    sql = "INSERT INTO `player` (`p_id`, `name`, `score`) VALUES (NULL, %s, %s);"
    param = (name, max_score)
    cursor.execute(sql, param)
    conn.commit()

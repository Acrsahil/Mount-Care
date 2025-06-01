import mysql.connector

# Connect to MySQL

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",       # 🔁 Replace this
    password="root",   # 🔁 Replace this
    database="mountcare"     # 🔁 Replace this
)

cursor = conn.cursor()


print("sucessful")

cursor.execute("select * from products")

rows = cursor.fetchall()





pricelist = {row[1]: [row[2],row[3]] for row in rows}


import mysql.connector

# Connect to MySQL

def dbconnect():
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


    return {row[1]: [row[2],row[3]] for row in rows}

all_product = dbconnect()


for pro in all_product.items():
    print(pro)


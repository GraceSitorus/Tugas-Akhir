import mysql.connector

mydb = mysql.connector.connect(
    host = "localhoost",
    user = "root",
    password = "",
    database = "review_product"
)
print("database connected")
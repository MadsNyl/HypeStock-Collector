from db.settings import DATABASE, DB_HOST, DB_USERNAME, DB_PASSWORD
import mysql.connector

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    database=DATABASE
)

pool = db.cursor(buffered=True)
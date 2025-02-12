import psycopg2

connection = psycopg2.connect(database="mydb", user="g.fabi", password="postgres", host="localhost", port=5432)

cursor = connection.cursor()

cursor.execute("SELECT * from weather;")

# Fetch all rows from database
record = cursor.fetchall()

print("Data from Database:- ", record)
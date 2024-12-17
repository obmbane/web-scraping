import sqlite3

connection = sqlite3.connect('/mnt/c/Users/olwethu.mbane/Documents/data.db')

cursor = connection.cursor()

'''
#Insert new rows into database

new_rows = [('Migos','Johannesburg','2024.12.31'),('Boys 2 Men','Harare','2025.01.25')]

cursor.executemany("INSERT INTO events VALUES (?,?,?)", new_rows)
connection.commit()

'''
'''

#fetch all data based on a condition

cursor.execute("SELECT * FROM events WHERE band='Migos'")

'''



# fetch data from specific column

cursor.execute("SELECT date FROM events WHERE band='Backstreet Boys'")


result  = cursor.fetchall()

print(result)
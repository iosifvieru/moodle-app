import mariadb
import sys

try:
    conn = mariadb.connect( 
        user="tero",
        password="adawdasd",
        host="localhost",
        database="study_database"
    )
except mariadb.Error as e:
    print("Error: ", e)
    sys.exit(1)


cur = conn.cursor()

cur.execute('''
        CREATE TABLE IF NOT EXISTS test (
            id INT AUTO_INCREMENT PRIMARY KEY
        );
    ''')
conn.commit();



print(cur.execute("INSERT INTO test VALUES();"))
conn.commit();

cur.execute("SELECT * FROM test;")

rows = cur.fetchall();
for row in rows:
    print(row)

conn.close()
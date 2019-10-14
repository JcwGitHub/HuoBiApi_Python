import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

# execute SQL commands, commit if changes are needed

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");

# Save (commit) the changes

conn.commit()

# close the database when the operation is completed
# Just be sure any changes have been committed or they will be lost.

conn.close()
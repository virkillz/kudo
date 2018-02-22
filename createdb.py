import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE `hackathon` (`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,`name` TEXT,`kudoaddress` TEXT,`phone` TEXT,`email`	TEXT,`programming_skill`	TEXT,`university`	TEXT,`blockchain_interest`	INTEGER,`regid`	INTEGER)')

print("Table created successfully")

conn.close()

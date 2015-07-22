import sqlite3
con = sqlite3.connect('contact.db')
con.execute("CREATE TABLE contact (id INTEGER PRIMARY KEY, firstname char(50) NOT NULL,lastname char(50) NOT NULL, email char(100), phone char(50), notes char(500))")
con.execute("INSERT INTO contact (firstname,lastname,email,phone,notes) VALUES ('peace','cho','','','')")
con.execute("INSERT INTO contact (firstname,lastname,email,phone,notes) VALUES ('wilson','zhao','','','')")
con.commit()


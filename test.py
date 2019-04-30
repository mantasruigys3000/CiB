""""TEST FILE, NOT FOR PRODUCTION"""

import db_interact as db

database = db.Connect_db("final.db")

print(database.get_emp_password(1))


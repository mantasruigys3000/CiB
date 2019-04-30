""""TEST FILE, NOT FOR PRODUCTION"""

import db_interact as db

database = db.Connect_db("final.db")

#database.add_employee((9,"sick","Ruigys","qwerty","salt",2,"07539996909",2,2,2,"no","po123he","yes","green"))
print(database.get_parking_for_emp(1,"2019-06-01 20:10","2018-12-30 12:30"))


""""TEST FILE, NOT FOR PRODUCTION"""
from datetime import datetime
import db_interact as db

database = db.Connect_db("final.db")

#database.add_employee((9,"sick","Ruigys","qwerty","salt",2,"07539996909",2,2,2,"no","po123he","yes","green"))

time = [(),()]
print(database.get_colour_valid(2,datetime.strptime("2019-06-26 09:00",database.time_format),datetime.strptime("2019-06-26 12:00",database.time_format)))
print(database.get_roles())
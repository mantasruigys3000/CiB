""""TEST FILE, NOT FOR PRODUCTION"""
from datetime import datetime
import db_interact as db

database = db.Connect_db("final.db")

#database.add_employee((9,"sick","Ruigys","qwerty","salt",2,"07539996909",2,2,2,"no","po123he","yes","green"))

time = [["09:00","09:00"],["12:00","17:00"]]
print(database.get_colour_valid(2,datetime.strptime("2019-06-26 09:00",database.time_format),datetime.strptime("2019-06-26 12:00",database.time_format)))
print(database.get_roles())

#print(database.csv_total_bookings_emp_range(1,"2019-07-01","2019-07-07"))
print(database.csv_multi_emp([1,2,3]))

#print(database.emp_book_week(1,"2019-W26",time))

print(database.get_emp_bookings(1))
database.write_csv(database.csv_total_bookings(),"report")
import sqlite3
import datetime as dt
from datetime import datetime
import csv



class Connect_db:
    def __init__(self,f_path="new.db"):

        if not (f_path.endswith(".db")):
            print("file was not .db file")
            f_path ="new.db"

        self.time_format = "%Y-%m-%d %H:%M"
        self.week_format = "%Y-%m-%d"
        self.role_dict = {"employee":1,"manager":2,"facilitator":4,"admin":8}
        self.connection = sqlite3.connect(f_path)
        self.curs = self.connection.cursor()
    
    def make_dummy_tables(self):
        emp_tbl = "CREATE TABLE employee (id,first_name,last_name,password,salt,department,mobile_number,extension_number,worker_type,role,blue_badge,post_code,parking_authourised,parking_badge_colour)"
        self.curs.execute(emp_tbl)
        self.connection.commit()
        print("Employee Table Made")

    def insert_dummy_data(self): #ONLY FOR TESTING
        values = (1,"Mantas","Ruigys","qwerty","salt",1,"07539996909",2,1,4,"no","po123he","yes","green")
        self.curs.execute("INSERT INTO employee VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)
        self.connection.commit()
        print("Values Inserted Into Employee")
    
    def get_emp_role(self,employee_id):
        query = "select role from employee where id=?"
        self.curs.execute(query,(employee_id,))
        result = self.curs.fetchone()
        return result[0]

    def add_employee(self,values = ()):
        self.curs.execute("INSERT INTO employee VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",values)
        self.connection.commit()
        print("Employee Added")

    def emp_update(self,values = ()):
        if values == ():
            return
        e_id = values[0]

        self.curs.execute("DELETE FROM employee WHERE id=?",(e_id,))
        
        self.add_employee(values)

        #self.curs.execute(query,values)
        self.connection.commit()
        print("employee updated")
        
        

    def set_emp_password(self,employee_id,password_str, salt):
        row = "password"
        query = "UPDATE employee SET password=?,salt=? WHERE id=?"

        self.curs.execute(query,(password_str[0],str(salt),employee_id,))
        self.connection.commit()
        return True


    
    
    def get_emp_ALL(self,employee_id):
        query = "select * from employee where id=?"
        self.curs.execute(query,(employee_id,))
        result = self.curs.fetchone()
        return result

    def get_emp_password(self,employee_id):
        query = "select password from employee where id=?"
        self.curs.execute(query,(employee_id,))
        result = self.curs.fetchone()
        return result[0]

        
    def convert_datetime(self,date):
            print(date)

            
    def get_parking_for_emp(self,employee_id,start_time,end_time):

        if not isinstance(start_time,datetime):
            obj_start_time = datetime.strptime(start_time,self.time_format)
        else:
             obj_start_time = start_time
        #print(obj_start_time)
        if not isinstance(end_time,datetime):
            obj_end_time = datetime.strptime(end_time,self.time_format)
        else:
            obj_end_time = end_time

        query = "SELECT department FROM employee WHERE id=?"
        self.curs.execute(query,(employee_id,))
        dept = self.curs.fetchone()[0]

        query = "SELECT id FROM employee where department=?"
        self.curs.execute(query,(dept,))
        all_emp = self.curs.fetchall()

        dates = []
        print(all_emp)
        query = "SELECT datetime_start, datetime_end From employee_timetable where employee_id=?"
        for i in all_emp:
            j = i[0]
            print(j)
            self.curs.execute(query,(j,))
            new_dates = self.curs.fetchone()
            print(new_dates)
            new_start = datetime.strptime(new_dates[0],"%d-%m-%Y %H:%M")
            new_end = datetime.strptime(new_dates[1],"%d-%m-%Y %H:%M")

            new_tup = (new_start,new_end)
            self.convert_datetime(new_dates[0].split("-"))
            dates.append(new_tup)
            
        print(dates)

        query = "SELECT total_spaces FROM department_parking WHERE department_number=?"
        self.curs.execute(query,(dept,))
        total_spaces = self.curs.fetchone()[0]

        for d in dates:
            if not ((obj_start_time >= d[1]) or (obj_end_time <= d[0])):
                total_spaces-=1



        return total_spaces

        

    def add_session(self,values=()):
        if values == ():
            print("Values is empty for creating a session")

        self.curs.execute("INSERT INTO session VALUES (?,?,?,?)",values)
        print("session added")
        self.connection.commit()

    def get_session_by_ip_token(self,ip,token):
        self.curs.execute("SELECT * From session WHERE ip_address=? AND token=?",(ip,token,))
        return self.curs.fetchone()

    
    def add_vehicle(self,values = ()):
        self.curs.execute("INSERT INTO vehicle VALUES (?,?,?,?)",values)
        self.connection.commit()

    def delete_vehicle(self,v_reg):

        self.curs.execute("DELETE FROM vehicle WHERE registration=?",(v_reg,))
        print("vehicle deleted")
        self.connection.commit()

    def get_vehicles(self):
        self.curs.execute("SELECT * FROM vehicle")
        tup = self.curs.fetchall()
        print(tup)

    def add_booking(self,values = ()):
        l = list(values)
        l.append("None")
        tup = tuple(l)

        self.curs.execute("INSERT INTO employee_timetable VALUES (?,?,?,?)",tup)
        print("Booking created")
        self.connection.commit()

    def emp_assign_colour(self,e_id,colour):
        self.curs.execute("UPDATE employee SET parking_badge_colour=? WHERE id=?",(colour,e_id,))
        print("Colour Set")
        self.connection.commit()


    def get_colour_valid(self,e_id,start_time,end_time):

        #get colour
        self.curs.execute("SELECT parking_badge_colour FROM employee where id=?",(e_id,))
        col = self.curs.fetchone()[0]
        print(col)
        # Get weeks commencing
        self.curs.execute("SELECT date FROM badge_dates WHERE colour=?",(col,))
        weeks = self.curs.fetchall()

        for week in weeks:
            week_start = datetime.strptime(week[0],"%d-%m-%Y %H:%M")
            week_end = week_start + dt.timedelta(days=7)

            if(start_time >= week_start and end_time <= week_end):
                return True

        return False

    def emp_book_week(self,e_id,wk,times = []):
        wk += '-1'
        wk += ' 00:00'
        print(times)
        week = datetime.strptime(wk,"%Y-W%W-%w %H:%M")
        week -= dt.timedelta(days=7)
        print(week)
        

        for l in range(len(times[0])):
            start_minutes = datetime.strptime(times[0][l],"%H:%M")
            end_minutes = datetime.strptime(times[1][l],"%H:%M")

            current_week = week + dt.timedelta(days=l)
            #current_week = week
            start_time = current_week + dt.timedelta(minutes=start_minutes.minute,hours=start_minutes.hour)
            end_time = current_week + dt.timedelta(minutes=end_minutes.minute,hours=end_minutes.hour)

            

            
            if self.get_colour_valid(e_id,start_time + dt.timedelta(days=1),end_time + dt.timedelta(days=1)):
                if (self.get_parking_for_emp(e_id,start_time ,end_time ) > 0):
                    self.add_booking((e_id,start_time,end_time))
                else:
                    return "Could not make booking not enough space"
            else:
                return "Invalid Week"

        return True
    def booking_details(self,):
        self.curs.execute("SELECT * FROM employee_timetable")
        bookings = self.curs.fetchall()
        return bookings #not frontend use


    def get_roles(self):
            self.curs.execute("SELECT * FROM roles")
            tbl = self.curs.fetchall()
            dic = {}

            for tup in tbl:
                dic[tup[1]] = tup[0]

            return dic

    def csv_total_bookings_emp_range(self,e_id,date_from,date_to):
        start_time = datetime.strptime(date_from + " 00:00",self.time_format)
        end_time = datetime.strptime(date_to + " 00:00",self.time_format)

        self.curs.execute("SELECT datetime_start,datetime_end FROM employee_timetable where employee_id=?",(e_id,))
        tbl = self.curs.fetchall()
        count = 0
        for i in tbl:
            table_date_from = i[0]
            table_date_to = i[1]


            try:
               table_date_from = datetime.strptime(table_date_from,"%Y-%m-%d %H:%M:%S")
               table_date_to = datetime.strptime(table_date_to,"%Y-%m-%d %H:%M:%S")
            except ValueError:
              table_date_from = datetime.strptime(table_date_from,"%d-%m-%Y %H:%M")
              table_date_to = datetime.strptime(table_date_to,"%d-%m-%Y %H:%M")
              pass

            if(table_date_from > start_time and table_date_to < end_time):
                count += 1


        
        start_time = start_time.strftime(self.time_format)
        end_time = end_time.strftime(self.time_format)


        tup = [e_id,start_time,end_time,count]
        newtup = [["Employee_id","Start_Time","End_Time","Count"]]
        newtup.append(tup)
        return newtup

    def csv_total_bookings_emp_colour(self,colour):
        self.curs.execute("SELECT id FROM employee WHERE parking_badge_colour=?",(colour,))
        colour_emp = self.curs.fetchall()
        count = 0
        for i in colour_emp:
            e_id = i[0]
            self.curs.execute("SELECT employee_id FROM employee_timetable where employee_id=?",(e_id,))
            emps_found = self.curs.fetchall()
            if emps_found != None:
                count += len(emps_found)

        details = self.booking_details()
        dic = []
        dic.append(["Employee_ID","Colour","Time_From","Time_To","Vehicle_Registration"])

        for i in details:
            
            self.curs.execute("SELECT parking_badge_colour FROM employee Where id=? ",(i[0],))
            c = self.curs.fetchone()[0]
            if c == colour:
                lil_dic = []
                lil_dic.append(i[0])
                lil_dic.append(c)
                lil_dic.append(i[1])
                lil_dic.append(i[2])
                lil_dic.append(i[3])
                dic.append(lil_dic)

            

        tup = dic
        return tup

    def csv_total_bookings(self):
        #get colours
        self.curs.execute("SELECT * FROM employee_timetable")
        bookings = self.curs.fetchall()
        dic = []
        dic.append(["Employee_ID","Colour","Time_From","Time_To","Vehicle_Registration"])

        for i in bookings:
            lil_dic = []
            lil_dic.append(i[0])
            self.curs.execute("SELECT parking_badge_colour FROM employee Where id=? ",(i[0],))
            col = self.curs.fetchone()[0]
            lil_dic.append(col)
            lil_dic.append(i[1])
            lil_dic.append(i[2])
            lil_dic.append(i[3])

            dic.append(lil_dic)

        return dic

        

    def csv_total_bookings_multi_colour(self,colours = []):
        dic = []
        dic.append(["Employee_ID","Colour","Time_From","Time_To","Vehicle_Registration"])
        for c in colours:
            tbl = self.csv_total_bookings_emp_colour(c)
            for i in range(1,len(tbl)):
                dic.append(tbl[i])
        
        return dic
    
    def csv_single_emp(self,e_id):
        emp =  self.get_emp_ALL(e_id)
        attributes = [0,1,2,5,6,7,8,9,10,11,12,13]
        dic = []
        dic.append(["Employee ID","First Name","Last Name","Department","Mobile No","Extention No","Type","Role","Blue Badge","PO CODE","Parking authorised","Badge Colour"])
        lil_dic = []
        for num in attributes:
            
            lil_dic.append(emp[num])
            
        dic.append(lil_dic)

        return dic

    def csv_multi_emp(self,ids = []):

        dic = []
        dic.append(["Employee ID","First Name","Last Name","Department","Mobile No","Extention No","Type","Role","Blue Badge","PO CODE","Parking authorised","Badge Colour"])

        for id in ids:
            dic.append(self.csv_single_emp(id)[1])
        
        return dic



    def get_emp_bookings(self,id):
        self.curs.execute("SELECT * FROM employee_timetable Where employee_id =?",(id,))
        return self.curs.fetchall()


    

    def get_check_car_valid(self,reg,time):
        self.curs.execute("SELECT employee_id FROM vehicle WHERE registration=?",(reg,))
        e_id = self.curs.fetchone()
        if e_id == None:
            return ("Car not in database")
        else:
            return self.get_colour_valid(e_id[0],time,time)

    def write_csv(self,tbl,name):

        with open("Reports/"+name + ".csv", 'w',newline = '') as csvFile:
            writer = csv.writer(csvFile,lineterminator='\n')
            writer.writerows(tbl)

        csvFile.close()

    

    


                
        

        

    






        


        




        




    
    def isRole(self,role_name,employee_id):
        

        if role_name in self.role_dict:
            if self.get_emp_role(employee_id) & self.role_dict[role_name]:
                return True
            else:
                return False
        return False

    def listRoles(self,users_role):
        roles_list = list()
        for role, flag in self.role_dict.items():
            if flag & users_role:
                roles_list.append(role)
        
        return roles_list




    





        
    


import sqlite3
from datetime import datetime



class Connect_db:
    def __init__(self,f_path="new.db"):

        if not (f_path.endswith(".db")):
            print("file was not .db file")
            f_path ="new.db"

        self.time_format = "%Y-%m-%d %H:%M"
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
        
        

    def set_emp_password(self,employee_id,password_str):
        row = "password"
        query = "UPDATE employee SET password=? WHERE id=?"

        self.curs.execute(query,(password_str,employee_id,))
        self.connection.commit();


    
    
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
        obj_start_time = datetime.strptime(start_time,self.time_format)
        #print(obj_start_time)
        obj_end_time = datetime.strptime(end_time,self.time_format)

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
            new_start = datetime.strptime(new_dates[0],self.time_format)
            new_end = datetime.strptime(new_dates[1],self.time_format)

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




    





        
    


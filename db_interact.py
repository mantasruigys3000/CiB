import sqlite3


class Connect_db:
    def __init__(self,f_path="new.db"):

        if not (f_path.endswith(".db")):
            print("file was not .db file")
            f_path ="new.db"

         
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




    





        
    


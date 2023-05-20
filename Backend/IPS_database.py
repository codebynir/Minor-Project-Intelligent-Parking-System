'''
INTELLIGENT PARKING SYSTEM DATABASE PROGRAM

DATABASE Name 'ips_db'
Contains Three TABLES :
    1. user_table (fname, email, password)
    2. member_table (fname, email, address, contact, password)
    3. company_table (company, address, block, slots, ip_address, email, id[PK, AI])
'''



class IPS_db:
    def __init__(self, mysql):
        self.mysqldb = mysql.connection
        
    def insert_user(self, fname, email, password):
        mycursor = self.mysqldb.cursor()#cursor() method create a cursor object    
        try:  
            #Execute SQL Query to insert record 
            mycursor.execute(f"INSERT INTO user_table VALUES('{fname}', '{email}', '{password}');")
            self.mysqldb.commit() # Commit is used for your changes in the database  
            print('Record inserted successfully...')  
        except:
            # rollback used for if any error   
            self.mysqldb.rollback()  
            print("Error occured during insertion...")
        self.mysqldb.close()#Connection Close  


    def match_user_data(self, email, password):
        mycursor = self.mysqldb.cursor()#cursor() method create a cursor object 
        valid_user = False
        try:
            #Execute SQL Query to select user record 
            mycursor.execute(f"SELECT * FROM user_table WHERE email = '{email}';")  
            user_data = mycursor.fetchall() #fetches all the rows
            for row in user_data:
                if row[2] == password:
                    valid_user = True
        except:   
            print('Error:Unable to fetch data.')
        self.mysqldb.close()#Connection Close
        return valid_user        
    
    def insert_member(self, fname, email, contact, address, password):
        mycursor = self.mysqldb.cursor()#cursor() method create a cursor object    
        try:  
            #Execute SQL Query to insert record 
            mycursor.execute(f"INSERT INTO member_table VALUES('{fname}', '{email}', '{address}', '{contact}', '{password}');")
            self.mysqldb.commit() # Commit is used for your changes in the database  
            print('Record inserted successfully...')  
        except:
            # rollback used for if any error   
            self.mysqldb.rollback() 
            print("Error occured during insertion...")
        self.mysqldb.close()#Connection Close  
    
    def match_member_data(self, email, password):
        mycursor = self.mysqldb.cursor()#cursor() method create a cursor object 
        valid_member = False
        try:
            #Execute SQL Query to select user record
            mycursor.execute(f"SELECT * FROM member_table WHERE email = '{email}';")  
            member_data = mycursor.fetchall() #fetches all the rows
            for row in member_data:
                if row[4] == password:
                    valid_member = True
        except:   
            print('Error:Unable to fetch data...')
        self.mysqldb.close()#Connection Close
        return valid_member        
    
    def add_company_info(self, company, address, block, slots, ip_address, email):
        mycursor = self.mysqldb.cursor()#cursor() method create a cursor object    
        try:  
            #Execute SQL Query to insert record 
            mycursor.execute(f"INSERT INTO company_table(company, address, block, slots, ip_address, email) VALUES('{company}', '{address}', '{block}', '{slots}', '{ip_address}', '{email}');")
            self.mysqldb.commit() # Commit is used for your changes in the database  
            print('Record inserted successfully...')  
        except:
            # rollback used for if any error   
            self.mysqldb.rollback() 
            print("Error occured during insertion...")
        self.mysqldb.close()#Connection Close  

    def update_company_info(self, company, address, block, slots, ip_address, email, id):
        mycursor = self.mysqldb.cursor()#cursor() method create a cursor object    
        try:  
            #Execute SQL Query to insert record
            mycursor.execute(f"UPDATE company_table SET company = '{company}', address = '{address}', block = '{block}', slots = '{slots}', ip_address = '{ip_address}', email = '{email}' WHERE id = {int(id)};")
            self.mysqldb.commit() # Commit is used for your changes in the database  
            print('Record updated successfully...')  
        except:
            # rollback used for if any error   
            self.mysqldb.rollback()  
            print("Error occured during updation...")
        self.mysqldb.close()#Connection Close  
    
    def insert_booking_details(self, company, parking_time, parking_duration, contact, email, name, vehicle_no, amount):
        mycursor = self.mysqldb.cursor()#cursor() method create a cursor object    
        try: 
            #Execute SQL Query to insert record 
            mycursor.execute(f"INSERT INTO booking_table(company, parking_time, parking_duration, contact, email, name, vehicle_no, amount) VALUES('{company}', '{parking_time}', '{parking_duration}', '{contact}', '{email}', '{name}', '{vehicle_no}', '{amount}');")
            self.mysqldb.commit() # Commit is used for your changes in the database  
            print('Record inserted successfully...')  
        except:
            # rollback used for if any error   
            self.mysqldb.rollback() 
            print("Error occured during insertion...")
        self.mysqldb.close()#Connection Close  
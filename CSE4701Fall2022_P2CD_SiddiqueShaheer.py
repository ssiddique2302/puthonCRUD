import mysql.connector
from tabulate import tabulate

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='company_database')
mc = cnx.cursor(buffered=True)

comm = ''

while(comm != '0'):
    print("Welcome to the company database!")
    print()
    print("MENU")
    print("(1) Add new employee")
    print("(2) View employee")
    print("(3) Modify employee")
    print("(4) Remove employee")
    print("(5) Add new dependent")
    print("(6) Remove dependent")
    print("(7) Add new department")
    print("(8) View department")
    print("(9) Remove department")
    print("(10) Add department location")
    print("(11) Remove department location")
    print("(0) Exit")
    comm = input("Select the number of desired option: ")

    if comm == '1':
        print()
        print("START")
        print("----------------------------")
        print()
        Fname_input = input('Enter employee first name: ')
        Minit_input = input("Enter middle initial of employee: ")
        Lname_input = input("Enter last name of employee: ")
        Ssn_input = input("Enter employee socual security number: ")
        Bdate_input = input("Enter employee birth date as YYYY-MM-DD: ")
        Address_input = input("Enter employee address: ")
        Sex_input = input("Enter employee sex: ")
        Salary_input = float(input("Enter employee salary: "))
        Salary_input = '%.2f' % Salary_input
        Super_ssn_input = input("Enter employee supervisor social security number: ")
        Dno_input = int(input("Enter employee department number: "))

        try:
            mc.execute("Insert into employee (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
            (Fname_input, Minit_input, Lname_input, Ssn_input, Bdate_input, Address_input, Sex_input, Salary_input, Super_ssn_input, Dno_input))
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))
        cnx.commit()
        print()
        print("DONE")
        print("----------------------------")
        print()

    elif comm == '2': #TODO fix so in one statement  
        print()
        print("START")
        print("----------------------------")
        print()
        Ssn_lookup = input("Enter employee ssn to view: ")

        mc.execute("select employee.Fname, employee.Minit, employee.Lname, employee.Ssn, employee.Bdate, employee.Address, employee.Sex, employee.Salary, Employee.Super_ssn, employee.Dno, e.Fname, e.Minit, e.Lname, department.Dname, dependent.Dependent_name, dependent.Sex, dependent.Bdate, dependent.Relationship from (((employee as e join employee on e.Ssn = employee.Super_ssn) join department on department.dnumber = employee.Dno) join dependent on dependent.Essn = employee.Ssn) where employee.ssn = %s",(Ssn_lookup,))
        
        #cnx.commit()
        results = mc.fetchall()

        print(tabulate(results, headers=['Fname', 'Minit', 'Lname', 'Ssn', 'Bdate', 'Address', 'Sex', 'Salary', 'Super_ssn', 'Dno', 'Fname', 'Minit', 'Lname', 'Dname', 'Dependent_name', 'Sex', 'Bdate', 'Relationship'], tablefmt='psql'))

        print()
        print("DONE")
        print("----------------------------")
        print()

    elif comm == '3':
        print()
        print("START")
        print("----------------------------")
        print()
        #mc.execute("LOCK TABLE employee READ")

        print("Modifying employee...")
        Ssn_update = input("Enter employee's SSN: ")
        mc.execute("select * from employee where Ssn = %s FOR SHARE",(Ssn_update,))
        
        update = ''

        while (update != '0'):
            
            print("(1) Address")
            print("(2) Sex")
            print("(3) Salary")
            print("(4) Supervisor's SSN")
            print("(5) Department number")
            print("(0) Finish")
            update = input("Enter number of field to update: ")

            if update == '1':
                Address_update = input("Enter new address: ")

                #mc.execute("select * from employee where Ssn = %s FOR SHARE",(Ssn_update,))
                mc.execute("update employee set Address = %s where Ssn = %s", (Address_update, Ssn_update))
                cnx.commit()
                
            
            elif update == '2':
                Sex_update = input("Enter new sex: ")

                #mc.execute("select * from employee where Ssn = %s FOR SHARE",(Ssn_update,))
                mc.execute("update employee set Sex = %s where Ssn = %s", (Sex_update, Ssn_update))
                cnx.commit()

            elif update == '3':
                Salary_update = float(input("Enter new sex: "))
                Salary_update = '%.2f' % Salary_update

                #mc.execute("select * from employee where Ssn = %s FOR SHARE",(Ssn_update,))
                mc.execute("update employee set Salary = %s where Ssn = %s", (Salary_update, Ssn_update))
                cnx.commit()
        

            elif update == '4':
                Super_ssn_update = input("Enter new supervisor social security number: ")

                #mc.execute("select * from employee where Ssn = %s FOR SHARE",(Ssn_update,))
                mc.execute("update employee set Super_ssn = %s where Ssn = %s", (Super_ssn_update, Ssn_update))
                cnx.commit()
                
            
            elif update == '5':
                #mc.execute("select * from employee where Ssn = %s FOR SHARE",(Ssn_update,))
                Department_update = input("Enter new department number: ")

                
                mc.execute("update employee set Dno = %s where Ssn = %s", (Department_update, Ssn_update))
                cnx.commit()
                

    

        #mc.execute("UNLOCK TABLES")
        print()
        print("DONE")
        print("----------------------------")
        print()
    
    elif comm == '4': 
        print()
        print("START")
        print("----------------------------")
        print()
        
        # checking dependencies would mean if they are anyone's supervisor
        # essn, and dependent also 
        #mc.execute("LOCK TABLE employee WRITE")

        print("Deleting employee...")
        Ssn_delete = input("Enter employee's SSN: ")
        
        

        mc.execute("Select * from employee where Ssn = %s FOR SHARE",(Ssn_delete,))
        to_delete = input("Confirm deletion [yes/no]? ")

        # if this is all set, delete from employee, delete from works on, delete from manger if they in there

        if to_delete == 'yes':
            try:
                mc.execute("delete from employee where Ssn = %s", (Ssn_delete,))
            except mysql.connector.IntegrityError as err:
                print("Error: {}".format(err))
            
            cnx.commit()

            
            #for i in mc:
             #   elem = i[0]
              #  isManager = int(elem)

            
            

        #mc.execute("UNLOCK TABLES")
        print()
        print("DONE")
        print("----------------------------")
        print()

        pass
    
    elif comm == '5':
        print()
        print("START")
        print("----------------------------")
        print()
        #mc.execute("LOCK TABLE Dependent WRITE")
        print("Adding dependent...")

        Essn_for_new_dependent = input("Enter employee social security number for new dependent: ")

        mc.execute("select * from dependent where Essn = %s", (Essn_for_new_dependent,))

        results = mc.fetchall()

        print(tabulate(results, headers=['Essn', 'Dependent_name', 'Sex', 'Bdate', 'Relationship'], tablefmt='psql'))

        mc.execute("Select * from employee where Ssn = %s for share",(Essn_for_new_dependent,))

        new_Dependent_name = input("Enter new dependent name: ")
        new_Dependent_sex = input("Enter new dependent sex: ")
        new_Dependent_bdate = input("Enter new dependent birth date as YYYY-MM-DD: ")
        new_Dependent_relationship = input("Enter new dependent relationship: ")

        mc.execute("Insert into dependent (Essn, Dependent_name, Sex, Bdate, Relationship) values (%s,%s,%s,%s,%s)", (Essn_for_new_dependent, new_Dependent_name, new_Dependent_sex, new_Dependent_bdate, new_Dependent_relationship))
        cnx.commit()
        

        #mc.execute("UNLOCK TABLES")
        print()
        print("DONE")
        print("----------------------------")
        print()

    elif comm == '6':
        print()
        print("START")
        print("----------------------------")
        print()
        #mc.execute("LOCK TABLE Dependent WRITE")
        print("Deleting employee's dependent...")

        Essn_for_delete_dependent = input("Enter employee social security number to remove dependnet: ")

        mc.execute("select * from dependent where Essn = %s", (Essn_for_delete_dependent,))
        results = mc.fetchall()

        print(tabulate(results, headers=['Essn', 'Dependent_name', 'Sex', 'Bdate', 'Relationship'], tablefmt='psql'))


        mc.execute("Select * from employee where ssn = %s for share",(Essn_for_delete_dependent,))

        remove_Dependent_name = input("Enter name for dependent to remove: ")

        mc.execute("delete from dependent where Essn = %s and dependent_name = %s", (Essn_for_delete_dependent, remove_Dependent_name))
        cnx.commit()
        #mc.execute("UNLOCK TABLES")
        print()
        print("DONE")
        print("----------------------------")
        print()

    elif comm == '7':
        print()
        print("START")
        print("----------------------------")
        print()
        new_Dname = input("Enter name for new department: ")
        new_Dno = int(input("Enter department number for new department: "))
        new_deparment_manager_Ssn = input("Enter manager social security number for new departnent: ")
        new_deparment_manager_start_date = input("Enter new department mangaer start date as YYYY-MM-DD: ")

        try:
            mc.execute("Insert into department (Dname, Dnumber, Mgr_ssn, Mgr_start_date) values (%s, %s, %s, %s)",(new_Dname, new_Dno, new_deparment_manager_Ssn, new_deparment_manager_start_date))
        except mysql.connector.IntegrityError as err:
            print("Error: {}".format(err))
        
        cnx.commit()
        print()
        print("DONE")
        print("----------------------------")
        print()


    elif comm == '8':
        print()
        print("START")
        print("----------------------------")
        print()
        Dnumber_to_view = int(input("Enter department number to view: "))

        mc.execute("select Dname, Fname, Minit, Lname, DLocation from (department join dept_locations on department.Dnumber = dept_locations.Dnumber) join employee on Mgr_ssn = employee.Ssn where department.Dnumber = %s",(Dnumber_to_view,))
        
        results = mc.fetchall()

        print(tabulate(results, headers=['Dname', 'Fname', 'Minit', 'Lname', 'Dlocation'], tablefmt='psql'))

        print()
        print("DONE")
        print("----------------------------")
        print()

    elif comm == '9':
        print()
        print("START")
        print("----------------------------")
        print()
        #mc.execute("LOCK TABLE Department WRITE")
        print("Deleting department...")
        Dnumber_to_delete = input("Enter department number to delete: ")

        mc.execute("select * from department where Dnumber = %s",(Dnumber_to_delete,))
        
        results = mc.fetchall()

        print(tabulate(results, headers=['Dname', 'Dnumber', 'Mgr_ssn', 'Mgr_start_date'], tablefmt='psql'))


        mc.execute("Select * from Department where Dnumber = %s for share",(Dnumber_to_delete,))
        confirm_delete = input("Confirm deletion [yes/no]? ")

        if confirm_delete == 'yes':
            try:
                mc.execute("delete from department where Dnumber = %s", (Dnumber_to_delete,))
            except mysql.connector.IntegrityError as err:
                print("Error: {}".format(err))
            
            cnx.commit()
        
        #mc.execute("UNLOCK TABLES") 
        print()
        print("DONE")
        print("----------------------------")
        print()     
        

    elif comm == '10':
        print()
        print("START")
        print("----------------------------")
        print()
        #mc.execute("LOCK TABLE dept_locations WRITE")
        print("Adding new location...")
        new_location_Dnumber = int(input("Enter department number to add new location: "))

        mc.execute("select * from dept_locations where dnumber = %s", (new_location_Dnumber,))
        results = mc.fetchall()

        print(tabulate(results, headers=['Dnumber', 'Dlocation'], tablefmt='psql'))


        mc.execute("Select * from Department where Dnumber = %s for share",(new_location_Dnumber,))
        location = input("Enter new location: ")

        mc.execute("insert into dept_locations (Dnumber, Dlocation) values (%s, %s)", (new_location_Dnumber, location))
        cnx.commit
        #mc.execute("UNLOCK TABLES")
        print()
        print("DONE")
        print("----------------------------")
        print()
        pass

    elif comm == '11':
        print()
        print("START")
        print("----------------------------")
        print()
        #mc.execute("LOCK TABLE dept_locations WRITE")
        print("Deleting location...")
        Dnumber_location_delete = int(input("Enter department number to delete location"))

        mc.execute("select * from dept_locations where Dnumber = %s", (Dnumber_location_delete,))

        results = mc.fetchall()

        print(tabulate(results, headers=['Dnumber', 'Dlocation'], tablefmt='psql'))

        mc.execute("Select * from Department where Dnumber = %s for share",(Dnumber_location_delete,))
        location_to_delete = input("Enter location to delete: ")

        mc.execute("delete from dept_locations where Dnumber = %s and Dlocation = %s", (Dnumber_location_delete, location_to_delete))
        cnx.commit()
        
        print()
        print("DONE")
        print("----------------------------")
        print()
        pass





cnx.close()
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
import mysql.connector
import datetime
from xlsxwriter import *
from xlrd import *
import pyqtgraph as pg

MainUI,_ = loadUiType('main.ui')


employee_id = 0
employee_branch = 1


class Main(QMainWindow , MainUI):
    def __init__(self , parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.UI_Changes()
        self.Db_Connect()
        self.Handel_Buttons()

        self.get_dashboard_data()

        # self.Open_Daily_movements_Tab()
        self.Show_All_Categories()
        self.Show_Branchies()
        self.Show_Publishers()
        self.Show_Authors()

        ##
        self.Show_All_Books()
        self.Show_All_CLients()
        self.Show_Employee()
        self.Retreive_Day_Work()
        self.Show_History()


    def UI_Changes(self):
        ## UI Changes in Login
        self.tabWidget.tabBar().setVisible(False)


    def Db_Connect(self):
        ## coneection between app and DB
        self.db = mysql.connector.connect(host='localhost' ,user='root', password='toor', db='lb')
        self.cur = self.db.cursor()
        print('Connection Accepted')


    def Handel_Buttons(self):
        ## Handel All Buttons In Our App
        self.pushButton.clicked.connect(self.Open_Daily_movements_Tab)
        self.pushButton_2.clicked.connect(self.Open_Books_Tap)
        self.pushButton_3.clicked.connect(self.Open_CLients_Tap)
        self.pushButton_4.clicked.connect(self.Open_Dashboard_Tap)
        self.pushButton_7.clicked.connect(self.Open_History_Tap)
        self.pushButton_6.clicked.connect(self.Open_Report_Tap)
        self.pushButton_5.clicked.connect(self.Open_Settings_Tab)


        self.pushButton_8.clicked.connect(self.Handel_to_Day_Work)
        self.pushButton_19.clicked.connect(self.Add_Branch)
        self.pushButton_20.clicked.connect(self.Add_Publisher)
        self.pushButton_21.clicked.connect(self.Add_Author)
        self.pushButton_22.clicked.connect(self.Add_Category)

        self.pushButton_27.clicked.connect(self.Add_Employee)
        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_15.clicked.connect(self.Add_New_Client)

        self.pushButton_12.clicked.connect(self.Edit_Book_search)
        self.pushButton_11.clicked.connect(self.Edit_Book)
        self.pushButton_13.clicked.connect(self.Delete_Book)
        self.pushButton_9.clicked.connect(self.All_Books_Filter)
        self.pushButton_35.clicked.connect(self.Book_Export_Report)

        self.pushButton_17.clicked.connect(self.Edit_CLient_Search)
        self.pushButton_16.clicked.connect(self.Edit_CLient)
        self.pushButton_18.clicked.connect(self.Delete_Client)
        self.pushButton_37.clicked.connect(self.Client_Export_Report)


        self.pushButton_29.clicked.connect(self.Check_Employee)
        self.pushButton_28.clicked.connect(self.Edit_Employee_Data)
        self.pushButton_30.clicked.connect(self.Add_Employee_Permissions)

        self.pushButton_38.clicked.connect(self.User_Login_Permissions)

    def Handel_Login(self):
        ## Handel Login
        pass


    def Handel_Reset_Passwors(self):
        # Handel Reset Password
        pass


    def Handel_to_Day_Work(self):
        ## Handel Day to day operations
        book_title = self.lineEdit.text()
        client_nationl_id = self.lineEdit_51.text()
        type = self.comboBox.currentIndex()
        from_date = str(datetime.date.today())
        # to_date = self.dateEdit_6.date()
        to_date = str(datetime.date.today())
        date = datetime.datetime.now()
        branch = 1
        employee = 1



        self.cur.execute('''
            INSERT INTO daily_movements(book_id , client_id , type,date,branch_id,book_from , book_to , employee_id)
            VALUES(%s , %s , %s , %s , %s , %s , %s , %s)
        ''',(book_title,client_nationl_id,type,date,branch,from_date,to_date,employee))

        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 3
        table = 6
        data = 'day to day work'

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch,data))


        self.db.commit()
        self.Show_History()
        self.Retreive_Day_Work()


    def Retreive_Day_Work(self):

        self.cur.execute('''
            SELECT book_id ,type , client_id , book_from , book_to  FROM daily_movements
            ''')
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row , form in enumerate(data):
            for column , item in enumerate(form):
                if column == 1 :
                    if item == 0 :
                        self.tableWidget.setItem(row, column, QTableWidgetItem(str("Rent")))
                    else:
                        self.tableWidget.setItem(row , column , QTableWidgetItem(str("Retrieve")))

                elif column == 2 :
                    sql = ''' SELECT name FROM clients WHERE national_id = %s '''
                    self.cur.execute(sql , [(item)])
                    client_name = self.cur.fetchone()
                    # self.tableWidget.setItem(row, column, QTableWidgetItem(str(client_name[0])))

                else:
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

    ##########################################
    def Show_All_Books(self):
        ## show all books
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        self.cur.execute('''
            SELECT code , title , category_id , author_id , price FROM books
        ''')

        data = self.cur.fetchall()

        for row , form in enumerate(data):
            for col , item in enumerate(form):
                if col == 2 :
                    sql = (''' SELECT category_name FROM category WHERE id = %s ''')
                    self.cur.execute(sql , [(item)])
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row,col , QTableWidgetItem(str(category_name[0])))

                elif col == 3:
                    sql = (''' SELECT name FROM author WHERE id = %s ''')
                    self.cur.execute(sql , [(item+1)])
                    author_name = self.cur.fetchone()
                    print(author_name)
                    print(item)
                    self.tableWidget_2.setItem(row,col , QTableWidgetItem(str(author_name[0])))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)



    def All_Books_Filter(self):
        book_title = self.lineEdit_2.text()
        category = self.comboBox_2.currentIndex()

        sql = '''
            SELECT code , title , category_id , author_id , publisher_id FROM books WHERE title = %s 
        '''
        self.cur.execute(sql ,[(book_title)])
        data = self.cur.fetchall()

        print(data)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        for row , form in enumerate(data):
            for col , item in enumerate(form):
                if col == 2 :
                    sql = (''' SELECT category_name FROM category WHERE id = %s ''')
                    self.cur.execute(sql , [(item)])

                    category_name = self.cur.fetchone()
                    print(category_name)

                    self.tableWidget_2.setItem(row,col , QTableWidgetItem(str(item)))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)




    def Add_New_Book(self):
        ## add new book
        book_title = self.lineEdit_3.text()
        category = self.comboBox_3.currentIndex()
        description = self.textEdit.toPlainText()
        price = self.lineEdit_4.text()
        code = self.lineEdit_5.text()
        publisher = self.comboBox_4.currentIndex()
        author = self.comboBox_5.currentIndex()
        status = self.comboBox_5.currentIndex()
        part_order = self.lineEdit_6.text()
        barcode = self.lineEdit_50.text()
        date = datetime.datetime.now()


        self.cur.execute('''
            INSERT INTO books(title,description,category_id,code,barcode,part_order,price,author_id ,publisher_id,status,date)
            VALUES (%s , %s , %s , %s,%s , %s , %s , %s , %s , %s  , %s)
        ''',(book_title,description,category,code,barcode,part_order,price,author ,publisher,status , date))


        global employee_id , employee_branch
        action = 3
        table = 0

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch , data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''',(employee_id,action,table,date,employee_branch,book_title))



        self.db.commit()
        self.Show_All_Books()
        self.Show_History()


    def Edit_Book_search(self):
        ## edit book
        book_code = self.lineEdit_8.text()

        sql = ('''
            SELECT * FROM books WHERE code = %s
        ''')

        self.cur.execute(sql , [(book_code)])

        data = self.cur.fetchone()

        print(data)

        self.lineEdit_10.setText(data[1])
        self.comboBox_10.setCurrentIndex(int(data[10]))
        self.lineEdit_7.setText(str(data[6]))
        self.comboBox_8.setCurrentIndex(int(data[11]))
        self.comboBox_9.setCurrentIndex(int(data[12]))
        self.comboBox_7.setCurrentIndex(int(data[8]))
        self.lineEdit_9.setText(str(data[5]))
        self.textEdit_2.setPlainText(data[2])


    def Edit_Book(self):
        book_title = self.lineEdit_10.text()
        category = self.comboBox_10.currentIndex()
        description = self.textEdit_2.toPlainText()
        price = self.lineEdit_7.text()
        code = self.lineEdit_8.text()
        publisher = self.comboBox_8.currentIndex()
        author = self.comboBox_9.currentIndex()
        status = self.comboBox_7.currentIndex()
        part_order = self.lineEdit_9.text()
        date = datetime.datetime.now()

        self.cur.execute('''
            UPDATE books SET title=%s ,description=%s ,code = %s ,part_order = %s , price = %s , status = %s , category_id=%s,publisher_id=%s,author_id=%s WHERE code = %s   
        ''',(book_title,description,code,part_order,price,status,category,publisher,author,code))


        global employee_id , employee_branch
        action = 4
        table = 0


        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''',(employee_id,action,table,date,employee_branch,book_title))




        self.db.commit()
        self.Show_History()
        self.statusBar().showMessage('تم تعديل معلومات الكتاب بنجاح')
        # QMessageBox.information(self , "success" , "تم تعديل معلومات الكتاب بنجاح")

        self.Show_All_Books()


    def Delete_Book(self):
        ## delete book from DB
        book_code = self.lineEdit_8.text()
        date = datetime.datetime.now()

        delete_message = QMessageBox.warning(self ,"مسح معلومات" , "هل انت متاكد من مسح الكتاب",QMessageBox.Yes | QMessageBox.No )

        if delete_message == QMessageBox.Yes :

            sql = ('''
                DELETE FROM books WHERE code = %s
            ''' )

            global employee_id, employee_branch
            action = 5
            table = 1

            self.cur.execute('''
                INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch , data)
                VALUES (%s , %s , %s , %s , %s , %s)
            ''', (employee_id, action, table, date, employee_branch , book_code))


            self.cur.execute(sql , [(book_code)])
            self.db.commit()
            self.Show_History()
            self.statusBar().showMessage('تم مسح الكتاب بنجاح')
            self.Show_All_Books()


    ###########################################
    def Show_All_CLients(self):
        ## show all clients
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)

        self.cur.execute('''
            SELECT name , mail , phone , national_id , date FROM clients
        ''')

        data = self.cur.fetchall()

            ## row = iteration , form = data
        for row , form in enumerate(data):
            for col , item in enumerate(form):
                self.tableWidget_3.setItem(row,col , QTableWidgetItem(str(item)))
                col += 1

            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)




    def Add_New_Client(self):
        ## add new Client
        client_name = self.lineEdit_12.text()
        client_email = self.lineEdit_13.text()
        client_phone = self.lineEdit_14.text()
        client_national_id = self.lineEdit_15.text()
        date = datetime.datetime.now()

        self.cur.execute('''
            INSERT INTO clients(name,mail,phone,national_id,date)
            VALUES (%s , %s , %s ,%s , %s)
        ''' , (client_name , client_email , client_phone , client_national_id , date))

        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 3
        table = 2

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data )
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch , client_name))

        self.db.commit()
        self.Show_All_CLients()
        self.Show_History()
        self.statusBar().showMessage('تم اضافه العميل بنجاح')
        print('done')



    def Edit_CLient_Search(self):
        ## edit client
        client_data = self.lineEdit_20.text()

        if self.comboBox_11.currentIndex() == 0 :
            sql = ('''SELECT * FROM clients WHERE name = %s''')
            self.cur.execute(sql , [(client_data)])
            data = self.cur.fetchone()
            print(data)

        if self.comboBox_11.currentIndex() == 1 :
            sql = ('''SELECT * FROM clients WHERE mail = %s''')
            self.cur.execute(sql , [(client_data)])
            data = self.cur.fetchone()
            print(data)


        if self.comboBox_11.currentIndex() == 2 :
            sql = ('''SELECT * FROM clients WHERE phone = %s''')
            self.cur.execute(sql , [(client_data)])
            data = self.cur.fetchone()
            print(data)


        if self.comboBox_11.currentIndex() == 3 :
            sql = ('''SELECT * FROM clients WHERE national_id = %s''')
            self.cur.execute(sql , [(client_data)])
            data = self.cur.fetchone()
            print(data)


        self.lineEdit_18.setText(data[1])
        self.lineEdit_17.setText(data[2])
        self.lineEdit_16.setText(data[3])
        self.lineEdit_19.setText(str(data[5]))



    def Edit_CLient(self):
        ## edit client
        client_name = self.lineEdit_18.text()
        client_mail = self.lineEdit_17.text()
        client_phone = self.lineEdit_16.text()
        client_national_id = self.lineEdit_19.text()


        self.cur.execute('''
            UPDATE clients SET name = %s , mail = %s , phone = %s , national_id = %s
        ''' , (client_name,client_mail,client_phone,client_national_id))


        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 4
        table = 2

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch , data )
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch , client_name))


        self.db.commit()
        self.Show_History()
        self.statusBar().showMessage('تم تعديل معلومات العميل بنجاح')
        self.Show_All_CLients()


    def Delete_Client(self):
        ## delete client from DB
        client_data = self.lineEdit_20.text()
        delete_message = QMessageBox.warning(self ,"مسح معلومات" , "هل انت متاكد من مسح العميل",QMessageBox.Yes | QMessageBox.No )

        if delete_message == QMessageBox.Yes :

            if self.comboBox_11.currentIndex() == 0 :
                sql = ('''DELETE FROM clients WHERE name = %s''')
                self.cur.execute(sql , [(client_data)])


            if self.comboBox_11.currentIndex() == 1 :
                sql = ('''DELETE FROM clients WHERE mail = %s''')
                self.cur.execute(sql , [(client_data)])


            if self.comboBox_11.currentIndex() == 2 :
                sql = ('''DELETE FROM clients WHERE phone = %s''')
                self.cur.execute(sql , [(client_data)])


            if self.comboBox_11.currentIndex() == 3 :
                sql = ('''DELETE FROM clients WHERE national_id = %s''')
                self.cur.execute(sql , [(client_data)])


            global employee_id, employee_branch
            action = 5
            table = 2
            date = datetime.datetime.now()

            self.cur.execute('''
                INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
                VALUES (%s , %s , %s , %s , %s , %s)
            ''', (employee_id, action, table, date, employee_branch,client_data))


            self.db.commit()
            self.Show_History()
            self.statusBar().showMessage('تم مسح العميل بنجاح')
            self.Show_All_CLients()


    ###########################################
    ## history

    def Show_History(self):
        ## show all history to the admin
        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)

        self.cur.execute('''
            SELECT employee_id , employee_branch , employee_action , affected_table , operation_date , data FROM history
        ''')

        data = self.cur.fetchall()

            ## row = iteration , form = data
        for row , form in enumerate(data):
            for col , item in enumerate(form):

                if col == 0 :
                    sql = (''' SELECT name FROM employee WHERE id = %s ''')
                    self.cur.execute(sql , [(item)])
                    employee_name = self.cur.fetchone()
                    self.tableWidget_4.setItem(row,col , QTableWidgetItem(str(employee_name[0])))

                elif col == 1 :
                    sql = (''' SELECT name FROM branch WHERE id = %s ''')
                    self.cur.execute(sql , [(item)])
                    branch_name = self.cur.fetchone()

                    self.tableWidget_4.setItem(row,col , QTableWidgetItem(str(branch_name)))



                elif col == 2 :
                    action = ' '
                    if item == 1 :
                        action = 'Login'

                    if item == 2 :
                        action = 'Logout'

                    if item == 3 :
                        action = 'Add'

                    if item == 4 :
                        action = 'Edit'

                    if item == 5 :
                        action = 'Delet'

                    if item == 6 :
                        action = 'Search'

                    self.tableWidget_4.setItem(row,col , QTableWidgetItem(str(action)))



                elif col == 3 :
                    table = ' '
                    if item == 1 :
                        table = 'Books'

                    if item == 2 :
                        table = 'Clients'

                    if item == 3 :
                        table = 'History'

                    if item == 4 :
                        table = 'Branch'

                    if item == 5 :
                        table = 'Category'

                    if item == 6 :
                        table = 'Daily Movements'


                    if item == 7 :
                        table = 'Employee'

                    if item == 8 :
                        table = 'Publisher'

                    if item == 8 :
                        table = 'Author'

                    self.tableWidget_4.setItem(row,col , QTableWidgetItem(str(table)))
                else:
                    self.tableWidget_4.setItem(row,col , QTableWidgetItem(str(item)))



                col += 1

            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)

    ###########################################
    ### books report

    def All_Books_Report(self):
        ## report for all books
        pass

    def Books_Filter_Report(self):
        ## Show report for filtered books
        pass


    def Book_Export_Report(self):
        ## export books data to excel file
        self.cur.execute('''
            SELECT code , title , category_id , author_id , price FROM books
        ''')

        data = self.cur.fetchall()
        excel_file = Workbook('books_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0,0,'Book Code')
        sheet1.write(0,1,'Book Title')
        sheet1.write(0,2,'Category')
        sheet1.write(0,3,'Author')
        sheet1.write(0,4,'Price')


        row_number = 1
        for row in data :
            column_number = 0
            for item in row :
                sheet1.write(row_number,column_number,str(item))
                column_number += 1
            row_number += 1

        excel_file.close()
        self.statusBar().showMessage('تم انشاء التقرير بنجاح')

    ###########################################
    ###########################################
    def All_Client_Report(self):
        ## report for all clients
        pass

    def Clients_Filter_Report(self):
        ## Show report for filtered clients
        pass


    def Client_Export_Report(self):
        ## export client data to excel file
        self.cur.execute('''
            SELECT name , mail , phone , national_id  FROM clients
        ''')

        data = self.cur.fetchall()
        excel_file = Workbook('CLients_report.xlsx')
        sheet1 = excel_file.add_worksheet()

        sheet1.write(0, 0, 'CLient Name')
        sheet1.write(0, 1, 'CLient mail')
        sheet1.write(0, 2, 'CLient Phone')
        sheet1.write(0, 3, 'CLient National Id')

        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        excel_file.close()
        self.statusBar().showMessage('تم انشاء التقرير بنجاح')

    ###########################################
    ###########################################
    def Monthly_Report(self):
        ## show one month report
        pass


    def Monthly_Report_Export(self):
        ## export monthly report to excel file
        pass

    ###########################################
    ###########################################
    ##### settings

    def Add_Branch(self):
        ## add new branch
        branch_name = self.lineEdit_21.text()
        branch_code = self.lineEdit_22.text()
        branch_location = self.lineEdit_23.text()

        self.cur.execute(''' 
            INSERT INTO branch(name , code , location)
            VALUES (%s , %s , %s)
            ''', (branch_name , branch_code,branch_location))


        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 3
        table = 4

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch , data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch,branch_name))

        self.db.commit()
        self.Show_History()
        print('Branch Added')




    def Add_Category(self):
        ## add new category
        category_name = self.lineEdit_28.text()
        parent_category_Text = self.comboBox_13.currentText()


        self.cur.execute('''
            INSERT INTO category(category_name , parent_category)
            VALUES (%s , %s)
        ''' , (category_name,parent_category_Text))



        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 3
        table = 5

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch,category_name))

        self.db.commit()
        print('Category Added')
        self.Show_History()

        self.Show_All_Categories()


    def Add_Publisher(self):
        ## add new publisher
        publisher_name = self.lineEdit_24.text()
        publisher_location = self.lineEdit_25.text()

        self.cur.execute('''
                INSERT INTO publisher(name , location)
                VALUES (%s , %s)
            ''' , (publisher_name , publisher_location))

        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 3
        table = 8

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch , publisher_name))


        self.db.commit()
        print('publisher Added')




    def Add_Author(self):
        ## add new author
        author_name = self.lineEdit_27.text()
        author_location = self.lineEdit_26.text()

        self.cur.execute(''' 
                INSERT INTO author(name , location)
                VALUES (%s , %s)
            ''' , (author_name , author_location))

        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 3
        table = 9

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch,author_name))

        self.db.commit()
        self.Show_History()

        print('Author Added')


    ###########################################################
    ############################################################

    def Show_All_Categories(self):
        self.comboBox_13.clear()
        self.cur.execute('''
            SELECT category_name FROM category
        ''')

        categories = self.cur.fetchall()

        for category in categories :
            self.comboBox_13.addItem(str(category[0]))
            self.comboBox_3.addItem(str(category[0]))
            self.comboBox_10.addItem(str(category[0]))
            self.comboBox_2.addItem(str(category[0]))



    def Show_Branchies(self):

        self.cur.execute(''' 
            SELECT name FROM branch
        ''')

        branchies = self.cur.fetchall()

        for branch in branchies:
            self.comboBox_21.addItem(branch[0])
            self.comboBox_22.addItem(branch[0])


    def Show_Publishers(self):
        self.cur.execute('''
            SELECT name FROM publisher
        ''')

        publishers = self.cur.fetchall()
        for publisher in publishers:
            print(publisher[0])
            self.comboBox_4.addItem(publisher[0])
            self.comboBox_8.addItem(publisher[0])


    def Show_Authors(self):
        self.cur.execute(''' 
            SELECT name FROM author
        ''')

        authors = self.cur.fetchall()
        for author in authors :
            self.comboBox_5.addItem(author[0])
            self.comboBox_9.addItem(author[0])



    def Show_Employee(self):
        self.cur.execute('''
            SELECT name FROM employee
        ''')
        employees = self.cur.fetchall()
        for employee in employees :
            self.comboBox_19.addItem(employee[0])
            self.comboBox_23.addItem(employee[0])

    ###########################################
    ###########################################

    def Add_Employee(self):
        ## add new employee
        employee_name = self.lineEdit_33.text()
        employee_email = self.lineEdit_34.text()
        employee_phone = self.lineEdit_35.text()
        employee_branch_ = self.comboBox_21.currentIndex()
        national_id = self.lineEdit_32.text()
        periority = self.lineEdit_44.text()
        password = self.lineEdit_36.text()
        password2 = self.lineEdit_37.text()
        global employee_id, employee_branch
        action = 3
        table = 7
        date = datetime.datetime.now()

        if password == password2 :

            self.cur.execute('''
                INSERT INTO employee (name , mail , phone , branch , national_id ,date, periority , password)
                VALUES (%s , %s , %s , %s , %s , %s , %s , %s)
            ''' , (employee_name,employee_email,employee_phone,employee_branch_,national_id,date,periority , password))



            self.cur.execute('''
                INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
                VALUES (%s , %s , %s , %s , %s , %s)
            ''', (employee_id, action, table, date, employee_branch,employee_email))

            self.db.commit()
            self.Show_History()

            self.lineEdit_33.setText('')
            self.lineEdit_34.setText('')
            self.lineEdit_35.setText('')
            self.lineEdit_32.setText('')
            self.lineEdit_44.setText('')
            self.lineEdit_36.setText('')
            self.lineEdit_37.setText('')
            self.statusBar().showMessage('تم اضافه الموظف بنجاح')


        else:
            print('wrong password')


    def Check_Employee(self):
        employee_name = self.lineEdit_39.text()
        employee_password = self.lineEdit_43.text()

        self.cur.execute(""" SELECT * FROM employee""")
        data = self.cur.fetchall()

        print(data)

        for row in data :
            if row[1] == employee_name and row[7] == employee_password :

                print(type(row[5]))

                self.groupBox_9.setEnabled(True)
                self.lineEdit_40.setText(row[2])
                self.lineEdit_41.setText(row[3])
                self.comboBox_22.setCurrentIndex(row[8])
                self.lineEdit_38.setText(str(row[5]))
                self.lineEdit_45.setText(str(row[6]))
                self.lineEdit_42.setText(str(row[7]))



    def Edit_Employee_Data(self):
        ## edit employee data
        employee_name = self.lineEdit_39.text()
        employee_password = self.lineEdit_43.text()
        employee_email = self.lineEdit_40.text()
        employee_phone = self.lineEdit_41.text()
        employee_branch_ = self.comboBox_22.currentIndex()
        employee_national_id = self.lineEdit_38.text()
        employee_periority = self.lineEdit_45.text()
        employee_password2 = self.lineEdit_42.text()

        date = datetime.datetime.now()

        if employee_password == employee_password2 :
            self.cur.execute('''
                UPDATE employee SET mail=%s,phone=%s,national_id=%s,Periority=%s,password=%s,branch=%s WHERE name=%s
            ''',(employee_email,employee_phone,employee_national_id,employee_periority,employee_password2,employee_branch_,employee_name))



        global employee_id, employee_branch
        date = datetime.datetime.now()
        action = 4
        table = 7

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch,data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch,employee_email))


        self.db.commit()
        self.Show_History()
        self.lineEdit_39.setText('')
        self.lineEdit_43.setText('')
        self.lineEdit_40.setText('')
        self.lineEdit_41.setText('')
        self.lineEdit_38.setText('')
        self.lineEdit_38.setText('')
        self.lineEdit_45.setText('')
        self.lineEdit_42.setText('')
        self.comboBox_22.setCurrentIndex(0)
        self.groupBox_9.setEnabled(False)
        self.statusBar().showMessage('تم تعديل معلومات الموظف بنجاح')


    ###########################################
    ###########################################

    def Add_Employee_Permissions(self):
        ## add permission to any employee

        employee_name = self.comboBox_19.currentText()


        if self.checkBox_23.isChecked() == True :

            self.cur.execute('''
                INSERT INTO employee_permissions (employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab ,
                                                   add_book,edit_book,delete_book,import_book,export_book  ,
                                                   add_client,edit_client,delete_client,import_client,export_client ,
                                                   add_branch,add_publisher,add_author,add_category,add_employee,edit_employee , is_admin)

                VALUES(%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s, %s , %s , %s , %s , %s, %s , %s , %s , %s , %s , %s , %s)
            ''', (employee_name, 1, 1, 1, 1, 1, 1 , 1, 1, 1, 1, 1,1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1 , 1))

            self.db.commit()
            print('permission added')
            self.statusBar().showMessage('تم اضافه كل الصلاحيات للموظف بنجاح')


        else:


            books_tab = 0
            clients_tab = 0
            dashboard_tab = 0
            history_tab = 0
            reports_tab = 0
            settings_tab = 0

            add_book = 0
            edit_book = 0
            delete_book = 0
            import_book = 0
            export_book = 0

            add_client = 0
            edit_client = 0
            delete_client = 0
            import_client = 0
            export_client = 0


            add_branch = 0
            add_publisher = 0
            add_author= 0
            add_category = 0
            add_employee = 0
            edit_employee = 0


                ### tabs
            if self.checkBox_7.isChecked() == True :
                books_tab = 1

            if self.checkBox_9.isChecked() == True :
                clients_tab = 1

            if self.checkBox_11.isChecked() == True :
                dashboard_tab = 1

            if self.checkBox_12.isChecked() == True :
                history_tab = 1

            if self.checkBox_13.isChecked() == True :
                reports_tab = 1

            if self.checkBox_14.isChecked() == True :
                settings_tab = 1


                ### books
            if self.checkBox.isChecked() == True :
                add_book = 1

            if self.checkBox_2.isChecked() == True :
                edit_book = 1

            if self.checkBox_4.isChecked() == True :
                delete_book = 1

            if self.checkBox_8.isChecked() == True :
                import_book = 1

            if self.checkBox_10.isChecked() == True :
                export_book = 1


                ### clients
            if self.checkBox_3.isChecked() == True :
                add_client = 1

            if self.checkBox_6.isChecked() == True :
                edit_client = 1

            if self.checkBox_5.isChecked() == True :
                delete_client = 1

            if self.checkBox_15.isChecked() == True :
                import_client = 1

            if self.checkBox_16.isChecked() == True :
                export_client = 1



                ### settings
            if self.checkBox_17.isChecked() == True :
                add_branch = 1

            if self.checkBox_18.isChecked() == True :
                add_publisher = 1

            if self.checkBox_19.isChecked() == True :
                add_author = 1

            if self.checkBox_20.isChecked() == True :
                add_category = 1

            if self.checkBox_21.isChecked() == True :
                add_employee = 1

            if self.checkBox_22.isChecked() == True :
                edit_employee = 1




            self.cur.execute('''
                INSERT INTO employee_permissions (employee_name,books_tab,clients_tab,dashboard_tab,history_tab,reports_tab,settings_tab ,
                                                   add_book,edit_book,delete_book,import_book,export_book  ,
                                                   add_client,edit_client,delete_client,import_client,export_client ,
                                                   add_branch,add_publisher,add_author,add_category,add_employee,edit_employee)
                                                   
                VALUES(%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s, %s , %s , %s , %s , %s, %s , %s , %s , %s , %s , %s)
            ''' , ( employee_name, books_tab ,clients_tab ,  dashboard_tab , history_tab ,reports_tab , settings_tab
                    , add_book , edit_book , delete_book , import_book , export_book ,
                    add_client , edit_client , delete_client , import_client , export_client ,
                    add_branch , add_publisher , add_author , add_category , add_employee , edit_employee))

            self.db.commit()
            print('permission added')
            self.statusBar().showMessage('تم اضافه الصلاحيات للموظف بنجاح')




    def Admin_Report(self):
        ## send report to the admin
        pass



    #########################################
    #########################################

    def Open_Login_Tab(self):
        self.tabWidget.setCurrentIndex(0)
        print('Login Tap')


    def Open_Reset_Password_Tab(self):
        self.tabWidget.setCurrentIndex(1)
        print('Reset Password Tap')


    def Open_Daily_movements_Tab(self):
        self.tabWidget.setCurrentIndex(2)
        print('Daily Movements Tap')


    def Open_Books_Tap(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(0)
        print('Books Tap')

    def Open_CLients_Tap(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)
        print('CLients Tap')

    def Open_Dashboard_Tap(self):
        self.tabWidget.setCurrentIndex(5)
        print('Dashboard Tap')

    def Open_History_Tap(self):
        self.tabWidget.setCurrentIndex(6)
        print('History Tap')


    def Open_Report_Tap(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)
        print('Report Tap')

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(8)
        print('Settings Tap')        




    ############################################
        ####### User Login

    def User_Login_Permissions(self):
        username = self.lineEdit_47.text()
        password = self.lineEdit_48.text()


        self.cur.execute(""" SELECT id , name , password , branch FROM employee""")
        data_ = self.cur.fetchall()

        for row in data_ :
            if row[1] == username and row[2] == password :
                global employee_id , employee_branch
                employee_id = row[0]
                employee_branch = row[3]


                ## load user permissions
                self.groupBox_14.setEnabled(True)
                self.cur.execute('''
                    SELECT * FROM employee_permissions WHERE employee_name = %s
                ''',(username,))

                user_permissions = self.cur.fetchone()

                self.pushButton.setEnabled(True)

                if user_permissions[2] == 1 :
                    self.pushButton_2.setEnabled(True)

                if user_permissions[3] == 1 :
                    self.pushButton_3.setEnabled(True)

                if user_permissions[4] == 1 :
                    self.pushButton_4.setEnabled(True)

                if user_permissions[4] == 1 :
                    self.pushButton_7.setEnabled(True)

                if user_permissions[5] == 1 :
                    self.pushButton_7.setEnabled(True)

                if user_permissions[6] == 1 :
                    self.pushButton_6.setEnabled(True)

                if user_permissions[7] == 1 :
                    self.pushButton_5.setEnabled(True)

                if user_permissions[8] == 1 :
                    self.pushButton_10.setEnabled(True)

                if user_permissions[9] == 1 :
                    self.pushButton_11.setEnabled(True)

                if user_permissions[10] == 1 :
                    self.pushButton_13.setEnabled(True)

                if user_permissions[11] == 1:
                    self.pushButton_34.setEnabled(True)

                if user_permissions[12] == 1:
                    self.pushButton_35.setEnabled(True)

                if user_permissions[13] == 1:
                    self.pushButton_15.setEnabled(True)

                if user_permissions[14] == 1 :
                    self.pushButton_16.setEnabled(True)

                if user_permissions[15] == 1 :
                    self.pushButton_18.setEnabled(True)

                if user_permissions[16] == 1 :
                    self.pushButton_36.setEnabled(True)

                if user_permissions[17] == 1 :
                    self.pushButton_37.setEnabled(True)

                if user_permissions[18] == 1:
                    self.pushButton_34.setEnabled(True)

                if user_permissions[19] == 1:
                    self.pushButton_19.setEnabled(True)

                if user_permissions[20] == 1:
                    self.pushButton_20.setEnabled(True)

                if user_permissions[21] == 1:
                    self.pushButton_21.setEnabled(True)


                if user_permissions[22] == 1:
                    self.pushButton_22.setEnabled(True)

                if user_permissions[23] == 1:
                    self.pushButton_27.setEnabled(True)

                if user_permissions[24] == 1:
                    self.pushButton_28.setEnabled(True)


        date = datetime.datetime.now()
        action = 1
        table = 7

        self.cur.execute('''
            INSERT INTO history(employee_id , employee_action , affected_table , operation_date , employee_branch , data)
            VALUES (%s , %s , %s , %s , %s , %s)
        ''', (employee_id, action, table, date, employee_branch , username))
        self.db.commit()
        self.Show_History()




    ########### dashboard
    def get_dashboard_data(self):
        data1 = [1,2,3,4,5,6,7,8,9] 
        data2 = [1,2,3,4,5,6,7,8,9] 




        ## retrieve data
        self.cur.execute(""" 
            SELECT COUNT(book_id), EXTRACT(MONTH FROM Book_from) as month
            FROM daily_movements
            GROUP BY month
        """)
        pen = pg.mkPen(color=(255,0,0))
        data = self.cur.fetchall()
        books_count = []
        rent_count = []
        for row in data:
                books_count.append(row[0])
                rent_count.append(row[1])
                
        self.widget.plot(books_count , rent_count , pen=pen , symbol='+' , symbolSize=20,symbolBrush=('w'))
        # self.widget.setBackground('w')
        self.widget.setTitle('المبيعات') # size , color 
        self.widget.addLegend()
        self.widget.setLabel('left' ,' left side' , color='red' , size=40 )
        self.widget.setLabel('bottom' ,' bottom side' , color='red' , size=40 )
        self.widget.showGrid(x=True,y=True)


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
import sys
import mysql.connector
from PyQt5.uic import loadUiType
MainUI,_ = loadUiType('main.ui')
class Main(QMainWindow , MainUI):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.db_connect()
        self.Mandel_Buttons()
        self.open_daily_move_tab()
        self.show_all_categ()
        self.show_publisher()
        self.show_author()
        self.Show_All_Book()
        self.ui_change()
    def db_connect(self):
        self.db = mysql.connector.connect(host='localhost', user='root', password='toor',
                         database='lb')
        self.cur = self.db.cursor()
        print('connexion accepted')
    def ui_change(self):
        self.tabWidget.tabBar().setVisible(False)
    ###user
    def user_login(self):
        usern = self.tb3.text()
        passw = self.tb4.text()
        self.cur.execute(""" SELECT name , password from employe""")
        data = self.cur.fetchall()
        print(data)
        for row in data :
            if row[0] == usern and row[1] == passw :
               #self.groupBox_5.setEnabled(True)
               print(row)
               self.cur.execute('''
                   SELECT * FROM employe_perm WHERE name_emp_perm = %s
               ''',(usern,))
               usrp = self.cur.fetchone()
               print(usrp)

    def handel_login(self):
        pass
    def handel_reset_password(self):
        pass
    def Mandel_Buttons(self):
        #handle all buttons in our app
        #self.pushButton.clicked.connect(self.open_daily_move_tab)
        self.pushButton_3.clicked.connect(self.open_daily_book_tab)
        self.pushButton_2.clicked.connect(self.open_daily_setting_tab)
        #self.pushButton_8.clicked.connect(self.Mandel_to_Day_Work)
        self.pushButton_28.clicked.connect(self.Add_branch)
        self.pushButton_27.clicked.connect(self.add_publisher)
        self.pushButton_26.clicked.connect(self.add_auth)
        self.pushButton_25.clicked.connect(self.add_category)
        self.pushButton_10.clicked.connect(self.add_book)
        self.pushButton_13.clicked.connect(self.Edit_Book_search)
        #self.pushButton_14.clicked.connect(self.Edit_book_save)
        self.pushButton_15.clicked.connect(self.Delete_Book)
        self.pushButton_9.clicked.connect(self.book_filter)
        self.pushButton_12.clicked.connect(self.user_login)
        self.pushButton_47.clicked.connect(self.add_employe)
    def add_employe(self):
        emn = self.lineEdit_58.text()
        eme =  self.lineEdit_59.text()
        emb = self.lineEdit_60.text()
        emp = self.lineEdit_61.text()
        empass = self.lineEdit_62.text()
        empassp = self.lineEdit_63.text()
        if empass == empassp :
            self.cur.execute('''
            INSERT INTO employe (name , mail , branch , Periority , password )
            VALUES (%s , %s , %s , %s , %s)
            ''', (emn,eme,emb,emp , empass))
            self.db.commit()
        else:
            print('wrong pass')
    def add_book(self):
        book_title = self.lineEdit_3.text()
        book_cat = self.comboBox_3.currentIndex()
        book_des = self.textEdit.toPlainText()
        book_cod = self.lineEdit_5.text()
        price = self.lineEdit_4.text()
        book_pub = self.comboBox_6.currentIndex()

        book_aut = self.comboBox_4.currentIndex()

        book_pa = self.lineEdit_6.text()
        status = self.comboBox_4.currentIndex()
        bc = self.lineEdit_10.text()
        date = datetime.datetime.now()

        self.cur.execute('''
             INSERT INTO books(title , description , category_id , code , barcode , part_order , price ,  author_id , publisher_id , status , date)
             VALUES (%s , %s , %s , %s , %s , %s , %s , %s , %s , %s , %s)
        ''',(book_title , book_des , book_cat , book_cod , bc , book_pa , price , book_aut , book_pub , status , date)
        )
        self.db.commit()
        self.Show_All_Book()
        print('good book')
    def Mandel_to_Day_Work(self):
        #handle day to day operation
       pass
    def Add_branch(self):
        b_n = self.lineEdit_31.text()
        b_c = self.lineEdit_30.text()
        b_l = self.lineEdit_29.text()
        self.cur.execute('''
             INSERT INTO branch(name , code , Location) 
             VALUES(%s , %s , %s)
             ''', (b_n , b_c , b_l ))
        self.db.commit()
        print('bra good')
    def add_publisher(self):
        p_n= self.lineEdit_7.text()
        p_l=self.lineEdit_9.text()
        self.cur.execute('''
                     INSERT INTO publisher(name , Location) 
                     VALUES(%s , %s)
                     ''', (p_n, p_l))
        self.db.commit()
        print('push good')
    def add_auth(self):
        c_n = self.lineEdit_25.text()
        c_l = self.lineEdit_11.text()
        self.cur.execute('''
                             INSERT INTO author(name , Location) 
                             VALUES(%s , %s)
                             ''', (c_n, c_l))
        self.db.commit()
        print('auth good')
    def add_category(self):
        category_name = self.lineEdit_28.text()
        parent_cat_txt = self.comboBox_17.currentText()
        query = '''SELECT id FROM category WHERE category_name = %s'''
        self.cur.execute(query, [(parent_cat_txt)])
        data = self.cur.fetchone()
        parent_category = data[0]
        self.cur.execute('''
                                     INSERT INTO category(category_name , parent_category) 
                                     VALUES(%s , %s)
                                     ''', (category_name,parent_category))
        self.db.commit()
        print('cat good')
        self.show_all_categ()

    def show_all_categ(self):
        #supp les doublons
        self.comboBox_17.clear()
        self.cur.execute('''
                         SELECT category_name FROM category
        ''')
        categories = self.cur.fetchall()
        for cat in categories:

            #relver de la base de donne et inserer dans notre button
            self.comboBox_17.addItem(str(cat[0]))
            self.comboBox_3.addItem(str(cat[0]))
            self.comboBox_14.addItem(str(cat[0]))
            #self.comboBox_16.addItem(str(cat[0]))


    def Show_All_Book(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        self.cur.execute('''
            SELECT code , title , category_id , author_id , price FROM books 
        ''')
        data = self.cur.fetchall()

        for row , form in enumerate(data):
            for col , item in enumerate(form):

                self.tableWidget_2.setItem(row,col ,QTableWidgetItem(str(item)))
                col += 1
            #index coulom
            row_pos = self.tableWidget_2.rowCount()
            #ajouter dans mon tbl
            self.tableWidget_2.insertRow(row_pos)
    def book_filter(self):
        t = self.lineEdit_24.text()
        # c = self.comboBox_16.currentIndex()
        sql = '''
                   SELECT code , title , category_id , author_id , price FROM books WHERE title = %s 
        '''
        self.cur.execute(sql ,[t])
        data = self.cur.fetchall()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)
        for row, form in enumerate(data):
            for col, item in enumerate(form):
                if col == 2:
                    sql = (''' SELECT category_name FROM category WHERE id = %s ''')
                    self.cur.execute(sql, [(item)])
                    category_name = self.cur.fetchone()
                    print(category_name)
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                else:
                    self.tableWidget_2.setItem(row, col, QTableWidgetItem(str(item)))
                col += 1
            # index coulom
            row_pos = self.tableWidget_2.rowCount()
            # ajouter dans mon tbl
            self.tableWidget_2.insertRow(row_pos)
    def Edit_Book_search(self):
        book_code = self.lineEdit_12.text()
        sql = ('''
        SELECT * FROM books WHERE code = %s
        ''')

        self.cur.execute(sql , [(book_code)])
        data = self.cur.fetchone()
        self.lineEdit_15.setText(data[1])
        self.comboBox_14.setCurrentIndex(int(data[10]))
        self.lineEdit_14.setText(str(data[6]))
        self.comboBox_13.setCurrentIndex(int(data[11]))
        self.comboBox_15.setCurrentIndex(int(data[12]))
        self.comboBox_12.setCurrentIndex(int(data[8]))
        self.lineEdit_13.setText(str(data[5]))
        self.textEdit_3.setPlainText(data[2])

    '''def Edit_book(self):
        book_title = self.lineEdit_15.text()
        category = self.comboBox_14.currentIndex()
        description = self.textEdit_3.toPlainText()
        code = self.lineEdit_12.text()
        price = self.lineEdit_14.text()
        publisher = self.comboBox_13.currentIndex()
        author = self.comboBox_15.currentIndex()
        part_order = self.lineEdit_13.text()
        status = self.comboBox_12.currentIndex()'''
        #self.cur.execute('''
         #    UPDATE books SET title = %s , description = %s , code = %s , part_order = %s , price = %s , status = %s , category_id = %s , publisher_id = %s , author_id = %s WHERE code = %s
        #''',(book_title , description , code , part_order , price , status , category , publisher , author, code ))

        #self.db.commit()
        #print('done book')
    def Delete_Book(self):
        c = self.lineEdit_12.text()

        sql = ('''
                DELETE FROM books WHERE code = %s            
            ''')
        self.cur.execute(sql , [(c)])
        self.db.commit()
        QMessageBox.about(self, "" , "DELETE SUCCES")
        #self.statusBar().showMessage("supp avec succes")
        self.Show_All_Book()
    def show_publisher(self):
        self.cur.execute('''
        SELECT name FROM publisher
        ''')
        publishers = self.cur.fetchall()
        for publisher in publishers:
            self.comboBox_6.addItem(publisher[0])
            self.comboBox_13.addItem(publisher[0])
    def show_author(self):
        self.cur.execute('''
                SELECT name FROM author
                ''')
        authors = self.cur.fetchall()
        for author in authors:
            self.comboBox_4.addItem(author[0])
            self.comboBox_15.addItem(author[0])
    def open_daily_move_tab(self):
        self.tabWidget.setCurrentIndex(1)
    def open_daily_book_tab(self):
        #self.tabWidget.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(3)

    def open_daily_setting_tab(self):
        self.tabWidget.setCurrentIndex(6)
    def open_login_tab(self):
        self.tabWidget.setCurrentIndex(4)

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
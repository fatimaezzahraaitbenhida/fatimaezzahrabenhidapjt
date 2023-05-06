from peewee import *
db = MySQLDatabase('my_app', user='root', password='toor',
                         host='localhost', port=3306)
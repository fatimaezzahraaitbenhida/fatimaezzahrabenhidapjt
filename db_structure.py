from peewee import *
import datetime
db = MySQLDatabase('lb', user='root', password='toor',
                         host='localhost', port=3306)
class Category(Model):
      category_name = CharField(unique=True)
      parent_category = IntegerField(null=True)
      class Meta:
           database = db
class Publisher(Model):
     name = CharField(unique=True)
     Location = CharField(null=True)

     class Meta:
         database = db


class branch(Model):
    name = CharField(unique=True)
    code = CharField(null=True , unique=True)
    Location = CharField(null=True)

    class Meta:
        database = db
class Author(Model):
     name = CharField(unique=True)
     Location = CharField(null=True)

     class Meta:
         database = db
type = (
         (1,'rent'),
         (2,'receive')
     )
class daily_movement(Model):
        type = CharField(choices=type)

        class Meta:
            database = db
book_statu = (
    (1,'New'),
    (2,'Used'),
    (3,'Damaged')
)
class Books(Model):
    title = CharField(unique=True)#on accepte le non saisi
    description = TextField(null=True)
    category = ForeignKeyField(Category , backref='category' , null=True)
    code = CharField(null=True)
    barcode = CharField()
    part_order = IntegerField(null=True)
    price = DecimalField(null=True)
    publisher = ForeignKeyField(Publisher , backref='publisher' , null=True)
    author = ForeignKeyField(Author ,  backref='author' , null=True)
    image = CharField(null=True)
    status = CharField(choices=book_statu)
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
class employe(Model):
    name = CharField()
    mail = CharField(null = True)
    periority = IntegerField(null = True)

    class Meta:
        database = db
class employe_perm(Model):
    name_emp_perm = CharField()


    class Meta:
        database = db
db.connect()
db.create_tables([Category,Publisher,Author,daily_movement,Books,branch,employe,employe_perm])
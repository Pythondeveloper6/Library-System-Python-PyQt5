from peewee import *
import datetime

db = MySQLDatabase('lb', user='root', password='toor',
                         host='localhost', port=3306)




class Publisher(Model):
        name = CharField(unique=True)
        Location = CharField(null=True)

        class Meta:
            database = db 


class Author(Model):
        name = CharField(unique=True)
        Location = CharField(null=True)

        class Meta:
            database = db 



class Category(Model):
        category_name = CharField(unique=True)
        parent_category = IntegerField(null=True)  ## Recursive relationship

        class Meta:
            database = db 


class Branch(Model):
        name = CharField()
        code = CharField(null=True , unique=True)
        location = CharField(null=True)

        class Meta:
            database = db 




BOOK_STATUS = (
        (1,'New'),
        (2,'Used'),
        (3,'Damaged')
    )


class Books(Model):
        title = CharField(unique=True)
        description = TextField(null=True)
        category = ForeignKeyField(Category , backref='category' , null=True)
        code = CharField(null=True)
        barcode = CharField()
        # parts *
        part_order  = IntegerField(null=True)
        price = DecimalField(null=True)
        publisher = ForeignKeyField(Publisher , backref='publisher' , null=True)
        author = ForeignKeyField(Author , backref='author' , null=True)
        image  = CharField(null=True)
        status = CharField(choices=BOOK_STATUS) # Choices
        date = DateTimeField(default=datetime.datetime.now)

        class Meta:
            database = db 



class Clients(Model):
        name = CharField()
        mail = CharField(null=True , unique=True)
        phone = CharField(null=True)
        date = DateTimeField(default=datetime.datetime.now)
        national_id = IntegerField(null=True , unique=True)

        class Meta:
            database = db 



class Employee(Model):
        name = CharField()
        mail = CharField(null=True , unique=True)
        phone = CharField(null=True)
        date = DateTimeField(default=datetime.datetime.now)
        national_id = IntegerField(null=True , unique=True)
        Periority = IntegerField(null=True)

        class Meta:
            database = db 



PROCESS_TYPE = (
        (1,'Rent'),
        (2,'Retrieve')
    )

class Daily_Movements(Model):
        book = ForeignKeyField(Books , backref='daily_book')
        client = ForeignKeyField(Clients , backref='book_client')
        type   = CharField(choices=PROCESS_TYPE)      #[rent - retrieve]
        date = DateTimeField(default=datetime.datetime.now)
        branch = ForeignKeyField(Branch , backref='Daily_branch' , null=True)
        Book_from = DateField(null=True)
        Book_to  = DateField(null=True)
        employee = ForeignKeyField(Employee , backref='Daily_employee' , null=True)
        
        class Meta:
            database = db 


ACTIONS_TYPE = (
        (1,'Login'),
        (2,'Update'),
        (3,'Create'),
        (4,'Delete'),
    )



TABLE_CHOICES = (
        (1,'Books'),
        (2,'Clients'),
        (3,'Employee'),
        (4,'Category'),
        (5,'Branch'),
        (6,'Daily Movements'),
        (7,'Publisher'),
        (8,'Author'),
    )


class History(Model):
        employee = ForeignKeyField(Employee , backref='History_employee')
        action = CharField(choices=ACTIONS_TYPE) # Choices 
        table = CharField(choices=TABLE_CHOICES) # Choices
        date = DateTimeField(default=datetime.datetime.now)
        branch = ForeignKeyField(Branch , backref='history_branch')

        class Meta:
            database = db 






db.connect()
db.create_tables([ Author ,Category ,Branch ,Publisher ,Books , Clients , Employee  , Daily_Movements , History ])












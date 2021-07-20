from mainapp import db
from sqlalchemy import Integer, Float, String, Date, Boolean, ForeignKey,DateTime, Column
from sqlalchemy import Column, INTEGER, FLOAT, BOOLEAN, DATE
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from calendar import monthrange


class RoomType(db.Model):
    id=db.Column(Integer, primary_key=True,autoincrement=True)
    name=db.Column(String(50),nullable=False)
    image=db.Column(String(255))
    amount=db.Column(Integer,default=0)
    price=db.Column(Integer,default=0)
    surcharge=db.Column(Float,default=0)
    detail=db.Column(String(1000))
    active=db.Column(Boolean,default=True)
    rooms= relationship('Room',backref='room_type',lazy=True)

    def __str__(self):
        return self.name

class Room(db.Model):
    id=db.Column(Integer,primary_key=True, autoincrement=True)
    name=db.Column(String(50),nullable=False)
    roomtype_id=db.Column(Integer,ForeignKey(RoomType.id),nullable=False)
    active =db.Column(Boolean,default=True)
    book_room=relationship('BookRoom', backref='room', lazy=True)
    report=relationship('Report',backref='room', lazy=True)

    def __str__(self):
        return self.name

class Nationality(db.Model):
    id=db.Column(Integer, primary_key=True, autoincrement=True)
    name=db.Column(String(50),nullable=False)
    users=relationship('User', backref='nationality',lazy=True)

    def __str__(self):
        return self.name

class UserType(db.Model):
    id=db.Column(Integer, primary_key=True, autoincrement=True)
    name=db.Column(String(50),nullable=False)
    active=db.Column(Boolean,default=True)
    users = relationship('User', backref='usertype', lazy=True)

    def __str__(self):
        return self.name

class User(db.Model):
    id=db.Column(Integer,primary_key=True, autoincrement=True)
    name=db.Column(String(50),nullable=False)
    sex=db.Column(Boolean, default=False)
    ic=db.Column(String(15), nullable=False, unique=True)
    phone=db.Column(String(15), nullable=False)
    email=db.Column(String(100),nullable=False)
    address=db.Column(String(300),nullable=False)
    nationality_id =db.Column(Integer, ForeignKey(Nationality.id), nullable=False)
    usertype_id=db.Column(Integer, ForeignKey(UserType.id), nullable=False)
    active=db.Column(Boolean, default=True)
    login_user=relationship('LoginUser',backref='user',lazy=True)
    bill=relationship('Bill',backref='user',lazy=True)
    book_room = relationship('BookRoom', backref='bookroom', lazy=True)
    user_room = relationship('UserRoom', backref='userroom', lazy=True)

    def __str__(self):
        return self.name


class LoginUser(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    username = db.Column(String(50), nullable=False, unique=True)
    password = db.Column(String(50), nullable=False)
    user_id = db.Column(Integer, ForeignKey(User.id))

    def __str__(self):
        return str(self.id)


class Status(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(20), nullable=False)
    book_room = relationship('BookRoom', backref='status', lazy=True)

    def __str__(self):
        return self.name

class Coefficient(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(Date, default=datetime.now())
    active = db.Column(Boolean, default=True)
    amount = db.Column(Integer, default=1)
    coefficient = db.Column(Float, default=0)
    book_room = relationship('BookRoom', backref='coefficient', lazy=True)

    def __str__(self):
        return str(self.created_date)

class BookRoom(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey(User.id), nullable=False)
    check_in = db.Column(Date, default=datetime.now())
    check_out = db.Column(Date, default=datetime.now())
    room_id = db.Column(Integer, ForeignKey(Room.id), nullable=False)
    price = db.Column(Integer, default=0)
    surcharge = db.Column(Float, default=0)
    amount = db.Column(Integer, default=0)
    coefficient_id = db.Column(Integer, ForeignKey(Coefficient.id), nullable=False)
    status_id = db.Column(Integer, ForeignKey(Status.id), nullable=False)
    expire=db.Column(Boolean,default=False)
    bill_detail=relationship('BillDetail',backref='book_room',lazy=True)
    user_room=relationship('UserRoom',backref='book_room',lazy=True)



    def __str__(self):
        return str(self.id)



class Bill(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, ForeignKey(User.id), nullable=False)
    total_price = db.Column(Integer, default=0)
    paid_date = db.Column(Date, default=datetime.now())
    bill_detail=relationship('BillDetail',backref='bill',lazy=True)

    def __str__(self):
        return str(self.id)

class UserRoom(db.Model):
    id=db.Column(Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(Integer,ForeignKey(User.id))
    bookroom_id=db.Column(Integer,ForeignKey(BookRoom.id))

    def __str__(self):
        return str(self.id)

class BillDetail(db.Model):
    id=db.Column(Integer,primary_key=True,autoincrement=True)
    bill_id=db.Column(Integer,ForeignKey(Bill.id))
    bookroom_id=db.Column(Integer,ForeignKey(BookRoom.id))

    def __str__(self):
        return str(self.id)

class Report(db.Model):
    id=db.Column(Integer,primary_key=True,autoincrement=True)
    room_id =db.Column(Integer, ForeignKey(Room.id))
    year=db.Column(Integer,default=datetime.now().year)
    month=db.Column(Integer,default=datetime.now().month)
    used=db.Column(Integer,default=0)
    revenue=db.Column(Integer,default=0)
    end_month=db.Column(Date,default=datetime(datetime.now().year, datetime.now().month,monthrange(datetime.now().year, datetime.now().month)[1],0,0,0))
    date_update=db.Column(DateTime,default=datetime.now())

    def __str__(self):
        str(self.room_id)+" "+str(self.month)+"/"+str(self.year)


#FOOD:
class Category (db.Model):
    __tablename__ = "category"
    id = Column(INTEGER,primary_key=True, autoincrement= True)
    name = Column(String(50),nullable=False)
    products = relationship('Product', backref='category', lazy = True)

    def __str__(self):
        return  self.name


class Product (db.Model):
    __tablename__ = "product"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(FLOAT, default=0)
    image = Column(String(255))
    created_date = Column(DATE, default=datetime.now())
    active = Column(BOOLEAN, default=True)
    category_id = Column(INTEGER, ForeignKey(Category.id))
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    def __str__(self):
        return  self.name

class Receipt(db.Model):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    created_date = Column(DATE, default=datetime.today())
    customer_id = Column(INTEGER, ForeignKey(User.id))
    details = relationship('ReceiptDetail', backref='receipt', lazy = True)

class ReceiptDetail(db.Model):
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    receipt_id = Column(INTEGER, ForeignKey(Receipt.id))
    product_id = Column(INTEGER, ForeignKey(Product.id))
    quantity = Column(INTEGER, default=0)
    price = Column(FLOAT, default=0)

if __name__=='__main__':
    db.create_all()

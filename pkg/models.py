from datetime import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

def utc_now_no_seconds():
    return datetime.utcnow().replace(second=0, microsecond=0)


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100))
    password = db.Column(db.String(200), nullable=False)
    date_reg = db.Column(db.DateTime, default=datetime.utcnow) # type: ignore


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False, index=True)
    lname = db.Column(db.String(100), nullable=False, index=True)
    username = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(100),nullable=False, unique=True)
    user_dp = db.Column(db.String(100))
    phone = db.Column(db.String(100), nullable=False)
    pwd = db.Column(db.String(255),nullable=False)
    regdate = db.Column(db.DateTime, default=datetime.utcnow) # type: ignore


class Product(db.Model):
    __tablename__ = 'product'
    prod_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prod_name = db.Column(db.String(100), index=True)
    amount = db.Column(db.Float)
    status = db.Column(db.String(100))
    category = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    dateadded = db.Column(db.DateTime, default=datetime.utcnow) # type: ignore

    # one-to-many relationship: one product → many images
    images = db.relationship('Image', backref='product', lazy=True, cascade="all, delete-orphan")



class Image(db.Model):
    __tablename__ = 'images'
    img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.prod_id'), nullable=False)


class Category(db.Model):
    __tablename__ = 'category'
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(200), nullable=False)



class Carts(db.Model):
    __tablename__ = 'carts'
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_prod_id = db.Column(db.Integer, db.ForeignKey('product.prod_id'))
    cart_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    cart_qty = db.Column(db.Integer, nullable=False, default=0)
    cart_amt = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    cart_payable = db.Column(db.Numeric(10,2), nullable=False, default=0.00)

    cart = db.relationship('Users', backref='mycart')
    cart = db.relationship('Product',backref='incart')

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_status = db.Column(db.Enum('1','0', name='order_status'), default=1)
    order_userid = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow) # type: ignore
    order_total = db.Column(db.Float(), nullable=True)

    user = db.relationship('Users', backref='myorders')

class OrderDetails(db.Model):
    __tablename__ = 'orderdetails'
    details_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    details_prod_id = db.Column(db.Integer, db.ForeignKey('product.prod_id'))
    details_orderid = db.Column(db.Integer, db.ForeignKey('orders.order_id'))

    order = db.relationship('Orders', backref='details_order')
    orddetail = db.relationship('Product',backref='order_detail')


class Payment(db.Model):
    __tablename__ = 'payment'
    pay_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pay_user = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    pay_order = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    pay_amt = db.Column(db.Float(), nullable=True)
    pay_ref = db.Column(db.String(200), nullable=False)
    pay_date = db.Column(db.DateTime, default=datetime.utcnow) # type: ignore
    pay_status = db.Column(db.Enum('pending','paid','failed', name='pay_status'), default='pending')
    pay_actual = db.Column(db.Float(), nullable=True)
    pay_data = db.Column(db.Text, nullable=True)

    

    # relationship

    paid_user = db.relationship('Users', backref='mypayments')
    paid_order = db.relationship('Orders', backref='paymentorder')


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prod_id = db.Column(db.Integer,db.ForeignKey('product.prod_id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    # FIXED: Use Numeric for money
    price = db.Column(db.Numeric(10,2), nullable=False, default=0.00)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    amt_payable = db.Column(db.Numeric(10,2), nullable=False, default=0.00)
    total = db.Column(db.Numeric(10,2), nullable=False, default=0.00)
    
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('Users', backref='history')
    product = db.relationship('Product', backref='hist')


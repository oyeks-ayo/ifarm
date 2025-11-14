import secrets,os, requests, random , json# type: ignore
from datetime import datetime
from decimal import Decimal
from functools import wraps
from flask import render_template,request,flash,redirect,url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message # type: ignore

from pkg import app, mail
from pkg.models import db, Product,Users, Carts, OrderDetails, Payment, Orders, History
from pkg.forms import UserSignUpForm, UserLoginForm, SettingsForm # type: ignore


def login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        if session.get('isonline') != None:
            return f(*args,**kwargs)
        else:
            flash('You need to be logged in', category='error')
            return redirect(url_for('home'))
    return login_decorator

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('users/home.html',products=products)

@app.route('/user/signup/',methods=['POST','GET'])
def signup():
    form=UserSignUpForm()

    if request.method == 'POST' and form.validate_on_submit():
        print(form.validate_on_submit())
        print(form.data)

        try:
            fname = form.fname.data
            lname = form.lname.data
            uname = form.username.data
            email = form.email.data
            phone = form.phone.data
            pwd = form.password.data
            pwd2 = form.cpassword.data

            if pwd != pwd2:
                raise ValueError('Both password must match!')
            
            existing_user = Users.query.filter_by(email=email).first()

            if existing_user:
                raise ValueError('User with this email already exists')

            if pwd:
                hashed_pwd = generate_password_hash(pwd)
            
            users = Users(fname=fname, lname=lname, username=uname, email=email, phone=phone,pwd=hashed_pwd)

            db.session.add(users)
            db.session.commit()

            flash('Signup was successful','success')
            return redirect(url_for('login'))

        except ValueError as ve:
            flash(str(ve), 'danger')
        except Exception as e:
            flash(str(e),'danger')
            app.logger.error("An error occurred: %s", e, exc_info=True)


    return render_template('users/signup.html', form=form)

@app.route('/user/login/', methods=['GET','POST'])
def login():
    form=UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            username = form.username.data
            pwd = form.password.data


            user = Users.query.filter((Users.username==username)|(Users.email==username)|(Users.phone==username)).first()

            if not user:
                raise ValueError('Invalid username, signup if you don\'t have an account')
            else:
                hash = check_password_hash(user.pwd, pwd)
                if user and hash:
                    session['isonline'] = user.user_id
                    flash('Login successful','success')
                    return redirect(url_for('home'))
                else:
                    raise ValueError('Invalid password!')
        except ValueError as ve:
            flash(str(ve),'danger')
            return redirect(url_for('login'))

    return render_template('users/login.html',form=form)

@app.route('/cart/add/<int:id>/')
@login_required
def cart_add(id):
    user_id = session.get('isonline')

    try:
        in_cart = Carts.query.filter_by(cart_prod_id=id).first()

        if in_cart:
            raise ValueError('Item already in cart!')
        else:
            cart = Carts(cart_prod_id=id,cart_user_id=user_id)
            db.session.add(cart)
            db.session.commit()

            flash('Product added to cart!', 'success')
        return redirect(url_for('home'))
        
    except ValueError as ve:
        flash(str(ve),'danger')
        return redirect(url_for('home'))
    except Exception as e:
        flash(str(e),'danger')

@app.route('/user/cart/')
@login_required
def mycart():
    user_id = session.get('isonline')
    items = Carts.query.filter_by(cart_user_id=user_id).all()

    return render_template('users/cart.html',items=items)


@app.route('/remove/item/<int:id>/')
@login_required
def remove_item(id):
   
    product = Carts.query.get(id)
    # product = Product.query.filter_by(product_id=id)
    db.session.delete(product)
    db.session.commit()

    flash('Product removed successfully','success')
    return redirect(url_for("mycart"))

@app.route('/checkout/', methods=["GET","POST"])
@login_required
def checkout():
    u_id = session.get('isonline')
    my_cart = Carts.query.filter_by(cart_user_id=u_id).all()

    if my_cart:
        total = sum((Decimal(item.cart_amt or 0) * (item.cart_qty or 0) for item in my_cart))
        total = total.quantize(Decimal("0.00"))

    if request.method == 'POST':
        cart_ids = request.form.getlist('cart_id[]')
        prod_ids = request.form.getlist('prod_id[]')
        prices   = request.form.getlist('price[]')
        qtys     = request.form.getlist('quantity[]')

        for cart_id, prod_id, price, qty in zip(cart_ids, prod_ids, prices, qtys):
            cart = Carts.query.filter_by(
                cart_id=cart_id,
                cart_prod_id=prod_id,
                cart_user_id=u_id
            ).first()
            
            if cart:
                cart.cart_amt = price
                cart.cart_qty = qty

        db.session.commit()
        flash('Your checkout is ready for payment', 'success')
        return redirect(url_for('checkout'))

    return render_template('users/checkout.html', cart=my_cart, total=total)

def in_mycart(user_id):
    items = Carts.query.filter_by(cart_user_id=user_id).all()
    return items

@app.route('/cart/pay/',methods=['POST'])
@login_required
def insert_order():
    user_id = session.get('isonline')
    if in_mycart(user_id):

        cart_ids = request.form.getlist('cart_id[]')
        prod_ids = request.form.getlist('prod_id[]')
        prices   = request.form.getlist('price[]')
        qtys     = request.form.getlist('quantity[]')
        payables = request.form.getlist('payable[]')

        for payable,cart_id,prod_id,price,qty in zip(payables,cart_ids, prod_ids, prices, qtys):
            
            cart = Carts.query.filter_by(
                cart_id=cart_id,
                cart_prod_id=prod_id,
                cart_user_id=user_id,
                cart_amt=price,
                cart_qty=qty
            ).first()
            
            if cart:
                cart.cart_payable = payable
                db.session.commit()

            history = History(prod_id=prod_id,
                              user_id=user_id,
                              price=Decimal(price or 0),
                              quantity=qty or 0,
                              amt_payable=Decimal(payable or 0),
                              )
            db.session.add(history)
            db.session.commit()

            hist_id = history.id

            session['history'] = hist_id

        order = Orders(order_status='0',order_userid=user_id)
        db.session.add(order)
        db.session.commit()
        order_id = order.order_id

        mycart = in_mycart(user_id)
        total = 0

        for i in mycart:
            prod_id = i.cart_prod_id
            prod_amt = i.cart_payable
            total = total + prod_amt

            record = OrderDetails(details_prod_id=prod_id,details_orderid=order_id)
            db.session.add(record)
            db.session.commit()

        order.order_total = total
        db.session.commit()

        history.total = total
        db.session.commit()


        ref = int(random.random() * 10000000000000)

        pay = Payment(pay_user=user_id, pay_order=order_id, pay_amt=total, pay_ref=ref)

        db.session.add(pay)
        db.session.commit()
        session['payref'] = ref

        return redirect(url_for('paystack_step1'))
    else:
        return redirect(url_for('checkout'))

@app.route('/paystack/')
@login_required
def paystack_step1():
    if session.get('payref') != None:
        ref = session.get('payref')
        userpayment = Payment.query.filter_by(pay_ref=ref).first()
        amount = userpayment.pay_amt

        u_id = session.get('isonline')
        user = Users.query.get(u_id)
        email = user.email

        url="https://api.paystack.co/transaction/initialize"
        headers = {"Content-Type":"application/json","Authorization":"Bearer sk_test_9abd3f0268eb764945c16e6ee5a09b91a259524a"}
        data = {"reference":ref, "amount":amount*100, "email":email, "callback_url":"http://127.0.0.1:5000/paystack/update"}
            
        response = requests.post(url, headers=headers, data=json.dumps(data))
        json_response = response.json()
        if json_response['status'] == True:
            pay_url = json_response['data']['authorization_url']
            return redirect(pay_url)
        else:
            paystack_error = json_response['message']
            flash(f'Error from paystack:{paystack_error}', category='danger')
            return redirect(url_for('checkout'))
    else:
            flash('Please add items to cart','danger')
            return redirect(url_for('checkout'))
    
@app.route('/paystack/update/')
@login_required
def paystack_update():
    
    ref = session.get('payref')
    if ref != None:

        #to update the db we need to connect to paystack to confirm the transaction
        url= f"https://api.paystack.co/transaction/verify/{ref}"
        headers = {"Content-Type":"application/json","Authorization":"Bearer sk_test_9abd3f0268eb764945c16e6ee5a09b91a259524a"}

        response = requests.get(url,headers=headers)
        json_response = response.json()
        actual = 0
        if json_response.get('status') == True:
            actual = (json_response['data']['amount'])/100
            gateway_rsp = json_response['data']['gateway_response']
            
            if gateway_rsp == 'Successful':
                status = 'paid'
            else:
                status = 'failed'

                hist_id = session.get('history')
                history = History.query.get(hist_id)
                db.session.delete(history)
                db.session.commit()
        else:
            status ='failed'

        #the following will be executed regardless if response is TRUE or NOT
        pay = Payment.query.filter(Payment.pay_ref==ref).first()

        pay.pay_auctual=actual
        pay.pay_status=status
        pay.pay_data =json.dumps(json_response)

        db.session.add(pay)
        db.session.commit()

        empty_cart = Carts.query.filter_by(cart_user_id = session.get('isonline')).all()
        if empty_cart:
            for item in empty_cart:
                db.session.delete(item)
            db.session.commit()
        flash(f'Transaction Completed! Your cart has been emptied!', category='success')
        return redirect(url_for('home'))
    else:
        flash('Continue from here', category='danger')
        return redirect(url_for('checkout'))
    
@app.route('/history/')
@login_required
def history():
    u_id = session.get('isonline')
    history = History.query.filter_by(user_id=u_id).all()
    return render_template('users/history.html',history=history)

def time_ago_filter(dt):
    now = datetime.utcnow()
    diff = now - dt
    
    periods = [
        ('year', 365*24*60*60),
        ('month', 30*24*60*60),
        ('day', 24*60*60),
        ('hour', 60*60),
        ('minute', 60)
    ]
    
    for period, seconds in periods:
        value = diff.total_seconds() // seconds
        if value:
            return f"{int(value)} {period}{'s' if value > 1 else ''} ago"
    return "just now"

# <small>Posted {{ project.datereg_project|time_ago }}</small>
# {Example output: "3 hours ago" #}

app.jinja_env.filters['time_ago'] = time_ago_filter

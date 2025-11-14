import secrets,os, requests, random , json# type: ignore
from functools import wraps
from flask import render_template,request,flash,redirect,url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message # type: ignore

from pkg import app, mail
from pkg.models import db, Admin,Category,Image,Product, Carts,OrderDetails, Payment, Orders
from pkg.forms import AdminSignUpForm,AdminLoginForm, AddProductForm, SettingsForm, UpdateProductForm # type: ignore


def login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        if session.get('adminonline') != None:
            return f(*args,**kwargs)
        else:
            flash('You need to be logged in as an Admin', category='error')
            return redirect(url_for('admin_login'))
    return login_decorator


@app.route('/admin/signup/', methods=['GET','POST'])
def admin_signup():
    form = AdminSignUpForm()
    if request.method == 'POST' and form.validate_on_submit():

        username = form.username.data
        email = form.username.data
        phone = form.username.data
        password = form.password.data
        cpassword = form.cpassword.data

        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            flash('Admin with this email already exists',category='danger')
            return redirect(url_for('admin_signup'))
        
        if password != cpassword:
            flash('Passwords do not match!','danger')
            return redirect(url_for('admin_signup'))
        
        hashed_password = generate_password_hash(password)
        new_admin = Admin(email=email, password=hashed_password,phone=phone,username=username)
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin account created successfully. Please log in.','success')
        return redirect(url_for('admin_login'))
    return render_template('admin/admin_signup.html', form=form)

@app.route('/admin/login/', methods=['GET','POST'])
def admin_login():
    form = AdminLoginForm()
    if request.method == 'POST' and form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        if username.isdigit():
            if len(username) != 11:
                flash('Invalid! Phone number must be 11 digits','danger')
            else:
                admin = Admin.query.filter((Admin.email == username) | (Admin.username == username) | (Admin.phone == username)).first()
                if admin and check_password_hash(admin.password,password) and admin.is_admin:
                    session['admin'] = admin.id
                    flash('Admin login successful','success')
                    return redirect(url_for('admin_home'))
                else:
                    flash('Invalid credentials or not an admin','danger')
                    return redirect(url_for('admin_login'))
        else:
            admin = Admin.query.filter((Admin.email == username) | (Admin.username == username) | (Admin.phone == username)).first()
            if admin and check_password_hash(admin.password,password):
                session['adminonline'] = admin.admin_id
                flash('Admin login successful','success')
                return redirect(url_for('admin_home'))
            else:
                flash('Invalid credentials! You are not an admin','danger')
                return redirect(url_for('admin_login'))
    return render_template('admin/admin_login.html', form=form)

@app.route('/admin/logout/')
@login_required
def admin_logout():
    session.pop('adminonline', None)
    flash('Admin logged out successfully','success')
    return redirect(url_for('admin_login'))

@app.route('/admin/home/')
@login_required
def admin_home():
    form=AddProductForm()
    category = Category.query.all()
    return render_template('admin/admin.html',form=form, category=category)

@app.route('/admin/addproduct/',methods=['GET','POST'])
@login_required
def add_product():
    form=AddProductForm()
    category = Category.query.all()
    products = Product.query.all()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                prod_name = form.name.data.capitalize()
                price = form.price.data
                category = request.form.get('category')
                quantity = form.quantity.data
                pics = form.image.data
                status = form.status.data

                check_product = Product.query.filter_by(prod_name=prod_name).first()

                if check_product:
                    raise ValueError('Product has been registered before, do you wish to make an update? If so, use the update button')

                product = Product(prod_name=prod_name,amount=price,status=status,category=category,quantity=quantity)

                db.session.add(product)
                db.session.commit()

                if pics:
                    if len(pics)>4:
                        raise ValueError('Maximum number file is 4')

                    allowed_format = ['.jpg','.png','.jpeg']
                    for pic in pics:
                        pics_name = pic.filename
                        _,ext = os.path.splitext(pics_name)
                        if ext.lower() not in allowed_format:
                            raise ValueError(f'Image format not supported! {pic.filename}')
                        
                        newname = secrets.token_hex(10) + ext
                        pic.save('pkg/static/products/'+newname)
                        
                        img = Image(filename=newname,product_id=product.prod_id)

                        db.session.add(img)
                    db.session.commit()

                flash('Product added successfully!','success')
                return redirect(url_for('add_product'))
            

            
            except ValueError as ve:
                flash(str(ve), 'danger')
            except Exception as e:
                flash(str(e),'danger')
                app.logger.error("An error occurred: %s", e, exc_info=True)
        else:
            flash ('Something went wrong!', 'warning')
            
    return render_template('admin/admin.html',form=form,
                                                    category=category, 
                                                    products=products)
# *******************************************************************************************************

# ************************************** DELETE PRODUCT**************************************************
@app.route('/admin/delete/product/',methods=['POST'])
@login_required
def delete_product():
    id = request.form.get('id')

    product = Product.query.get(id)
    # product = Product.query.filter_by(product_id=id)

    db.session.delete(product)
    db.session.commit()

    flash('Product deleted successfully','success')
    return redirect(url_for("admin_home"))
# ************************************** DELETE PRODUCT**************************************************

# ************************************** DELETE PRODUCT**************************************************
@app.route('/admin/update/product/', methods=['GET','POST'])
@login_required
def update_product():

    form=UpdateProductForm()
    category = Category.query.all()
    products = Product.query.all()

    if request.method == 'POST':

        if form.validate_on_submit():
            try:
                id = request.form.get('id')
                price = form.price.data
                cat = request.form.get('category')
                quantity = form.quantity.data
                # pics = form.image.data
                pics = [pic for pic in form.image.data if pic and pic.filename]
                status = form.status.data

                product = Product.query.get(id)

                if product:
                    if price:product.amount = price

                    if cat:product.category = cat
                        
                    if quantity:product.quantity = quantity
                    
                    if status:product.status = status

                    db.session.commit()

                if pics:

                    if len(pics)>4:
                        raise ValueError('Maximum number file is 4')
                    
                    allowed_format = ['.jpg','.png','.jpeg']

                    Image.query.filter_by(product_id=id).delete()
                    db.session.commit()

                    for pic in pics:
                        
                        pics_name = pic.filename
                        _,ext = os.path.splitext(pics_name)

                        if ext.lower() not in allowed_format:
                            raise ValueError(f'Image format not supported! {pic.filename}')
                        
                        newname = secrets.token_hex(10) + ext
                        pic.save('pkg/static/products/'+newname)

                        img = Image(filename=newname,product_id=id)
                        db.session.add(img)
                    db.session.commit()

                    flash('Product updated successfully!','success')
                return redirect(url_for('add_product'))
            except ValueError as ve:
                flash(str(ve),'danger')
            except Exception as e:
                flash(str(e), 'danger')
    return render_template('admin/updateproducts.html',form=form,
                                                    category=category, 
                                                    products=products)
# ************************************** UPDATE PRODUCT**************************************************


    
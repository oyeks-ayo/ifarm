from flask import render_template,request,flash,redirect,url_for,session
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.models import db,Users
from pkg.templates.users.forms import UserSignUpForm, UserLoginForm


@app.route('/')
def home():
    return render_template('users/home.html')

@app.route('/user/signup/', methods=['GET','POST'])
def signup():
    form = UserSignUpForm()
    print('I am here')
    if request.method == 'POST' and form.validate_on_submit():
        print('I got here!')
        try:
            fname = form.fname.data
            lname = form.lname.data
            email = form.email.data
            username = form.username.data
            phone = form.phone.data
            pwd = form.password.data
            cpwd = form.cpassword.data

            if pwd != cpwd:
                raise ValueError('Passwords do not match!')
            
            existing_user = Users.query.filter_by(email=email).first()

            if existing_user:
                raise ValueError('Email taken by another user')
            
            if pwd:
                hashed_pwd = generate_password_hash(pwd)

            user = Users(
                fname=fname,
                lname=lname,
                email=email,
                username=username,
                phone=phone,
                password=hashed_pwd
            )

            db.session.add(user)
            db.session.commit()

            flash('Sign up was successful', 'success')
            return redirect(url_for('login'))
            
        except ValueError as ve:
            flash(str(ve), 'danger')
        except Exception as e:
            flash(str(e),'danger')
            app.logger.error("An error occurred: %s", e, exc_info=True)
            


    return render_template('users/signup.html', form=form)

@app.route('/user/login/', methods=['GET','POST'])
def login():
    form = UserLoginForm()
    return render_template('users/login.html', form=form)

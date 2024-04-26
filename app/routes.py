from urllib.parse import urlsplit

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa

from .forms import LoginForm, RegistrationForm
from .extensions import db
from .models import Product, User


def init_routes(app):
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html', title='Home')

    @app.route('/login', methods = ['GET', 'POST'])
    def login():
        if current_user.is_authenticated: # If user is already logged in, return to home
            return redirect(url_for('index'))
        form = LoginForm() # Use login form from forms.py
        if form.validate_on_submit(): # If all required fields are filled
            user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data)) # Search db for username
            if user is None or not user.check_password(form.password.data): # If user doesn't exist in db or password is incorrect
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next') # get 'next' query string at and of url
            if not next_page or urlsplit(next_page).netloc != '': 
                #if there is no next OR next forwards to a different website, then redirect to home
                #To determine if the URL is absolute or relative, parse w/ urlsplit() function & check if netloc is set or not
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, is_admin = 0) #, email=form.email.data) # Not using email at this time
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @app.route('/dbtest')
    def dbtest():
        # new_product = Product(name = "Blackberry Phone", price = 199.99, stock = 3, description = "The ye olden blackberry phone, with the light up keyboard")
        # db.session.add(new_product)
        # db.session.commit()

        # product_count = db.session.query(Product).filter(Product.prod_id)
        # print(product_count)
        # results = db.session.query(Product).all()
        # for r in results:
        #     print(r.prod_id, r.name, r.price)  # , type(r.price))

        u = User(username = 'susan', email='susan@example.com', is_admin = 0)
        u.set_password('kitty')
        print(u.check_password('anotherpassword'))
        print(u.check_password('kitty'))
        db.session.add(u)
        db.session.commit()

        # users = db.session.query(User).all()
        # for r in users:
        #     print(r.username, r.check_password('mypassword'))

        return "hello"

    # test the db
    @app.route('/catalog')
    def catalog():

        results = Product.query.all()

        return render_template('search_results.html', results=results)

    @app.route('/search', methods=['GET', 'POST'])
    def search():

        search_term = request.args.get('query', '')

        if search_term:

            results = Product.search(search_term)

        else:
            results = Product.query.all()

        return render_template('search_results.html', results=results,
                               search_term=search_term)

    @app.route('/itmes_page/<int:prod_id>')
    def items_page(prod_id):

        product = Product.query.get_or_404(prod_id)

        return render_template('items_page.html', results=product)

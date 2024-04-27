from urllib.parse import urlsplit

from flask import Response, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa

from .forms import CheckoutForm, DeleteUserForm, LoginForm, RegistrationForm, \
    UpdateProfileForm
from .extensions import db
from .models import Cart, Order, Product, User
from .utils import admin_required


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

    @app.route('/items_page/<int:prod_id>')
    def items_page(prod_id):

        product = Product.query.get_or_404(prod_id)

        return render_template('items_page.html', results=product)

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        """Page for viewing/updating the user's name, email, and address."""
        form = UpdateProfileForm(obj=current_user)
        if form.validate_on_submit():
            current_user.name = form.name.data
            current_user.email = form.email.data
            current_user.address = form.address.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.name.data = current_user.name
            form.email.data = current_user.email
            form.address.data = current_user.address
        return render_template('profile.html',
                               title='Update Profile', form=form)

    @app.route('/admin', methods=['GET', 'POST'])
    @admin_required
    @login_required
    def admin():
        """Page for deleting users and printing sales report."""
        form = DeleteUserForm()
        form.user.choices = [(user.id, user.username)
                             for user in User.query.all()]
        if form.validate_on_submit():
            user = db.session.get(User, form.user.data)
            db.session.delete(user)
            db.session.commit()
            flash('User has been deleted.')
            return redirect(url_for('admin'))
        return render_template('admin.html',
                               title='Admin Dashboard', form=form)

    @app.route('/admin/sales_report')
    @admin_required
    @login_required
    def sales_report():
        """Returns a CSV file for all orders."""
        data = Order.get_all_orders_in_csv_format()
        return Response(data, mimetype='text/csv',
                        headers={'Content-Disposition':
                                 'attachment; filename=orders.csv'})


    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        """Checkout page for the user's cart"""
        user = current_user
        cart = Cart.query.filter_by(user_id=user.id).first()
        # If there's no cart or an empty cart, redirect.
        if not cart or not cart.items:
            flash('Your cart is empty.')
            return redirect(url_for('catalog'))
        form = CheckoutForm(obj=user)
        if form.validate_on_submit():
            # Payment processing would occur here...
            try:
                order = Order.create_order_from_cart(cart)
                flash('Order placed successfully.')
                return redirect(url_for('order_success'))
            # If product was out of stock...
            except ValueError as e:
                flash(str(e))
                return redirect(url_for('checkout'))
            # If something went wrong with SQL...
            except RuntimeError as e:
                flash("An unexpected error occurred. Please try again.")
                return redirect(url_for('checkout'))
        return render_template('checkout.html',
                               title='Checkout',
                               form=form,
                               cart=cart)


    @app.route('/order_success')
    @login_required
    def order_success():
        """Page for displaying a successful order."""
        return render_template('order_success.html',
                               title='Order Success')

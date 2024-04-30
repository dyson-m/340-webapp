from urllib.parse import urlsplit

from flask import Response, render_template, flash, redirect, session, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa

from .forms import CheckoutForm, DeleteUserForm, LoginForm, RegistrationForm, \
    UpdateProfileForm
from .extensions import db
from .models import Order, Product, User, Cart, CartItem
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
            full_address = f"{form.address.data}, {form.city.data}, {form.state.data} {form.zip_code.data}"  
            user = User(username=form.username.data, name=form.name.data, 
                    email=form.email.data, address=full_address) 
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering!')
            return redirect(url_for('index'))  
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

    @app.route('/cart')
    @login_required
    def cart():
        cart = None  
        if current_user.is_authenticated:
           
            user_id = current_user.id   
            cart = Cart.query.filter_by(user_id=user_id).first_or_404()
            
        if not cart:
            cart = Cart()  
            cart.items = [] 
        return render_template('cart.html', cart=cart)   
      
    
    @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
    def add_to_cart(product_id):
        quantity = int(request.form['quantity'])
        user_id = current_user.id  

       
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            user = User.query.get(user_id)
            cart = Cart(user=user)
            db.session.add(cart)

    
        cart.add_product(product_id, quantity)
        db.session.commit()
        flash('Product added to cart successfully!')
        return redirect(url_for('cart'))
  
    @app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
    def remove_from_cart(product_id):
        user_id = current_user.id  
        cart = Cart.query.filter_by(user_id=user_id).first()
        if cart:
            cart.remove_product(product_id)
            db.session.commit()
            flash('Product removed from cart successfully!')
        else:
            flash('No cart found!', 'error')
        return redirect(url_for('cart'))
    
    
    @app.route('/update_cart_item/<int:item_id>', methods=['POST'])
    def update_cart_item(item_id):
        quantity = int(request.form['quantity'])
        cart_item = CartItem.query.get_or_404(item_id)
        if quantity > 0:
            cart_item.update_quantity(quantity)
            flash('Quantity updated successfully!')
        else:
            db.session.delete(cart_item)
            db.session.commit()
            flash('Item removed from the cart!')
        return redirect(url_for('cart'))

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
                session['order_number'] = order.id
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
        order_number = session.get('order_number', None)
        if order_number:
            session.pop('order_number', None)
            return render_template('order_success.html',
                                   title='Order Success',
                                   order_number=order_number)
        else:
            flash('No order number found.')
            return redirect(url_for('index'))
                                

from urllib.parse import urlsplit

from flask import render_template, flash, redirect, session, url_for, request
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa

from .forms import LoginForm, RegistrationForm
from .extensions import db
from .models import Product, User,Cart,CartItem


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

            results = Product.query.filter(
                sa.or_(Product.name.like(f'%{search_term}%'), 
                       Product.description.like(f'%{search_term}%'))).all()

        else:
            results = Product.query.all()

        return render_template('search_results.html', results=results,
                               search_term=search_term)

    @app.route('/itmes_page/<int:prod_id>')
    def items_page(prod_id):

        product = Product.query.get_or_404(prod_id)

        return render_template('items_page.html', results=product)
    
    
    @app.route('/cart')
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
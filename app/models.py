"""Database models for the e-commerce platform."""
from __future__ import annotations
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager

class User(UserMixin, db.Model):
    """User model for storing user information in the database.

    A user can represent a customer or an admin, and is used for authentication
    and authorization purposes. The user's password is stored as a hashed
    value for security purposes.

    Attributes:
        id (int): The user's unique identifier.
        username (str): The user's unique login name.
        name (str): The user's full name.
        password_hash (str): The hashed password for authentication.
        email (str): The user's email address.
        address (str): The user's physical address.
        is_admin (bool): A flag indicating if the user is an admin.
        cart (Cart): The user's shopping cart.

    Methods:
        set_password: Stores a hashed version of the user's password.
        check_password: Checks if a given password matches the user's password.

    Example:
        >>> user = User(name='Bob Tinker', email='btinker@gmail.com',
        >>>             address='123 Main St.')
        >>> admin = User(name='Alice Tinker', email="atinker@gamil.com",
        >>>              address="123", admin=True)
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True, nullable=True)
    address = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    cart = db.relationship('Cart', uselist=False, back_populates='user',
                           cascade='all, delete-orphan')

    @staticmethod
    def get_user_by_email(email: str) -> User | None:
        """Fetches a user by their email address.

        Args:
            email (str): The user's email address.

        Returns:
            User: The user with the given email address.

        Example:
            >>> user = User(name='Bob Tinker', email="btinker@gmail.com",
            >>>             address='123 Main St.')
            >>> user.get_user_by_email('btinker@gmail.com')
            <User Bob Tinker>
        """
        return User.query.filter_by(email=email).first()

    def set_password(self, password: str):
        """Sets the user's password using a hashed version of the password.

        Args:
            password (str): The user's plaintext password.

        Example:
            >>> user = User(name=..., email=..., address=...)
            >>> user.set_password('password123')
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if a given password matches the user's password.

        Args:
            password (str): The plaintext password to check.

        Returns:
            bool: True if the password matches, False otherwise.

        Example:
            >>> user = User(name=..., email=..., address=...)
            >>> user.set_password('password123')
            >>> user.check_password('password123')
            True
            >>> user.check_password('wrong_password')
            False
        """
        return check_password_hash(self.password_hash, password)

    def update_user_info(self, name: str, address: str):
        """Updates the user's name and address.

        Args:
            name (str): The user's new name.
            address (str): The user's new address.

        Example:
            >>> user = User(name='Bob Tinker', email="btinker@gmail.com",
            >>>             address="123 Main St.")
            >>> user.update_user_info('Robert Tinker', '456 Main St.')
        """
        self.name = name
        self.address = address
        db.session.commit()

    def __repr__(self):
        return f'<User {self.name}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Product(db.Model):
    """Product model for storing product/inventory information in the database.

    Products are meant to represent both information about individual items
    and information about the inventory as a whole.

    Attributes:
        id (int): The product's unique identifier.
        name (str): The product's name.
        description (str): A brief description of the product.
        price (float): The price of the product.
        stock (int): The quantity of the product in stock.

    Methods:
        subtract_stock: Subtracts a given quantity from the product's stock.

    Example:
        >>> product = Product(name='TV', description='A small TV',
        >>>                   price=100.99, stock=5)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    @staticmethod
    def search(query: str):
        """Searches for products based on a search query.

        This method will search for products based on their name
        or description.

        Args:
            query (str): The search query to use.

        Returns:
            List[Product]: A list of products that match the search query.

        Example:
            >>> Product.search('TV')
            [<Product Large TV>, <Product Small TV>]
        """
        query_match = or_(Product.name.ilike(f'%{query}%'),
                          Product.description.ilike(f'%{query}%'))
        return Product.query.filter(query_match).all()

    def subtract_stock(self, quantity: int):
        """Subtracts a given quantity from the product's stock.

        This is intended to be used when a product is purchased and the
        inventory needs to be updated. If the quantity to subtract is greater
        than the available stock, a ValueError is raised.

        Args:
            quantity (int): The quantity to subtract from the stock.

        Raises:
            ValueError: If the quantity to subtract is greater than the
              available stock.

        Example:
            >>> product = Product(name='TV', description='A small TV',
            >>>                   price=100.99, stock=5)
            >>> product.subtract_stock(3)
            >>> product.stock
            2
            >>> product.subtract_stock(999)
            ValueError: Cannot subtract more than available stock: Stock: 2,
                Subtracted: 999
        """
        if self.stock - quantity < 0:
            raise ValueError('Cannot subtract more than available stock:'
                             f' Stock: {self.stock}, Subtracted: {quantity}')
        self.stock -= quantity

    def __repr__(self):
        return f'<Product {self.name}>'


class Cart(db.Model):
    """Cart model for storing user shopping cart information in the database.

    A cart is meant to represent a user's shopping cart, and store the items
    in it as cart items where each cart item is a product and the quantity of
    that product in the cart. Carts are unique to each user.

    Attributes:
        id (int): The cart's unique identifier.
        user_id (int): The user's unique identifier associated with the cart.
        user (User): The user associated with the cart.
        items (List[CartItem]): A list of items in the cart.

    Methods:
        add_product: Adds a product to the cart with an optional quantity.
        remove_product: Removes a product from the cart.
        remove_cart_item: Removes a cart item from the cart.
        get_total_price: Calculates the total price of all items in the cart.

    Example:
        >>> user = User(name=..., email=..., address=...)
        >>> cart = Cart(user=user)
        >>> product = Product(name='TV', description='A small TV',
        >>>                   price=100.99, stock=5)
        >>> cart.add_product(product.id)
        >>> cart.items
        [<CartItem 1>]
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart',
                            cascade='all, delete-orphan')

    def clear_cart(self):
        """Removes all items from the cart.

        Example:
            >>> user = User(name=..., email=..., address=...)
            >>> cart = Cart(user=user)
            >>> product = Product(name='TV', description='A small TV',
            >>>                   price=100.99, stock=5)
            >>> cart.add_product(product.id)
            >>> len(cart.items)
            1
            >>> cart.clear_cart()
            >>> len(cart.items)
            0
        """
        for item in self.items:
            db.session.delete(item)
        db.session.commit()

    def add_product(self, product_id: int, quantity: int = 1):
        """Adds a product to the cart, optionally with a specified quantity.

        If no quantity is provided, the default is 1. If the product is already
        in the cart, the quantity will be added to the current quantity.

        Args:
            product_id (int): The id of the product to be added to the cart.
            quantity (int): The quantity of the product to add to the cart.

        Example:
            >>> user = User(name=..., email=..., address=...)
            >>> cart = Cart(user=user)
            >>> product = Product(name='TV', description='A small TV',
            >>>                   price=100.99, stock=5)
            >>> cart.add_product(product.id)
            >>> cart.items[0].name
            'TV'
        """
        current_item = CartItem.query.filter_by(cart_id=self.id,
                                                product_id=product_id).first()
        if current_item:
            current_item.quantity += quantity
        else:
            new_item = CartItem(cart_id=self.id, product_id=product_id,
                                quantity=quantity)
            db.session.add(new_item)
        db.session.commit()

    def remove_product(self, product_id: int):
        """Removes a product from the cart.

        If the product is not in the cart, nothing happens.

        Args:
            product_id (int): The id of the product to remove from the cart.

        Example:
            >>> user = User(name=..., email=..., address=...)
            >>> cart = Cart(user=user)
            >>> product = Product(name='TV', description='A small TV',
            >>>                   price=100.99, stock=5)
            >>> cart.add_product(product.id)
            >>> len(cart.items)
            1
            >>> cart.remove_product(product.id)
            >>> len(cart.items)
            0
        """
        current_item = CartItem.query.filter_by(cart_id=self.id,
                                                product_id=product_id).first()
        if current_item:
            db.session.delete(current_item)
            db.session.commit()

    def get_total_price(self) -> float:
        """Calculates the total price of all items in the cart.

        Returns:

            float: The total price of all items in the cart.

        Example:
            >>> user = User(name=..., email=..., address=...)
            >>> cart = Cart(user=user)
            >>> product = Product(name='TV', description='A small TV',
            >>>                   price=100.99, stock=5)
            >>> cart.add_product(product.id, quantity=2)
            >>> cart.get_total_price()
            201.98
        """
        return sum(item.quantity * item.product.price for item in self.items)

    def __repr__(self):
        return f'<Cart {self.id}>'


class CartItem(db.Model):
    """CartItem model for storing cart item information in the database.

    Cart items are meant to represent the individual items in a user's cart,
    and store the quantity of each product in the cart. So if a user has 3
    of a product in their cart, there would be one cart item with a quantity
    of 3, rather than 3 separate cart items.

    Attributes:
        id (int): The cart item's unique identifier.
        quantity (int): The quantity of the product in the cart.
        cart_id (int): The cart's unique identifier associated with the item.
        product_id (int): The product's unique identifier associated with the
         item.
        cart (Cart): The cart associated with the item.
        product (Product): The product associated with the item.

    Methods:
        update_quantity: Updates the quantity of the item in the cart.

    """
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product')

    def update_quantity(self, quantity: int):
        """Sets the quantity of the item in the cart.

        If the quantity is less than or equal to 0, the item is removed from
        the cart. Otherwise, the quantity value will simply be updated.
        """
        if quantity <= 0:
            db.session.delete(self)
            db.session.commit()
        else:
            self.quantity = quantity
            db.session.commit()

    def __repr__(self):
        return f'<CartItem {self.id}>'


class Order(db.Model):
    """The model for storing order information in the database.

    Orders are meant to represent completed transactions, and should be created
    after a purchase is completed.

    Attributes:
        id (int): The order's unique identifier.
        user_id (int): The user's id associated with the order.
        order_date (datetime): The date and time the order was placed.
        user (User): The user associated with the order.
        items (List[OrderItem]): A list of items in the order.

    Methods:
        create_order_from_cart: Creates an order from a user's cart.
        get_total_price: Calculates the total price of all items in the order.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User')
    items = db.relationship('OrderItem', back_populates='order',
                            cascade='all, delete-orphan')

    @staticmethod
    def create_order_from_cart(cart: Cart) -> Order:
        """Creates an order from a user's cart.

        Static method meant for directly converting an existing cart into an
        order. This method would be called once the purchase is completed and
        will result a new order being created in the database.

        Args:
            cart (Cart): The user's cart to convert into an order.

        Returns:
            Order: The newly created order.
        """
        order = Order(user_id=cart.user_id, order_date=datetime.now())

        for cart_item in cart.items:
            order_item = OrderItem(product_id=cart_item.product_id,
                                   quantity=cart_item.quantity,
                                   price=cart_item.product.price)
            order.items.append(order_item)
        db.session.add(order)
        db.session.commit()
        return order

    def get_total_price(self) -> float:
        """Calculates the total price of all items in the order.

        This will calculate the historical price of the order based on what
        the order items were set to at the time of creation, and not what
        the products are necessarily associated with now.

        Returns:
            float: The total price of all items in the order.
        """
        return sum(item.quantity * item.price for item in self.items)

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    """The model for storing order item information in the database.

    Order items are meant to represent the individual items in an orders, and
    store the quantity and price of each item at the time of the order. Each
    order item is associated with a specific order and product.

    Attributes:
        id (int): The order item's unique identifier.
        order_id (int): The order's id associated with the item.
        product_id (int): The product's id associated with the item.
        quantity (int): The quantity of the product in the order.
        price (float): The price of the product at the time of the order.
        order (Order): The order associated with the item.
        product (Product): The product associated with the item.
    """
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product')

    def __repr__(self):
        return f'<Order {self.id}>'

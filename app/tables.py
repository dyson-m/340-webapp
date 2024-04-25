# # Purpose: to define classes that represent database tables.

# from datetime import datetime
# from app import app
# from app import db
# from app import login
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin

# with app.app_context():
#     db.Model.metadata.reflect(db.engine)

#     class Product(db.Model):
#         __table__ = db.Model.metadata.tables['product']

#     class User(UserMixin, db.Model):
#         __table__ = db.Model.metadata.tables['usr']

#         def get_id(self):
#             return str(self.user_id)

#         def set_password(self, password):
#             self.password_hash = generate_password_hash(password)

#         def check_password(self, password):
#             return check_password_hash(self.password_hash, password)

# @login.user_loader
# def load_user(id):
#     return db.session.get(User, int(id))
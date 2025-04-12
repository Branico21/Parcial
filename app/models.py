from . import db

class User(db.Model):
    __tablename__ = "user"  # Especifica el nombre de la tabla como 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    # Relación inversa: un usuario puede tener múltiples productos
    products = db.relationship('Product', backref= "user", lazy=True)

class Product(db.Model):
    __tablename__ = "product"  # Especifica el nombre de la tabla como 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)  # URL de la imagen del producto
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relación con la tabla user
from flask import Blueprint, request, jsonify, render_template, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import Product, User, db
import os
from flask import session

main = Blueprint('main', __name__)

# Ruta para la página de registro
@main.route('/registro')
def registro():
    return render_template('registro.html')

# Ruta para la página principal (inicio de sesión)
@main.route('/')
def home():
    return render_template('login.html')  # Renderiza la página de inicio de sesión

# Ruta para manejar el inicio de sesión

@main.route('/login', methods=['POST'])
def login():
    data = request.json

    # Validar los datos
    if not data.get('email') or not data.get('password'):
        return jsonify({"message": "Por favor, completa todos los campos."}), 400

    # Verificar si el usuario existe
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"message": "El correo no está registrado. Por favor, regístrate primero."}), 404

    # Verificar la contraseña
    if not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Contraseña incorrecta. Inténtalo de nuevo."}), 401

    # Guardar el user_id en la sesión
    session['user_id'] = user.id

    # Redirigir según el rol del usuario
    if user.role == "vendedor":
        return jsonify({"message": f"Bienvenido, {user.username}!", "redirect_url": "/agregarProductos"}), 200
    else:
        return jsonify({"message": f"Bienvenido, {user.username}!", "redirect_url": "/comprador"}), 200

# Ruta para manejar el registro de usuarios
@main.route('/register', methods=['POST'])
def register():
    data = request.json

    # Validar los datos
    if not data.get('username') or not data.get('email') or not data.get('password') or not data.get('role'):
        return jsonify({"message": "Faltan datos. Por favor, completa todos los campos."}), 400

    # Verificar si el correo ya está registrado
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "El correo ya está registrado. Usa otro correo."}), 400

    # Cifrar la contraseña
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Crear un nuevo usuario
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()

    # Mostrar mensaje de éxito y redirigir al inicio de sesión
    return jsonify({"message": "Usuario registrado exitosamente. Por favor, inicia sesión.", "redirect_url": "/"}), 201

# Ruta para la página del comprador
@main.route('/comprador')
def comprador():
    productos = Product.query.all()  # Obtener todos los productos
    return render_template('comprador.html', productos=productos)

# Ruta para agregar productos (formulario)
@main.route('/agregarProductos')
def agregar_productos():
    return render_template('agregarProductos.html')

# Función para validar archivos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Ruta para manejar la solicitud POST de agregar productos
@main.route('/add-product', methods=['POST'])
def add_product():
    try:
        # Obtener el user_id de la sesión
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"message": "Usuario no autenticado. Por favor, inicia sesión."}), 401

        # Validar los datos del formulario
        name = request.form.get('productName')
        description = request.form.get('productDescription')
        price = request.form.get('productPrice')
        quantity = request.form.get('productQuantity')
        file = request.files.get('productImage')

        if not name or not description or not price or not quantity or not file:
            return jsonify({"message": "Faltan datos. Por favor, completa todos los campos."}), 400

        # Validar el archivo
        if not allowed_file(file.filename):
            return jsonify({"message": "Formato de archivo no permitido. Usa PNG, JPG, JPEG o GIF."}), 400

        # Verificar si la carpeta de subida existe
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])  # Crear la carpeta si no existe

        # Guardar la imagen en la carpeta de subida
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Crear un nuevo producto
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            quantity=int(quantity),
            image_url=os.path.join('uploads', filename),  # Guardar la ruta relativa en la base de datos
            user_id=user_id  # Asociar el producto con el usuario autenticado
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Producto agregado exitosamente"}), 201

    except Exception as e:
        # Imprimir el error en la terminal para depuración
        print(f"Error al agregar el producto: {e}")
        return jsonify({"message": "Ocurrió un error al intentar agregar el producto."}), 500
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, db

def register_user(data):
    # Verificar si el correo ya está registrado
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "El correo ya está registrado. Usa otro correo."}), 400

    # Cifrar la contraseña
    hashed_password = generate_password_hash(data['password'], method='sha256')

    # Crear un nuevo usuario
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

def login_user(data):
    # Verificar si se proporcionaron los datos necesarios
    if 'email' not in data or 'password' not in data:
        return jsonify({"message": "Faltan datos. Por favor, proporciona correo y contraseña."}), 400

    # Buscar al usuario por correo electrónico
    user = User.query.filter_by(email=data['email']).first()
    
    # Verificar si el usuario existe
    if not user:
        return jsonify({"message": "Usuario no encontrado. Por favor, regístrate primero."}), 404
    
    # Verificar si la contraseña es correcta
    if not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Contraseña incorrecta."}), 401
    
    # Si todo es correcto, permitir el inicio de sesión
    return jsonify({"message": f"Bienvenido, {user.username}!"}), 200
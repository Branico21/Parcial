import os
from flask import jsonify

UPLOAD_FOLDER = 'uploads/'

def upload_file(files):
    if 'file' not in files:
        return jsonify({"message": "No se encontró ningún archivo"}), 400
    file = files['file']
    if file.filename == '':
        return jsonify({"message": "El archivo no tiene nombre"}), 400
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return jsonify({"message": f"Archivo {file.filename} subido exitosamente"}), 200
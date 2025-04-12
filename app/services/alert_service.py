from flask import jsonify

def send_alert(data):
    # Aquí puedes implementar la lógica para enviar alertas (correo, SMS, etc.)
    return jsonify({"message": f"Alerta enviada a {data['email']}"}), 200
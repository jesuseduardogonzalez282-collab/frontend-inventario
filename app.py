from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 🔥 IMPORTANTE: permite conexión con tu frontend

# Página principal
@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>API Inventario</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                text-align: center;
                padding: 50px;
            }
            h1 { color: #38bdf8; }
            .box {
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
            }
            a {
                color: #22c55e;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🚀 API de Inventario de TI</h1>
        <div class="box">
            <p>Bienvenido a mi API</p>
            <p>Endpoints disponibles:</p>
            <ul style="list-style: none;">
                <li><a href="/devices">GET /devices</a></li>
                <li>GET /devices/{id}</li>
                <li>POST /devices</li>
                <li>PUT /devices/{id}</li>
                <li>DELETE /devices/{id}</li>
            </ul>
        </div>
    </body>
    </html>
    """

# Base de datos en memoria
devices = []
current_id = 1

# GET todos
@app.route('/devices', methods=['GET'])
def get_devices():
    return jsonify(devices)

# GET uno
@app.route('/devices/<int:id>', methods=['GET'])
def get_device(id):
    for device in devices:
        if device['id'] == id:
            return jsonify(device)
    return jsonify({"error": "Dispositivo no encontrado"}), 404

# POST crear
@app.route('/devices', methods=['POST'])
def create_device():
    global current_id
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    required_fields = ['nombre', 'tipo', 'estado', 'area']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"El campo {field} es obligatorio"}), 400

    new_device = {
        "id": current_id,
        "nombre": data['nombre'],
        "tipo": data['tipo'],
        "estado": data['estado'],
        "area": data['area'],
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    devices.append(new_device)
    current_id += 1

    return jsonify(new_device), 201

# PUT actualizar
@app.route('/devices/<int:id>', methods=['PUT'])
def update_device(id):
    data = request.get_json()

    for device in devices:
        if device['id'] == id:
            device['nombre'] = data.get('nombre', device['nombre'])
            device['tipo'] = data.get('tipo', device['tipo'])
            device['estado'] = data.get('estado', device['estado'])
            device['area'] = data.get('area', device['area'])
            return jsonify(device)

    return jsonify({"error": "Dispositivo no encontrado"}), 404

# DELETE eliminar
@app.route('/devices/<int:id>', methods=['DELETE'])
def delete_device(id):
    for device in devices:
        if device['id'] == id:
            devices.remove(device)
            return jsonify({"mensaje": "Eliminado correctamente"})
    return jsonify({"error": "Dispositivo no encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)
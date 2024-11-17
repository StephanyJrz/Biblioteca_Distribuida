from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('ubicaciones_prestamos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/ubicaciones/<int:libro_id>', methods=['GET'])
def get_ubicacion(libro_id):
    conn = get_db_connection()
    ubicacion = conn.execute(
        'SELECT * FROM ubicaciones WHERE libro_id = ?',
        (libro_id,)
    ).fetchone()
    conn.close()
    if ubicacion is None:
        return jsonify({"error": "Ubicación no encontrada"}), 404
    return jsonify(dict(ubicacion))

@app.route('/prestamos', methods=['POST'])
def registrar_prestamo():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO prestamos (libro_id, usuario, fecha_prestamo) VALUES (?, ?, ?)',
        (data['libro_id'], data['usuario'], data['fecha_prestamo'])
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Préstamo registrado"}), 201
@app.route('/ubicaciones', methods=['GET'])
def obtener_ubicaciones():
    conn = get_db_connection()
    ubicaciones = conn.execute('SELECT * FROM ubicaciones').fetchall()
    conn.close()
    return jsonify([dict(ubicacion) for ubicacion in ubicaciones])

@app.route('/prestamos', methods=['GET'])
def obtener_prestamos():
    conn = get_db_connection()
    prestamos = conn.execute('SELECT * FROM prestamos').fetchall()
    conn.close()
    return jsonify([dict(prestamo) for prestamo in prestamos])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('catalogo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint para buscar libros
@app.route('/libros', methods=['GET'])
def get_libros():
    titulo = request.args.get('titulo', '').strip()
    autor = request.args.get('autor', '').strip()
    tipo = request.args.get('tipo', None)
    idioma = request.args.get('idioma', '').strip()
    id = request.args.get('id', '').strip()
    editorial = request.args.get('editorial', '').strip()

    query = "SELECT * FROM libros WHERE 1=1"
    params = []
    if titulo:
        query += " AND titulo LIKE ?"
        params.append(f"%{titulo}%")
    if autor:
        query += " AND autor LIKE ?"
        params.append(f"%{autor}%")
    if idioma:
        query += " AND idioma LIKE ?"
        params.append(f"%{idioma}%")
    if tipo:
        query += " AND tipo LIKE ?"
        params.append(f"%{tipo}%")
    if id:
        query += " AND id LIKE ?"
        params.append(f"%{id}%")
    if editorial:
        query += " AND editorial LIKE ?"
        params.append(f"%{editorial}%")

    conn = get_db_connection()
    libros = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(libro) for libro in libros])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


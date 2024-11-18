from flask import Flask, render_template, request
import requests

# Definición de la aplicación Flask
app = Flask(__name__)

# Direcciones de los otros contenedores
CATALOGO_URL = 'http://catalogo:5000'
UBICACIONES_URL = 'http://ubicaciones_prestamos:5000'

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para buscar libros
@app.route('/buscar', methods=['GET'])
def buscar():
    titulo = request.args.get('titulo', '').strip()
    autor = request.args.get('autor', '').strip()
    

    # Solicita datos al contenedor catalogo
    response = requests.get(f'{CATALOGO_URL}/libros', params={'titulo': titulo, 'autor': autor})
    
    if response.status_code == 200:
        libros = response.json()
    else:
        libros = []  # En caso de error, devuelve una lista vacía
    
    return render_template('resultados.html', libros=libros)

# Ruta para registrar préstamos
@app.route('/prestar', methods=['POST'])
def prestar():
    libro_id = request.form.get('libro_id')
    usuario = request.form.get('usuario')
    
    # Enviar datos al fragmento de ubicaciones_prestamos
    response = requests.post(f'{UBICACIONES_URL}/prestamos', json={
        'libro_id': libro_id,
        'usuario': usuario,
        'fecha_prestamo': '2024-11-16'  # Fecha actual o dinámica
    })
    
    if response.status_code == 201:
        mensaje = "Préstamo registrado con éxito."
    else:
        mensaje = "Error al registrar el préstamo."
    
    return render_template('mensaje.html', mensaje=mensaje)


@app.route('/ubicaciones', methods=['GET'])
def consultar_ubicaciones():
    # Solicitar información de ubicaciones al contenedor `ubicaciones_prestamos`
    response = requests.get(f'{UBICACIONES_URL}/ubicaciones')
    if response.status_code == 200:
        ubicaciones = response.json()
    else:
        ubicaciones = []  # Lista vacía en caso de error
    
    return render_template('ubicaciones.html', ubicaciones=ubicaciones)







@app.route('/prestamos', methods=['GET'])
def consultar_prestamos():
    # Solicitar información de préstamos al contenedor `ubicaciones_prestamos`
    response = requests.get(f'{UBICACIONES_URL}/prestamos')
    if response.status_code == 200:
        prestamos = response.json()
    else:
        prestamos = []  # Lista vacía en caso de error
    
    return render_template('prestamos.html', prestamos=prestamos)

@app.route('/disponibilidad', methods=['GET'])
def consultar_disponibilidad():
    # Solicitar información de préstamos al contenedor `ubicaciones_prestamos`
    response = requests.get(f'{CATALOGO_URL}/disponibilidad')
    if response.status_code == 200:
        disponibles = response.json()
    else:
        disponibles = []  # Lista vacía en caso de error
    
    return render_template('disponibilidad.html', disponibles=disponibles)

@app.route('/categorias', methods=['GET'])
def consultar_categoria():
    try:
        # Solicitar información de categorías al servicio `catalogo`
        response = requests.get(f'{CATALOGO_URL}/categorias')
        if response.status_code == 200:
            libros = response.json()  # Datos obtenidos del servicio
        else:
            print("Error al obtener categorías:", response.status_code)
            libros = []  # Lista vacía en caso de error
    except Exception as e:
        print("Error al conectarse con el servicio de catálogo:", e)
        libros = []  # Lista vacía en caso de excepción

    # Pasar los datos a la plantilla
    return render_template('categorias.html', libros=libros)


# Bloque para ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


from flask import Flask, render_template, request, jsonify
from datetime import datetime
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
    idioma = request.args.get('idioma', '').strip()
    editorial = request.args.get('editorial', '').strip()

    # Solicita datos al contenedor catalogo
    response = requests.get(f'{CATALOGO_URL}/libros', params={'titulo': titulo, 'autor': autor, 'idioma': idioma, 'editorial': editorial})
    
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
    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    # Enviar datos al fragmento de ubicaciones_prestamos
    response = requests.post(f'{UBICACIONES_URL}/prestamos', json={
        'libro_id': libro_id,
        'usuario': usuario,
        'fecha_prestamo': fecha_actual  # Fecha actual o dinámica
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
    # Obtén la categoría si está en los parámetros de la consulta (no es obligatorio)
    categoria = request.args.get('categoria', '').strip()

    # Solicita datos al contenedor catálogo
    response = requests.get(f'{CATALOGO_URL}/libros', params={'categoria': categoria})
    
    if response.status_code == 200:
        libros = response.json()
        # Agrupar los libros por categoría
        categorias = {}
        for libro in libros:
            cat = libro.get('categoria', 'Sin categoría')
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(libro['titulo'])
    else:
        categorias = {}  # Diccionario vacío en caso de error

    # Renderiza el template con las categorías agrupadas
    return render_template('categorias.html', categorias=categorias)


# Ruta para verificar audiolibros existentes 
@app.route('/audiolibros', methods=['GET'])
def consultar_audiolibros():

    # Consulta los libros del tipo 'Audiolibro' desde el contenedor catálogo.
    try:
        # Solicitar información de audiolibros al contenedor 'catalogo'
        response = requests.get(f'{CATALOGO_URL}/libros', params={'tipo': 'Audiolibro'})

        if response.status_code == 200:
            audiolibros = response.json()  # Lista de audiolibros
        else:
            audiolibros = []  # Lista vacía en caso de error

        # Renderizar el template con los datos obtenidos
        return render_template('audiolibros.html', tipos=audiolibros)
    
    except Exception as e:
        # Manejo de error
        mensaje_error = f"Error al consultar audiolibros: {str(e)}"
        return render_template('mensaje.html', mensaje=mensaje_error)
    
# Para ver la sinopsis
@app.route('/sinopsis/<int:libro_id>', methods=['GET'])
def sinopsis(libro_id):
    # Solicitar el libro con el ID proporcionado desde el contenedor de catálogo
    response = requests.get(f'{CATALOGO_URL}/libros', params={'id': libro_id})

    if response.status_code == 200:
        libro = response.json()[0]  # Suponemos que el libro con el ID existe
        sinopsis = libro.get('sinopsis', 'No se encontró sinopsis para este libro.')
        return jsonify({'sinopsis': sinopsis})
    else:
        return jsonify({'sinopsis': 'Error al obtener la sinopsis del libro.'}), 404


# Bloque para ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


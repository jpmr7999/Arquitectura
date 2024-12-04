from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from flask_cors import CORS

# Definir la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuración de conexión a MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "5555",  # Asegúrate de que tu contraseña esté configurada correctamente
    "database": "db_elmirador"  # Asegúrate de que el nombre de la base de datos esté bien
}

# Endpoint para servir index.html
@app.route('/')
def serve_index():
    # Este código sirve index.html desde la carpeta 'static'
    return send_from_directory('static', 'index.html')

# Endpoint para Crear Propietario
@app.route('/propietario/crear', methods=['POST'])
def crear_propietario():
    data = request.json
    rut = data.get('rut')
    nombre = data.get('nombre')
    ape_pat = data.get('ape_pat')
    ape_mat = data.get('ape_mat')
    email = data.get('email')
    fono1 = data.get('fono1')
    fono2 = data.get('fono2')
    estado = data.get('estado')

    if not all([rut, nombre, ape_pat, ape_mat, email, fono1, estado]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Propietarios (RutProp, Nombre, ApePat, ApeMat, Email, Fono1, Fono2, Estado) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (rut, nombre, ape_pat, ape_mat, email, fono1, fono2, estado)
        )
        
        connection.commit()
        return jsonify({"message": "Propietario creado exitosamente"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# Endpoint para Crear Edificio
@app.route('/edificio/crear', methods=['POST'])
def crear_edificio():
    data = request.json
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    inmobiliaria = data.get('inmobiliaria')
    lat = data.get('lat')
    log = data.get('log')
    estado = data.get('estado')
    npisos = data.get('npisos')
    valor_gasto_comun = data.get('valor_gasto_comun')

    if not all([nombre, direccion, inmobiliaria, lat, log, estado, npisos, valor_gasto_comun]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Edificios (Nombre, Direccion, Inmobiliaria, Lat, Log, Estado, NPisos, ValorGastoComun) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (nombre, direccion, inmobiliaria, lat, log, estado, npisos, valor_gasto_comun)
        )
        
        connection.commit()
        return jsonify({"message": "Edificio creado exitosamente"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# Endpoint para listar edificios
# Endpoint para Listar edificios
@app.route('/edificio/listar', methods=['GET'])
def listar_edificios():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Consulta ajustada para el campo 'cod'
        cursor.execute("SELECT cod, Nombre, Direccion FROM Edificios")
        edificios = cursor.fetchall()

        edificios_list = []
        for edificio in edificios:
            edificios_list.append({
                "cod": edificio[0],  # Cambio de CodEdificio a cod
                "Nombre": edificio[1],
                "Direccion": edificio[2]
            })

        return jsonify(edificios_list), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

# Endpoint para Crear Departamento
@app.route('/departamento/crear', methods=['POST'])
def crear_departamento():
    data = request.json
    cod_edificio = data.get('codDepto')
    piso = data.get('piso')
    numero = data.get('numero')
    estado = data.get('estado')
    arrendado = data.get('arrendado')
    rut_prop = data.get('rut_prop')
    num_hab = data.get('num_hab')
    num_baños = data.get('num_baños')

    # Validación de campos
    if not all([cod_edificio, piso, numero, estado, rut_prop, num_hab, num_baños]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insertar el nuevo departamento en la base de datos
        cursor.execute(
            "INSERT INTO Departamentos (CodEdificio, Piso, Numero, Estado, Arrendado, RutProp, NumHab, NumBaños) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (cod_edificio, piso, numero, estado, arrendado, rut_prop, num_hab, num_baños)
        )

        connection.commit()
        return jsonify({"message": "Departamento creado exitosamente"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

# Endpoint para Generar Gastos Comunes para un Edificio
@app.route('/gastos/generar', methods=['POST'])
def generar_gastos():
    data = request.json
    mes = data.get('mes')
    año = data.get('año')
    cod_edificio = data.get('cod_edificio')
    
    if not all([año, cod_edificio]):
        return jsonify({"error": "El campo 'año' y 'cod_edificio' son obligatorios"}), 400
    
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Obtener los departamentos del edificio especificado
        cursor.execute("SELECT CodDepto FROM Departamentos WHERE CodEdificio = %s", (cod_edificio,))
        departamentos = cursor.fetchall()
        
        if not departamentos:
            return jsonify({"error": "No existen departamentos para este edificio."}), 400

        for depto in departamentos:
            cursor.execute(
                "INSERT INTO CuotasGC (Mes, Año, ValorPagado, FechaPago, Atrazado, CodDepto) VALUES (%s, %s, %s, %s, %s, %s)",
                (mes, año, 0.00, None, False, depto[0])  # Asociar el gasto al departamento
            )
        
        connection.commit()
        return jsonify({"message": "Gastos generados exitosamente"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)

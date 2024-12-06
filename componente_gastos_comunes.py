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


# Endpoint para Crear Arrendatarios
@app.route('/arrendatario/crear', methods=['POST'])
def crear_arrendatario():
    data = request.json
    rutArre = data.get('rutArre')
    nombre = data.get('nombre')
    apePat = data.get('apePat')
    apeMat = data.get('apeMat')
    email = data.get('email')
    fono1 = data.get('fono1')
    fono2 = data.get('fono2')
    estado = data.get('estado')

    if not all([rutArre, nombre, apePat, apeMat, email, fono1, estado]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Propietarios (RutArre, Nombre, ApePat, ApeMat, Email, Fono1, Fono2, Estado) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (rutArre, nombre, apePat, apeMat, email, fono1, fono2, estado)
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



# Endpoint para Listar edificios
@app.route('/edificio/listar', methods=['GET'])
def listar_edificios():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT cod, Nombre, Direccion FROM Edificios")
        edificios = cursor.fetchall()

        edificios_list = []
        for edificio in edificios:
            edificios_list.append({
                "cod": edificio[0],
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
    codDepto = data.get('codDepto')
    cod_edificio = data.get('cod_edificio')
    piso = data.get('piso')
    numero = data.get('numero')
    arrendado = data.get('arrendado')  # Puede ser 'si' o 'no'
    rut_prop = data.get('rut_prop')
    estado = data.get('estado')
    rutarre = data.get('rutarre')  # Opcional si arrendado es 'no'
    fechainic = data.get('fechainic')
    fechafinc = data.get('fechafinc')
    observacion = data.get('observacion')
    num_hab = data.get('num_hab')
    num_baños = data.get('num_baños')

    # Validaciones
    errores = []

    # Validar campos obligatorios comunes
    if not codDepto:
        errores.append("El código del departamento es obligatorio.")
    if not cod_edificio:
        errores.append("El código del edificio es obligatorio.")
    if not piso:
        errores.append("El piso es obligatorio.")
    if not numero:
        errores.append("El número es obligatorio.")
    if not rut_prop:
        errores.append("El RUT del propietario es obligatorio.")
    if not estado:
        errores.append("El estado es obligatorio.")
    if not num_hab:
        errores.append("El número de habitaciones es obligatorio.")
    if not num_baños:
        errores.append("El número de baños es obligatorio.")

    # Validar arrendado y rutarre
    if arrendado == "si" and not rutarre:
        errores.append("El RUT del arrendatario es obligatorio si el departamento está arrendado.")

    # Validar fechas
    if arrendado == "si" and (not fechainic or not fechafinc):
        errores.append("Las fechas de inicio y fin de contrato son obligatorias si el departamento está arrendado.")

    # Si hay errores, devolverlos
    if errores:
        return jsonify({"error": "Errores de validación", "detalles": errores}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insertar el nuevo departamento en la base de datos
        cursor.execute(
            "INSERT INTO Departamentos (CodDepto, CodEdificio, Piso, Numero, Arrendado, RutProp, Estado, RutArre, FechaIniC, FechaFinC, Observacion, NumHab, NumBaños)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (codDepto, cod_edificio, piso, numero, arrendado, rut_prop, estado, rutarre, fechainic, fechafinc, observacion, num_hab, num_baños)
        )

        connection.commit()
        return jsonify({"message": "Departamento creado exitosamente"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()




if __name__ == '__main__':
    app.run(debug=True)

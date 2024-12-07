from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from flask_cors import CORS
from datetime import datetime


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
    estado = data.get('estado')
    npisos = data.get('npisos')
    valor_gasto_comun = data.get('valor_gasto_comun')

    if not all([nombre, direccion, inmobiliaria, estado, npisos, valor_gasto_comun]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Edificios (Nombre, Direccion, Inmobiliaria, Estado, NPisos, ValorGastoComun) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, direccion, inmobiliaria, estado, npisos, valor_gasto_comun)
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
    rut_prop = data.get('rut_prop')
    rutarre = data.get('rutarre')
    num_hab = data.get('num_hab')
    num_baños = data.get('num_baños')

    # Validaciones
    errores = []

    # Validar campos obligatorios comunes
    if not cod_edificio:
        errores.append("El código del edificio es obligatorio.")
    if not piso:
        errores.append("El piso es obligatorio.")
    if not numero:
        errores.append("El número es obligatorio.")
    if not rut_prop:
        errores.append("El RUT del propietario es obligatorio.")
    if not num_hab:
        errores.append("El número de habitaciones es obligatorio.")
    if not num_baños:
        errores.append("El número de baños es obligatorio.")

    # Si hay errores, devolverlos
    if errores:
        return jsonify({"error": "Errores de validación", "detalles": errores}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insertar el nuevo departamento en la base de datos
        cursor.execute(
            "INSERT INTO Departamentos (CodDepto, CodEdificio, Piso, Numero, RutProp, RutArre, NumHab, NumBaños)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (codDepto, cod_edificio, piso, numero, rut_prop, rutarre, num_hab, num_baños)
        )

        connection.commit()
        return jsonify({"message": "Departamento creado exitosamente"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# Endpoint para Listar departamentos
@app.route('/departamento/listar', methods=['GET'])
def listar_departamentos():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT CodDepto FROM departamentos")
        departamentos = cursor.fetchall()

        departamentos_list = []
        for departamento in departamentos:
            departamentos_list.append({
                "cod": departamento[0]
            })

        return jsonify(departamentos_list), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# Enpoint para generar gastos
@app.route('/gastos/generar', methods=['POST'])
def generar_gastos_comunes():
    data = request.json
    mes = data.get('mes')
    anio = data.get('anio')
    monto_departamento = data.get('monto_departamento')
    departamentos = list(monto_departamento.keys())

    cantidad_departamentos = len(monto_departamento)
    registros_creados = []  # Lista para almacenar los registros insertados
    
    # Validación de entrada
    if not anio:
        return jsonify({"error": "El año es obligatorio."}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        if not mes:
            meses = range(1, 13)  # Generar para todos los meses del año
        else:
            meses = [mes]  # Generar solo para el mes especificado

        for m in meses:
            if cantidad_departamentos == 0:
                cursor.execute("""
                    SELECT d.CodDepto, d.RutProp, d.RutArre, e.ValorGastoComun
                    FROM Departamentos d
                    INNER JOIN Edificios e ON d.CodEdificio = e.Cod
                """)
                departamentos_db = cursor.fetchall()

                for depto in departamentos_db:
                    cod_depto, rut_prop, rut_arre, valor_gasto_comun = depto

                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM CuotasGC 
                        WHERE Mes = %s AND Año = %s AND CodDepto = %s
                    """, (m, anio, cod_depto))
                    existe = cursor.fetchone()[0]

                    if existe > 0:
                        continue

                    valor_cuota = monto_departamento.get(cod_depto, valor_gasto_comun)

                    cursor.execute("""
                        INSERT INTO CuotasGC (Mes, Año, ValorCuota, FechaPago, Atrazado, CodDepto, RutProp, RutArre)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (m, anio, valor_cuota, None, 0, cod_depto, rut_prop, rut_arre))
                    
                    registros_creados.append({
                        "Mes": m,
                        "Año": anio,
                        "ValorCuota": valor_cuota,
                        "CodDepto": cod_depto,
                        "RutProp": rut_prop,
                        "RutArre": rut_arre
                    })

            else:
                for cod_depto in departamentos:
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM CuotasGC 
                        WHERE Mes = %s AND Año = %s AND CodDepto = %s
                    """, (m, anio, cod_depto))
                    existe = cursor.fetchone()[0]

                    if existe > 0:
                        continue

                    valor_cuota = monto_departamento.get(cod_depto)

                    cursor.execute("""
                        SELECT d.RutProp, d.RutArre, e.ValorGastoComun
                        FROM Departamentos d
                        INNER JOIN Edificios e ON d.CodEdificio = e.Cod
                        WHERE d.CodDepto = %s
                    """, (cod_depto,))
                    departamento = cursor.fetchone()

                    if not departamento:
                        return jsonify({"error": f"El departamento {cod_depto} no existe."}), 400

                    rut_prop, rut_arre, valor_gasto_comun = departamento

                    if valor_cuota is None:
                        valor_cuota = valor_gasto_comun

                    cursor.execute("""
                        INSERT INTO CuotasGC (Mes, Año, ValorCuota, FechaPago, Atrazado, CodDepto, RutProp, RutArre)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (m, anio, valor_cuota, None, 0, cod_depto, rut_prop, rut_arre))
                    
                    registros_creados.append({
                        "Mes": m,
                        "Año": anio,
                        "ValorCuota": valor_cuota,
                        "CodDepto": cod_depto,
                        "RutProp": rut_prop,
                        "RutArre": rut_arre
                    })

        connection.commit()

        return jsonify({"message": "Gastos comunes generados exitosamente", "registros": registros_creados}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# Endpoint para pagar gasto
@app.route('/gastos/pagar', methods=['POST'])
def marcar_como_pagado():
    data = request.json
    departamento = data.get('departamento')
    mes = data.get('mes')  # Mes a pagar
    anio = data.get('anio')  # Año a pagar
    fecha_pago = data.get('fecha_pago')  # Fecha de pago

    # Validación de entrada
    if not all([departamento, mes, anio, fecha_pago]):
        return jsonify({"error": "Todos los campos son obligatorios (departamento, mes, año, fecha_pago)."}), 400

    try:
        anio = int(anio)
        mes = int(mes)
        # Convertir la fecha de pago a un objeto datetime
        fecha_pago_dt = datetime.strptime(fecha_pago, '%Y-%m-%d')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Verificar si ya existe un registro de pago para este departamento y período
        cursor.execute("""
            SELECT FechaPago, Atrazado
            FROM CuotasGC
            WHERE CodDepto = %s AND Mes = %s AND Año = %s
        """, (departamento, mes, anio))
        registro = cursor.fetchone()

        if not registro:
            return jsonify({"error": "No existe un registro de gasto común para este departamento y período."}), 404

        fecha_pago_registrada, atrazado = registro  # Desempaquetar la tupla

        # Verificar si ya se ha registrado un pago
        if fecha_pago_registrada:
            return jsonify({
                "estado": "Pago duplicado",
                "departamento": departamento,
                "periodo": f"{mes:02d}-{anio}",
                "fecha_pago": fecha_pago_registrada.strftime('%Y-%m-%d')  # Verificar si no es None
            }), 400

        # Calcular la fecha límite de pago (por ejemplo, fin del mes correspondiente)
        import calendar
        last_day = calendar.monthrange(anio, mes)[1]
        fecha_limite = datetime(anio, mes, last_day)

        # Determinar si el pago es dentro o fuera del plazo
        dentro_del_plazo = fecha_pago_dt <= fecha_limite
        estado_pago = "Pago exitoso dentro del plazo" if dentro_del_plazo else "Pago exitoso fuera de plazo"

        # Actualizar el registro en la base de datos
        cursor.execute("""
            UPDATE CuotasGC
            SET FechaPago = %s, Atrazado = %s
            WHERE CodDepto = %s AND Mes = %s AND Año = %s
        """, (fecha_pago_dt, not dentro_del_plazo, departamento, mes, anio))
        connection.commit()

        # Respuesta con el estado de la transacción
        return jsonify({
            "estado": estado_pago,
            "departamento": departamento,
            "fecha_pago": fecha_pago_dt.strftime('%Y-%m-%d'),
            "periodo": f"{mes:02d}-{anio}"
        }), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


# Enpoint para listar pendientes
@app.route('/gastos/pendientes', methods=['POST'])
def gastos_pendientes():
    data = request.json
    hasta_mes = int(data.get('hasta_mes'))  # Mes hasta el que se quiere consultar
    hasta_anio = int(data.get('hasta_año'))  # Año hasta el que se quiere consultar

    # Validación de entrada
    if not all([hasta_mes, hasta_anio]):
        return jsonify({"error": "Los campos hasta_mes y hasta_año son obligatorios."}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Obtener los gastos pendientes de todos los meses hasta el mes especificado
        cursor.execute("""
            SELECT d.CodDepto, d.RutProp, d.RutArre, e.ValorGastoComun, c.Mes, c.Año
            FROM CuotasGC c
            INNER JOIN Departamentos d ON c.CodDepto = d.CodDepto
            INNER JOIN Edificios e ON d.CodEdificio = e.Cod
            WHERE c.FechaPago IS NULL
            AND (c.Año < %s OR (c.Año = %s AND c.Mes <= %s))
            ORDER BY c.Año ASC, c.Mes ASC
        """, (hasta_anio, hasta_anio, hasta_mes))

        gastos = cursor.fetchall()

        if not gastos:
            return jsonify({"mensaje": "Sin montos pendientes"}), 200

        # Formatear los resultados
        gastos_pendientes = []
        for gasto in gastos:
            cod_depto, rut_prop, rut_arre, valor_gasto_comun, mes, anio = gasto
            gastos_pendientes.append({
                "CodDepto": cod_depto,
                "RutProp": rut_prop,
                "RutArre": rut_arre,
                "ValorGastoComun": valor_gasto_comun,
                "Mes": mes,
                "Año": anio
            })

        return jsonify(gastos_pendientes), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()




if __name__ == '__main__':
    app.run(debug=True)

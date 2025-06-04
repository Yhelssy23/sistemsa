from flask import Flask, render_template, request, redirect, session
from config.conexion import conexion

app = Flask(__name__)
app.secret_key = 'MiClave'

# =========================
# FUNCIONES AUXILIARES
# =========================
def mostrarTodo():
    try:
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM tbcliente')
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al mostrar clientes: {e}")
        return []

def mostrarCliente(id):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tbcliente WHERE id_cliente=%s", (id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error al mostrar cliente: {e}")
        return None

def mostrarUsuarios():
    try:
        with conexion.cursor() as cursor:
            cursor.execute('SELECT * FROM tbusuario')
            return cursor.fetchall()
    except Exception as e:
        print(f"Error al mostrar usuarios: {e}")
        return []

# =========================
# RUTAS PRINCIPALES
# =========================
@app.route('/')
def index():
    if 'usuario' in session:
        clientes = mostrarTodo()
        usuarios = mostrarUsuarios()
        return render_template('registrar.html', clientes=clientes, usuarios=usuarios)
    return render_template("login.html")

@app.route('/insertar', methods=['POST'])
def insertar():
    nombre = request.form['txtnombre']
    nit = request.form['txtnit']

    if not nombre or not nit:
        mensaje = "Faltan datos para insertar cliente."
    else:
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO tbcliente (nombre, nit) VALUES (%s, %s)"
                cursor.execute(sql, (nombre, nit))
                conexion.commit()
            mensaje = "Cliente insertado correctamente."
        except Exception as e:
            mensaje = f"Error al insertar cliente: {e}"

    clientes = mostrarTodo()
    usuarios = mostrarUsuarios()
    return render_template('registrar.html', mensaje=mensaje, clientes=clientes, usuarios=usuarios)

@app.route('/actualizar/<id>')
def actualizar(id):
    dato = mostrarCliente(id)
    return render_template('actualizar.html', dato=dato)

@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente():
    id = request.form['txtid']
    nombre = request.form['txtnombre']
    nit = request.form['txtnit']

    try:
        with conexion.cursor() as cursor:
            sql = "UPDATE tbcliente SET nombre = %s, nit = %s WHERE id_cliente = %s"
            cursor.execute(sql, (nombre, nit, id))
            conexion.commit()
    except Exception as e:
        return f"Error al actualizar cliente: {e}"

    return redirect('/')

@app.route('/eliminar/<id>')
def eliminar(id):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM tbcliente WHERE id_cliente=%s", (id,))
            conexion.commit()
    except Exception as e:
        return f"Error al eliminar cliente: {e}"
    return redirect('/')

@app.route('/comprar', methods=['POST'])
def insertarCompra():
    id = request.form['id']
    producto = request.form['Producto']
    cantidad = request.form['Cantidad']
    costo = request.form['Costo']

    if not id or not producto or not cantidad or not costo:
        return "Faltan datos para registrar la compra"

    try:
        with conexion.cursor() as cursor:
            sql = "INSERT INTO tbcompra (tbcliente_id_cliente, producto, cantidad, costo) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id, producto, cantidad, costo))
            conexion.commit()
    except Exception as e:
        return f"Error al insertar compra: {e}"

    return redirect('/')

@app.route('/vercompras/<id>')
def vercompras(id):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tbcompra WHERE tbcliente_id_cliente=%s", (id,))
            datos = cursor.fetchall()
        return render_template('vercompras.html', datos=datos)
    except Exception as e:
        return f"Error al obtener compras: {e}"

# =========================
# USUARIOS
# =========================
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    user = request.form['txtuser']
    clave = request.form['txtclave']

    if not user or not clave:
        mensaje = "Faltan datos para agregar usuario."
    else:
        try:
            with conexion.cursor() as cursor:
                sql = "INSERT INTO tbusuario (user, clave) VALUES (%s, %s)"
                cursor.execute(sql, (user, clave))
                conexion.commit()
            mensaje = "Usuario agregado correctamente."
        except Exception as e:
            mensaje = f"Error al agregar usuario: {e}"

    clientes = mostrarTodo()
    usuarios = mostrarUsuarios()
    return render_template('registrar.html', mensaje=mensaje, clientes=clientes, usuarios=usuarios)

@app.route('/eliminar_usuario/<id>')
def eliminar_usuario(id):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM tbusuario WHERE id_usuario=%s", (id,))
            conexion.commit()
        mensaje = "Usuario eliminado correctamente."
    except Exception as e:
        mensaje = f"Error al eliminar usuario: {e}"

    clientes = mostrarTodo()
    usuarios = mostrarUsuarios()
    return render_template('registrar.html', mensaje=mensaje, clientes=clientes, usuarios=usuarios)

@app.route('/buscar')
def buscar():
    termino = request.args.get('txtbuscar')
    if not termino:
        return redirect('/')
    
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tbcliente WHERE nombre LIKE %s OR nit LIKE %s", 
                           (f"%{termino}%", f"%{termino}%"))
            clientes = cursor.fetchall()
        mensaje = f"Resultados para: '{termino}'" if clientes else "No se encontraron coincidencias."
    except Exception as e:
        mensaje = f"Error al buscar clientes: {e}"
        clientes = []

    usuarios = mostrarUsuarios()
    return render_template("registrar.html", clientes=clientes, usuarios=usuarios, mensaje=mensaje)

# =========================
# LOGIN / LOGOUT
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = ''
    if request.method == 'POST':
        user = request.form['txtuser']
        clave = request.form['txtclave']
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM tbusuario WHERE user=%s AND clave=%s", (user, clave))
                usuario = cursor.fetchone()
            if usuario:
                session['usuario'] = usuario[1]
                return redirect('/')
            else:
                mensaje = "Usuario o contraseña incorrectos."
        except Exception as e:
            return f"Error al iniciar sesión: {e}"

    return render_template('login.html', mensaje=mensaje)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)

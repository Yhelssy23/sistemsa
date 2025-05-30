from config.conexion import conexion
from flask import Flask, render_template,request,redirect,session

app = Flask(__name__)

app.secret_key='MiClave'

def mostrarTodo():
    cursor = conexion.cursor()
    cursor.execute('select * from tbcliente')
    clientes = cursor.fetchall()
    cursor.close()
    return clientes


@app.route('/insertar', methods=['POST'])
def insertar():
    nombre=request.form['txtnombre']
    nit=request.form['txtnit']
    cursor = conexion.cursor()
    sql="INSERT INTO tbcliente (nombre, nit) VALUES (%s, %s)"
    cursor.execute(sql, (nombre , nit))
    conexion.commit()
    cursor.close()
    clientes=mostrarTodo()
    mensaje="Registro insertado correctamente"
    return render_template ('registrar.html',mensaje=mensaje,clientes=clientes)

@app.route('/')
def index():
    if 'usuario' in session:
        datos=mostrarTodo()
        return render_template('registrar.html', clientes=datos)
    return render_template("login.html")

@app.route('/actualizar/<id>')
def actualizar(id):
    cursor=conexion.cursor()
    sql="select * from tbcliente where id_cliente=%s"
    cursor.execute(sql,(id,))
    dato=cursor.fetchone()
    cursor.close
    return render_template('actualizar.html' ,dato=dato)

@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente():
    id = request.form['id']
    nombre = request.form['nombre']
    nit = request.form['nit']
    cursor = conexion.cursor()
    sql = "UPDATE tbcliente SET nombre = %s, nit = %s WHERE id_cliente = %s"
    cursor.execute(sql, (nombre, nit, id))
    conexion.commit()
    cursor.close()
    return redirect('/')

@app.route('/eliminar/<id>')
def eliminar(id):
    cursor=conexion.cursor()
    sql=("DELETE FROM tbcliente WHERE id_cliente=%s")
    cursor.execute(sql,(id,))
    conexion.commit()
    cursor.close()
    return redirect('/')

@app.route('/comprar', methods=['POST'])
def insertarCompra():
    id = request.form['id']
    producto = request.form['Producto']
    cantidad = request.form['Cantidad']
    costo = request.form['Costo']
    cursor = conexion.cursor()
    sql = "INSERT INTO tbcompra (tbcliente_id_cliente,producto,cantidad,costo) VALUES (&s,%s,&s,&s)"
    cursor.execute(sql, (id,producto,cantidad,costo))
    conexion.commit()
    cursor.close()
    return redirect('/')

@app.route('/vercompras/<id>', methods=['GET'])
def vercompras(id):
    cursor=conexion.cursor()
    sql="SELECT * FROM tbcompra where tbcliente_id_cliente=%s"
    cursor.execute(sql,(id,))
    datos=cursor.fetchall()
    return render_template('vercompras.html', datos=datos)

def mostrarCliente(id):
    cursor=conexion.cursor()
    sql="SELECT * FROM tbcliente WHERE id_cliente=%s"
    cursor.execute(sql,(id,))
    dato=cursor.fetchone()
    return dato

@app.route('/login', methods=['GET','POST'])
def login():
    mensaje=''
    if request.method=='POST':
        user=request.form['txtuser']
        clave=request.form['txtclave']

        cursor=conexion.cursor()
        sql='Select * from tbusuario where user=%s AND clave =%s'
        cursor.execute(sql,(user,clave))
        usuario=cursor.fetchone()
        cursor.close()

        if usuario:
            session['usuario']=usuario[1]
            session['clave']=usuario[3]
            return redirect('/')
        else:
            mensaje="Usuario o contraseña incorrecto"
    return render_template('login.html',mensaje=mensaje)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
    

if __name__=='__main__':
    app.run(debug=True)

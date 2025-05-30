import mysql.connector     

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="tbventas"
)

if conexion.is_connected():
    print("conexion exitosa")


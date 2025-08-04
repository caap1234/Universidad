import mysql.connector
import hashlib
from datetime import datetime
import getpass

conexion = mysql.connector.connect(
    host="localhost",
    user="universidad",
    password="Qw3rty@2812",
    database="seguridad_db"
)

class Usuario:
    def __init__(self, nombre, password):
        self.nombre = nombre
        self._password = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def guardar_en_bd(self):
        sql = "INSERT INTO usuarios (nombre, password_hash) VALUES (%s, %s)"
        with conexion.cursor() as cursor:
            cursor.execute(sql, (self.nombre, self._password))
            conexion.commit()

class GestorAccesos:
    def login(self, nombre, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        sql = "SELECT * FROM usuarios WHERE nombre = %s AND password_hash = %s"
        with conexion.cursor() as cursor:
            cursor.execute(sql, (nombre, password_hash))
            usuario = cursor.fetchone()
        exito = 1 if usuario else 0
        self._registrar_intento(nombre, exito)
        return exito

    def _registrar_intento(self, usuario, exito):
        fecha = datetime.now()
        sql = "INSERT INTO accesos (usuario, fecha, exito) VALUES (%s, %s, %s)"
        with conexion.cursor() as cursor:
            cursor.execute(sql, (usuario, fecha, exito))
            conexion.commit()

    def mostrar_historial(self, nombre):
        sql = "SELECT fecha, exito FROM accesos WHERE usuario = %s"
        with conexion.cursor() as cursor:
            cursor.execute(sql, (nombre,))
            return cursor.fetchall()

def menu():
    gestor = GestorAccesos()
    try:
        while True:
            print("\n--- MENÚ ---")
            print("1. Registrar nuevo usuario")
            print("2. Iniciar sesión")
            print("3. Ver historial de accesos")
            print("4. Salir")
            opcion = input("Elige una opción: ")

            if opcion == "1":
                nombre = input("Nombre de usuario: ")
                password = getpass.getpass("Contraseña: ")
                usuario = Usuario(nombre, password)
                usuario.guardar_en_bd()
                print("Usuario registrado correctamente.")

            elif opcion == "2":
                nombre = input("Nombre de usuario: ")
                password = getpass.getpass("Contraseña: ")
                if gestor.login(nombre, password):
                    print("Acceso concedido")
                else:
                    print("Acceso denegado")

            elif opcion == "3":
                nombre = input("Nombre de usuario: ")
                historial = gestor.mostrar_historial(nombre)
                if historial:
                    for intento in historial:
                        estado = "Éxito" if intento[1] else "Fallo"
                        print(f"Fecha: {intento[0]} - {estado}")
                else:
                    print("No hay historial disponible.")

            elif opcion == "4":
                print("Saliendo del programa...")
                break
            else:
                print("Opción inválida.")
    except KeyboardInterrupt:
        print("\nPrograma terminado. ¡Hasta luego!")

if __name__ == "__main__":
    menu()

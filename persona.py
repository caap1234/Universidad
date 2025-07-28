 # Definición de la clase Persona
 class Persona:
     def __init__(self, nombre, edad, ocupacion=None):
         self.nombre = nombre
         self.edad = edad
         self.ocupacion = ocupacion
 
     def presentar(self):
         if self.ocupacion:
             print(f"\nHola, mi nombre es {self.nombre}, tengo {self.edad} años y trabajo como {self.ocupacion}.")
         else:
             print(f"\nHola, mi nombre es {self.nombre}, tengo {self.edad} años y actualmente estoy desempleado.")
 
     def contratar(self, nueva_ocupacion):
         self.ocupacion = nueva_ocupacion
         print(f"\n{self.nombre} ha sido contratado como {self.ocupacion}.")
 
 # Lista para almacenar personas
 personas = []

# Personas predefinidas (una con ocupación y tres con diferentes datos)
personas.append(Persona("Carlos", 35, "Profesor"))
personas.append(Persona("Ana", 29, "Diseñadora"))
personas.append(Persona("Luis", 22))
personas.append(Persona("Marta", 41, "Médico"))

 # Función para mostrar menú principal
 def mostrar_menu():
     print("\n----- MENÚ PRINCIPAL -----")
     print("1. Agregar persona")
     print("2. Contratar persona")
     print("3. Ver presentación de persona")
     print("4. Salir")
     return input("Selecciona una opción: ")
 
 # Función para seleccionar persona con opción de regresar
 def seleccionar_persona():
     if not personas:
         print("\nNo hay personas registradas.")
         return None
     while True:
         print("\nPersonas disponibles:")
         for i, persona in enumerate(personas):
             print(f"{i + 1}. {persona.nombre}")
         print("0. Regresar")
         try:
             seleccion = int(input("Selecciona el número de la persona: "))
             if seleccion == 0:
                 return None
             elif 1 <= seleccion <= len(personas):
                 return personas[seleccion - 1]
             else:
                 print("Número fuera de rango.")
         except ValueError:
             print("Entrada inválida. Ingresa un número.")
 
 # Bucle principal con manejo de Ctrl+C
 try:
     while True:
         opcion = mostrar_menu()
 
         if opcion == "1":
             print("\n--- Agregar persona ---")
             nombre = input("Nombre: ")
             edad_input = input("Edad: ")
             try:
                 edad = int(edad_input)
                 nueva_persona = Persona(nombre, edad)
                 personas.append(nueva_persona)
                 print(f"{nombre} fue agregada correctamente.")
             except ValueError:
                 print("Edad inválida. Debe ser un número entero.")
 
         elif opcion == "2":
             print("\n--- Contratar persona ---")
             persona = seleccionar_persona()
             if persona:
                 ocupacion = input(f"¿Qué ocupación tendrá {persona.nombre}? ")
                 persona.contratar(ocupacion)
 
         elif opcion == "3":
             print("\n--- Presentar persona ---")
             persona = seleccionar_persona()
             if persona:
                 persona.presentar()
 
         elif opcion == "4":
             print("\nGracias por usar el programa. ¡Hasta luego!")
             break
 
         else:
             print("\nOpción no válida. Intenta de nuevo.")
 
 except KeyboardInterrupt:
     print("\n\nCerrando ...")
 

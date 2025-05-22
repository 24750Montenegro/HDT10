# ---------------------------------------------------------------
# Universidad: Universidad del Valle de Guatemala
# Curso: Algoritmos y Estructuras de Datos
# Nombre: Javier Alvarado, Juan Montenegro
# Carné: 24545, 24750
# Fecha: 21/05/2025
# Descripción: Programa para gestionar rutas entre ciudades usando
# el algoritmo de Floyd-Warshall, considerando diferentes climas.
# Permite consultar rutas más cortas, centro del grafo y modificar
# conexiones y clima.
# ---------------------------------------------------------------

# Lista de climas posibles y variable global para el clima actual
CLIMAS = ["normal", "lluvia", "nieve", "tormenta"]
IDX_CLIMA = 0 

class Grafo:
    def __init__(self):
        # Diccionario de ciudades y conexiones
        self.ciudades = {}
        self.pesos = {}
        self.distancias = {}
        self.antecesores = {}

    def agregar_conexion(self, c1, c2, tiempos):
        # Agrega una conexión bidireccional entre dos ciudades con los tiempos dados
        self.ciudades.setdefault(c1, {})
        self.ciudades.setdefault(c2, {})
        self.ciudades[c1][c2] = tiempos
        self.ciudades[c2][c1] = tiempos

    def interrumpir_conexion(self, c1, c2):
        # Elimina la conexión entre dos ciudades
        if c2 in self.ciudades.get(c1, {}):
            del self.ciudades[c1][c2]
        if c1 in self.ciudades.get(c2, {}):
            del self.ciudades[c2][c1]

    def establecer_clima(self, clima):
        # Cambia el clima actual si es válido
        global IDX_CLIMA
        if clima in CLIMAS:
            IDX_CLIMA = CLIMAS.index(clima)

    def floyd_warshall(self):
        # Calcula las distancias más cortas entre todas las ciudades
        nodes = list(self.ciudades.keys())
        dist = {i: {j: float('inf') for j in nodes} for i in nodes}
        prev = {i: {j: None for j in nodes} for i in nodes}

        for u in nodes:
            dist[u][u] = 0
            for v in self.ciudades[u]:
                dist[u][v] = self.ciudades[u][v][IDX_CLIMA]
                prev[u][v] = u

        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        prev[i][j] = prev[k][j]

        self.distancias = dist
        self.antecesores = prev

    def ruta_mas_corta(self, origen, destino):
        # Devuelve la distancia y el camino más corto entre dos ciudades
        if origen not in self.distancias or destino not in self.distancias[origen]:
            return None, []

        camino = []
        actual = destino
        while actual != origen:
            camino.insert(0, actual)
            actual = self.antecesores[origen].get(actual)
            if actual is None:
                return None, []
        camino.insert(0, origen)
        return self.distancias[origen][destino], camino

    def centro_grafo(self):
        # Devuelve el centro del grafo (ciudad con menor distancia máxima a otras)
        max_min = float('inf')
        centro = None
        for nodo in self.distancias:
            distancias = self.distancias[nodo]
            max_d = max(distancias.values())
            if max_d < max_min:
                max_min = max_d
                centro = nodo
        return centro

    def mostrar_matriz_adyacencia(self):
        # Imprime la matriz de adyacencia según el clima actual
        print("")
        print("Matriz de adyacencia, clima : " + CLIMAS[IDX_CLIMA] )
        print("")

        ciudades = list(self.ciudades.keys())
        ancho = max(len(c) for c in ciudades) + 2

        encabezado = " " * ancho
        for ciudad in ciudades:
            encabezado += ciudad.center(ancho)
        print(encabezado)

        for i in ciudades:
            fila = i.ljust(ancho)
            for j in ciudades:
                if j in self.ciudades[i]:
                    valor = str(self.ciudades[i][j][IDX_CLIMA])
                elif i == j:
                    valor = "0"
                else:
                    valor = "X"
                fila += valor.center(ancho)
            print(fila)
        print("")


class Interfaz:
    def __init__(self):
        # Inicializa la interfaz con un grafo vacío
        self.grafo = Grafo()

    def leer_archivo(self, nombre_archivo):
        # Lee las conexiones de un archivo y las agrega al grafo
        with open(nombre_archivo, "r") as f:
            for linea in f:
                datos = linea.strip().split()
                c1, c2 = datos[0], datos[1]
                tiempos = list(map(int, datos[2:]))
                self.grafo.agregar_conexion(c1, c2, tiempos)
        self.grafo.floyd_warshall()

    def mostrar_menu(self):
        # Muestra el menú principal
        print("")
        print("--- Menú ---")
        print("1. Ruta más corta entre dos ciudades")
        print("2. Centro del grafo")
        print("3. Modificaciones")
        print("4. Salir")
        print("")

    def mostrar_ciudades(self):
        # Muestra la lista de ciudades disponibles
        ciudades = list(self.grafo.ciudades.keys())
        for i, c in enumerate(ciudades):
            print(str(i) + ". " + c)
        return ciudades

    def ejecutar(self):
        # Método principal que ejecuta el programa y gestiona la interacción con el usuario
        archivo = "guategrafo.txt"
        self.leer_archivo(archivo)
        self.grafo.mostrar_matriz_adyacencia()

        opcion = ""
        while opcion != "4":
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                # Opción para mostrar la ruta más corta entre dos ciudades
                print("Ciudades disponibles:")
                ciudades = self.mostrar_ciudades()
                print("")
                idx1 = int(input("Ingrese el número de la ciudad origen: "))
                idx2 = int(input("Ingrese el número de la destino: "))
                origen = ciudades[idx1]
                destino = ciudades[idx2]
                dist, ruta = self.grafo.ruta_mas_corta(origen, destino)
                if dist is not None:
                    print("Distancia: " + str(dist) + " horas")
                    print("Ruta: " + " -> ".join(ruta))
                else:
                    print("No hay ruta disponible.")

            elif opcion == "2":
                # Opción para mostrar el centro del grafo
                centro = self.grafo.centro_grafo()
                print("Centro del grafo: " + centro)

            elif opcion == "3":
                # Opción para modificar conexiones o clima
                print("")
                print("Selecciona una modificación:")
                print("1. Interrumpir conexión")
                print("2. Establecer nueva conexión")
                print("3. Cambiar clima actual")
                opcionMod = input("Seleccione una opción: ")

                if opcionMod == "1":
                    # Interrumpir conexión entre dos ciudades
                    print("Seleccione ciudad 1:")
                    ciudades = self.mostrar_ciudades()
                    idx1 = int(input("Número ciudad 1: "))
                    print("Seleccione ciudad 2:")
                    idx2 = int(input("Número ciudad 2: "))
                    c1 = ciudades[idx1]
                    c2 = ciudades[idx2]
                    self.grafo.interrumpir_conexion(c1, c2)

                elif opcionMod == "2":
                    # Establecer nueva conexión entre dos ciudades
                    print("Seleccione ciudad 1:")
                    ciudades = self.mostrar_ciudades()
                    idx1 = int(input("Número ciudad 1: "))
                    print("Seleccione ciudad 2:")
                    idx2 = int(input("Número ciudad 2: "))
                    c1 = ciudades[idx1]
                    c2 = ciudades[idx2]
                    tiempos = list(map(int, input("Ingrese los 4 tiempos (normal lluvia nieve tormenta): ").split()))
                    self.grafo.agregar_conexion(c1, c2, tiempos)

                elif opcionMod == "3":
                    # Cambiar el clima actual
                    print("Climas disponibles: " + ", ".join(CLIMAS))
                    clima = input("Ingrese nuevo clima: ")
                    self.grafo.establecer_clima(clima)

                # Actualiza las distancias y muestra la matriz
                self.grafo.floyd_warshall()
                self.grafo.mostrar_matriz_adyacencia()

            elif opcion == "4":
                # Salir del programa
                print("Finalizando la ejecución. Hasta luego :)")

            else:
                print("Opción no válida.")

if __name__ == "__main__":
    # Punto de entrada del programa
    interfaz = Interfaz()
    interfaz.ejecutar()
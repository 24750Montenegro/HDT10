CLIMAS = ["normal", "lluvia", "nieve", "tormenta"]
IDX_CLIMA = 0 

class Grafo:
    def __init__(self):
        self.ciudades = {}
        self.pesos = {}
        self.distancias = {}
        self.antecesores = {}

    def agregar_conexion(self, c1, c2, tiempos):
        self.ciudades.setdefault(c1, {})
        self.ciudades.setdefault(c2, {})
        self.ciudades[c1][c2] = tiempos
        self.ciudades[c2][c1] = tiempos

    def interrumpir_conexion(self, c1, c2):
        if c2 in self.ciudades.get(c1, {}):
            del self.ciudades[c1][c2]
        if c1 in self.ciudades.get(c2, {}):
            del self.ciudades[c2][c1]

    def establecer_clima(self, clima):
        global IDX_CLIMA
        if clima in CLIMAS:
            IDX_CLIMA = CLIMAS.index(clima)

    def floyd_warshall(self):
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



    def mostrar_matriz_adyacencia(self):
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
        self.grafo = Grafo()

    def leer_archivo(self, nombre_archivo):
        with open(nombre_archivo, "r") as f:
            for linea in f:
                datos = linea.strip().split()
                c1, c2 = datos[0], datos[1]
                tiempos = list(map(int, datos[2:]))
                self.grafo.agregar_conexion(c1, c2, tiempos)
        self.grafo.floyd_warshall()


    def ejecutar(self):
        archivo = "logistica.txt"
        self.leer_archivo(archivo)
        self.grafo.mostrar_matriz_adyacencia()


if __name__ == "__main__":
    interfaz = Interfaz()
    interfaz.ejecutar()

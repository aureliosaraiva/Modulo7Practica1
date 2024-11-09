import json
import math
import statistics

def read_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

class Recomendation:
    json_data = None
    users = None
    movies = set()

    def __init__(self):
        self.json_data = read_data("src/data.json")
        self.users = [item['usuario'] for item in self.json_data]
        for item in self.json_data:
            self.movies.update(item['valoraciones'].keys())
        self.movies = list(self.movies)

    def devolver_valoraciones(self, usuario):
        for i, elem in enumerate(self.json_data):
            if elem['usuario'] == usuario:
                return(elem['valoraciones'])
            
    def calcularmedia(self, valoracion1,valoracion2):
        cont = 0
        suma1 = 0
        suma2 = 0
        r_a = []
        r_b = []
        for elem in valoracion1:
            if elem in valoracion2:
                cont += 1
                suma1 += valoracion1.get(elem)
                suma2 += valoracion2.get(elem)
                r_a.append(valoracion1.get(elem))
                r_b.append(valoracion2.get(elem))
        return(r_a, r_b, suma1/cont, suma2/cont)
    
    def calcular_similitud(self, usuario1, usuario2):
        val1 = self.devolver_valoraciones(usuario1)
        val2 = self.devolver_valoraciones(usuario2)
        r_a, r_b, r_a_med, r_b_med = self.calcularmedia(val1,val2)
        
        numerador = 0
        denominador1 = 0
        denominador2 = 0
        
        for i, elem in enumerate(r_a):
            numerador += (elem - r_a_med) * (r_b[i] - r_b_med)
            denominador1 +=  ((elem - r_a_med) ** 2)
            denominador2 +=  ((r_b[i] - r_b_med) ** 2)

        return(numerador/(math.sqrt(denominador1) * math.sqrt(denominador2)))
    
    def calcular_similitudes(self):
        matriz = {}
        for i in range(0,len(self.users)):
            elem = {}
            for j in range(0,len(self.users)):
                if i != j:
                    elem[self.users[j]] = self.calcular_similitud(self.users[i],self.users[j])
            matriz[self.users[i]] = elem
        return(matriz)
    
    def usuarios_parecidos(self, usuario, g):
        m = self.calcular_similitudes()
        l = []
        valoracion = m[usuario]
        for key, value in valoracion.items():
            if value >= g:
                l.append(key)
        return l
    
    def devolver_series_sin_valorar(self):
        falta = []
        for i in range(0,len(self.json_data)):
            usuario = self.json_data[i]['usuario']
            valoracion = self.json_data[i].get('valoraciones')
            for j in range(0,len(self.movies)):
                if not self.movies[j] in valoracion:
                    elem = {}
                    elem['usuario'] = usuario
                    elem['pelicula'] = self.movies[j]
                    elem['posicion'] = i
                    falta.append(elem)
        return(falta)
    
    def calcular_media_total(self, usu):
        val = self.devolver_valoraciones(usu)
        return(statistics.mean(tuple(val.values())))

    def prediccion(self, usu, pelicula):
        l = self.usuarios_parecidos(usu, 0.7)
        m = self.calcular_similitudes()
        numerador = 0
        denominador = 0
        for i in l:
            numerador += m[usu][i] * (self.devolver_valoraciones(i).get(pelicula,0) - self.calcular_media_total(i))
            denominador += m[usu][i]
        return(numerador / denominador + self.calcular_media_total(usu))
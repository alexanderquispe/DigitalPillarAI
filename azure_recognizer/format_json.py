import json

class J1SON:
    def __init__(self):
        self.algo = 12
        self.nada = {
            'algo': 'nada',
            'todo': 12
        }
        self.array = [12, 32, 4, 2342, 34]  # Corrección: Añadir comas entre los elementos del array

# Crear una instancia de la clase J1SON
a = J1SON()

# Convertir el objeto en JSON
json_data = json.dumps(a.__dict__, indent=4)

# Imprimir el JSON resultante
print(json_data)

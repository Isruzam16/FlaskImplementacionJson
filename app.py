import json
from flask import Flask, render_template, request

app = Flask(__name__)

class Persona:
    def __init__(self, nombre, edad, ciudad, correo, telefono, carrera, universidad, pais, hobbies, descripcion):
        self.nombre = nombre
        self.edad = edad
        self.ciudad = ciudad
        self.correo = correo
        self.telefono = telefono
        self.carrera = carrera
        self.universidad = universidad
        self.pais = pais
        self.hobbies = hobbies
        self.descripcion = descripcion

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    edad = request.form['edad']
    ciudad = request.form['ciudad']
    correo = request.form['correo']
    telefono = request.form['telefono']
    carrera = request.form['carrera']
    universidad = request.form['universidad']
    pais = request.form['pais']
    hobbies = request.form['hobbies']
    descripcion = request.form['descripcion']

    # Crear una instancia de la clase Persona
    persona = Persona(nombre, edad, ciudad, correo, telefono, carrera, universidad, pais, hobbies, descripcion)

    # Cargar los datos existentes del archivo JSON
    try:
        with open('personas.json', 'r') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        datos = []

    # Agregar el nuevo registro a la lista de datos
    datos.append(persona.__dict__)

    # Guardar los datos actualizados en el archivo JSON
    with open('personas.json', 'w') as archivo:
        json.dump(datos, archivo, indent=4)

    return '¡Los datos se han guardado correctamente!'

if __name__ == '__main__':
    app.run(debug=True)

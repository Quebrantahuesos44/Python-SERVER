print("Iniciando servidor...")

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)  # Permite que tu navegador haga peticiones sin error de CORS

class IAUsuario:
    def __init__(self, nombre_usuario):
        self.nombre = nombre_usuario
        self.memoria = self.cargar_memoria()

    def responder(self, mensaje):
        if mensaje.lower() in ["hola", "buenas"]:
            respuesta = f"¡Hola {self.nombre}!"
        else:
            respuesta = random.choice(["Interesante...", "Cuéntame más.", "¿Por qué piensas eso?"])

        self.memoria.append(mensaje)
        self.guardar_memoria()
        return respuesta

    def guardar_memoria(self):
        with open(f"{self.nombre}_memoria.json", "w") as archivo:
            json.dump(self.memoria, archivo)

    def cargar_memoria(self):
        try:
            with open(f"{self.nombre}_memoria.json", "r") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []

@app.route("/")
def home():
    return "¡Bienvenido a la API de la IA!"

@app.route("/chat", methods=["POST"])
def chat():
    datos = request.json
    nombre = datos.get("nombre", "Usuario")
    mensaje = datos.get("mensaje", "")

    usuario_ia = IAUsuario(nombre)
    respuesta = usuario_ia.responder(mensaje)

    return jsonify({
        "nombre": nombre,
        "mensaje": mensaje,
        "respuesta": respuesta
    })

if __name__ == "__main__":
    # Arranca el servidor en modo debug en el puerto 5000
    app.run(debug=True, port=5000)

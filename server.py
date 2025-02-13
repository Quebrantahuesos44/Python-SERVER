print("Iniciando servidor...")

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Permite que el navegador haga peticiones sin errores de CORS

# Cargar el modelo GPT-2
chatbot = pipeline("text-generation", model="gpt2")

@app.route("/")
def home():
    return "¡Bienvenido a la API de la IA con GPT-2!"

@app.route("/chat", methods=["POST"])
def chat():
    datos = request.json
    nombre = datos.get("nombre", "Usuario")
    mensaje = datos.get("mensaje", "")

    # Generar respuesta con GPT-2
    respuesta_generada = chatbot(mensaje, max_length=50, num_return_sequences=1)[0]["generated_text"]

    return jsonify({
        "nombre": nombre,
        "mensaje": mensaje,
        "respuesta": respuesta_generada
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

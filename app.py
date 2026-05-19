# app.py

import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

from config import (
    RECEITA_SCHEMA,
    SYSTEM_INSTRUCTION,
    PALAVRAS_BLOQUEADAS
)

# =========================
# CONFIGURAÇÃO
# =========================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

# =========================
# FILTRO DE PALAVRAS
# =========================

def contem_palavra_proibida(texto):
    texto = texto.lower()

    for categoria in PALAVRAS_BLOQUEADAS.values():
        for palavra in categoria:
            if palavra in texto:
                return True

    return False

# =========================
# GERADOR DE RECEITA
# =========================

def generate_recipe(ingredientes):

    lista_ingredientes = ", ".join(ingredientes)

    conteudo_prompt = f"""
    Crie uma receita utilizando obrigatoriamente estes ingredientes:
    {lista_ingredientes}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",

        contents=conteudo_prompt,

        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=RECEITA_SCHEMA,
        )
    )

    return response.text

# =========================
# ROTAS
# =========================

@app.route("/")
def root():

    return jsonify({
        "status": "success",
        "message": "API Gerador de Receitas funcionando!",
        "version": "1.0"
    }), 200


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    # =========================
    # VALIDAÇÕES
    # =========================

    if not data:

        return jsonify({
            "status": "error",
            "message": "Nenhum JSON enviado."
        }), 400

    if "ingredientes" not in data:

        return jsonify({
            "status": "error",
            "message": "Envie a lista de ingredientes."
        }), 400

    ingredientes = data.get("ingredientes", [])

    if not isinstance(ingredientes, list):

        return jsonify({
            "status": "error",
            "message": "Ingredientes devem ser uma lista."
        }), 400

    if len(ingredientes) < 3:

        return jsonify({
            "status": "error",
            "message": "Envie no mínimo 3 ingredientes."
        }), 400

    # =========================
    # FILTRO DE PALAVRAS
    # =========================

    for ingrediente in ingredientes:

        if contem_palavra_proibida(ingrediente):

            return jsonify({
                "status": "error",
                "message": "Conteúdo impróprio detectado."
            }), 400

    # =========================
    # GERA RECEITA
    # =========================

    try:

        receita_json_string = generate_recipe(ingredientes)

        receita_estruturada = json.loads(receita_json_string)

        return jsonify({
            "status": "success",
            "ingredientes_enviados": ingredientes,
            "dados_receita": receita_estruturada
        }), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": f"Erro ao gerar receita: {str(e)}"
        }), 500


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run()
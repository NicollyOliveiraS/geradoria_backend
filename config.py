# config.py

# =========================
# PALAVRAS BLOQUEADAS
# =========================

PALAVRAS_BLOQUEADAS = {

    "ofensivas": [
        "burro",
        "idiota",
        "imbecil",
        "otario",
        "otária",
        "babaca",
        "troxa",
        "fdp",
        "arrombado",
        "desgraçado",
        "nojento",
        "lixo",
        "besta"
    ],

    "violencia": [
        "matar",
        "assassinar",
        "arma",
        "bomba",
        "explodir",
        "faca",
        "sangue",
        "sequestrar"
    ],

    "conteudo_inadequado": [
        "drogas",
        "álcool",
        "tabaco",
        "cocô",
        "xixi",
        "pussy",
        "penis",
        "vagina",
        "picada",
        "fezes",
        "lubrificante",
        "paula mole",
        "paula dura",
        "sangue",
        "semen"

    ]
}

# =========================
# SCHEMA DA RECEITA
# =========================

RECEITA_SCHEMA = {
    "type": "OBJECT",

    "properties": {

        "nome_da_receita": {
            "type": "STRING",
            "description": "Nome da receita"
        },

        "porcoes": {
            "type": "STRING",
            "description": "Quantidade de porções"
        },

        "tempo_de_preparo": {
            "type": "STRING",
            "description": "Tempo de preparo"
        },

        "ingredientes": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            },
            "description": "Lista de ingredientes"
        },

        "modo_de_preparo": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            },
            "description": "Passo a passo"
        }
    },

    "required": [
        "nome_da_receita",
        "porcoes",
        "tempo_de_preparo",
        "ingredientes",
        "modo_de_preparo"
    ]
}

# =========================
# INSTRUÇÃO DO GEMINI
# =========================

SYSTEM_INSTRUCTION = """
Você é um Chef de Cozinha renomado.

Crie receitas deliciosas utilizando os ingredientes enviados pelo usuário.

Você pode adicionar ingredientes básicos extras
como sal, óleo e temperos.

Responda obrigatoriamente em português.

Nunca gere conteúdos ofensivos,
violentos ou inadequados.
"""
import json
import os

materiais = {}
def salvar_dados():
    with open('materiais.json', 'w', encoding='utf-8') as f:
        json.dump(materiais, f, ensure_ascii=False, indent=2)

def carregar_dados():
    global materiais
    if os.path.exists('materiais.json'):
        with open('materiais.json', 'r', encoding='utf-8') as f:
            materiais = json.load(f)
    else:
        materiais = {}


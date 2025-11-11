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
def registrar_material():
    tema = input('Tema principal: ')
    subtema = input('Subtema (deixe vazio se não tiver): ')
    titulo = input('Título do material: ')
    tipo = input('Tipo do material (artigo,video e etc.): ')
    link = input('Link ou referência: ')

    material = {
        'titulo': titulo,
        'tipo': tipo,
        'link': link
    }

    # Adiciona ao tema/subtema
    if tema not in materiais:
        materiais[tema] = {'materiais': [], 'subtemas': {}}

    if subtema:
        adicionar_subtema_recursivo(materiais[tema]['subtemas'], subtema, material) #adicionar_subtema_recursivo nome da funcao para vcs usarem ai
    else:
        materiais[tema]['materiais'].append(material)

    salvar_dados()
    print('Material registrado com sucesso :) \n')


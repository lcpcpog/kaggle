import json
import os
import unicodedata
from datetime import datetime

materiais = {}

#materiais = {
#    'tema1': {'materiais': [...], 'subtemas': {...}},
#    'tema2': {'materiais': [...], 'subtemas': {...}},
#}

def salvar_dados(caminho_arquivo, estrutura):
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(estrutura, f, indent=4, ensure_ascii=False)
    print(f'{caminho_arquivo} foi salvo com sucesso!')

def carregar_dados(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return {}

def normalizar_texto(texto):
    texto = texto.strip().lower()
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def registrar_material():
    tema = normalizar_texto(input('Tema: '))
    subtema = normalizar_texto(input('Subtema (deixe vazio se não tiver): '))
    titulo = input('Título: ')
    tipo = input('Tipo (podcast, artigo , video e etc): ')
    palavras = input('Palavras-chave (separe por vírgula se tiver mais de uma): ').split(',')
    nivel = normalizar_texto(input('Nível (básico / intermediário / avançado): '))
    data = input('Data (YYYY-MM-DD) precisa ser nesta sequência: ')
    link = input('Link: ')

    material = {
        'titulo': titulo,
        'tipo': tipo,
        'palavras_chave': [p.strip() for p in palavras],
        'nivel': nivel,
        'data': data,
        'link': link
    }

    if tema not in materiais:
        materiais[tema] = {'materiais': [], 'subtemas': {}}

    if subtema:
        adicionar_subtema(materiais[tema]['subtemas'], subtema, material)
    else:
        materiais[tema]['materiais'].append(material)

    salvar_dados('materiais.json', materiais)
    print('Material salvo =D \n')

def adicionar_subtema(subtemas, nome_subtema, material):
    if nome_subtema not in subtemas:
        subtemas[nome_subtema] = {'materiais': [], 'subtemas': {}}

    sub_subtema = input(f'O subtema "{nome_subtema}" possui outro subtema dentro dele? (s/n): ')
    if sub_subtema.lower() == 's':
        nome = input('Nome do sub-subtema: ')
        adicionar_subtema(subtemas[nome_subtema]['subtemas'], nome, material)
    else:
        subtemas[nome_subtema]['materiais'].append(material)

def exibir_temas(subtemas=None, nivel=0):
    if subtemas is None:
        subtemas = materiais

    for tema, conteudo in subtemas.items():
        print(' ' * nivel + f'- {tema}')
        for m in conteudo['materiais']:
            print('  ' * (nivel + 1) + f' {m["titulo"]} ({m["tipo"]}, {m["nivel"]}) - {m["data"]} - {m["link"]}')
        exibir_temas(conteudo['subtemas'], nivel + 1)

def consultar_personalizado():
    print('\nConsulta perzonalizad')
    tema_filtro = input('Tema (vazio = sem filtro): ').strip()
    tipo_filtro = input('Tipo (vazio = sem filtro): ').strip().lower()
    nivel_filtro = input('Nível (básico/intermediário/avançado, vazio = sem filtro): ').strip().lower()
    palavra_filtro = input('Palavra-chave (vazio = sem filtro): ').strip().lower()
    data_inicio = input('Data inicial (YYYY-MM-DD, vazio = sem filtro): ').strip()
    data_fim = input('Data final (YYYY-MM-DD, vazio = sem filtro): ').strip()

    resultados = []

    def buscar(subtemas):
        for nome, conteudo in subtemas.items():
            for m in conteudo['materiais']:
                if tema_filtro and tema_filtro.lower() not in nome.lower():
                    continue
                if tipo_filtro and tipo_filtro != m['tipo'].lower():
                    continue
                if nivel_filtro and nivel_filtro != m['nivel'].lower():
                    continue
                if palavra_filtro and not any(palavra_filtro in p.lower() for p in m['palavras_chave']):
                    continue
                if data_inicio and m['data'] < data_inicio:
                    continue
                if data_fim and m['data'] > data_fim:
                    continue
                resultados.append((nome, m))
            buscar(conteudo['subtemas'])

    buscar(materiais)

    if resultados:
        print('\nResultados:')
        for nome, m in resultados:
            print(f'Tema: {nome} | {m["titulo"]} ({m["tipo"]}, {m["nivel"]}) - {m["data"]} - {m['link']}')
    else:
        print('Nenhum resultado encontrado.\n')

def gerar_relatorio():
    print('\n=== Relatório ===')
    total_tema = {}
    total_tipo = {}
    datas = []

    def contar(subtemas):
        total_local = 0
        for nome, conteudo in subtemas.items():
            qtd_materiais = len(conteudo['materiais'])

            qtd_sub = contar(conteudo['subtemas'])
            qtd_materiais += qtd_sub

            total_tema[nome] = qtd_materiais
            for m in conteudo['materiais']:
                total_tipo[m['tipo']] = total_tipo.get(m['tipo'], 0) + 1
                if m['data']:
                    datas.append(m['data'])

            total_local += qtd_materiais
        return total_local
    
    contar(materiais)

    print('\nMateriais por Tema:')
    for tema, qtd in total_tema.items():
        print(f'- {tema}: {qtd} materiais')

    print('\nMateriais por Tipo:')
    for tipo, qtd in total_tipo.items():
        print(f'- {tipo}: {qtd}')

    if datas:
        anos = [int(d.split('-')[0]) for d in datas]
        media = len(datas) / len(set(anos))
        print(f'\nMédia de materiais por ano: {media:.2f}')
    print()

def menu():
    global materiais
    materiais = carregar_dados('materiais.json')

    while True:
        print('Sistema de Gerenciamento de Estudos :')
        print('1 - Registrar novo material')
        print('2 - Exibir todos os temas')
        print('3 - Busca personalizada')
        print('4 - Relatórios')
        print('0 - Sair')

        opcao = input('Escolha uma opção: ')
        print()

        if opcao == '1':
            registrar_material()
        elif opcao == '2':
            exibir_temas()
            print()
        elif opcao == '3':
            consultar_personalizado()
        elif opcao == '4':
            gerar_relatorio()
        elif opcao == '0':
            print('falou =D')
            break
        else:
            print('Opção inválida, tente novamente.\n')

menu()

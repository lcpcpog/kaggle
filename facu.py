import json
import os
from datetime import datetime

movimentacoes = []


def salvar_movimentacoes():
    with open('movimentacoes.json', 'w', encoding='utf-8') as f:
        json.dump(movimentacoes, f, ensure_ascii=False, indent=2)

def carregar_movimentacoes():
    global movimentacoes
    if os.path.exists('movimentacoes.json'):
        with open('movimentacoes.json', 'r', encoding='utf-8') as f:
            movimentacoes = json.load(f)
    else:
        movimentacoes = []

# Registrar movimentação
def registrar_movimentacao():
    try:
        descricao = input('Descrição: ')
        while True:
            try:
                valor = float(input('Valor (positivo = receita, negativo = despesa): '))
                break
            except ValueError:
                print('Digite apenas números, exemplo: 1000 ou -250.')

        categoria = input('Categoria (ex: alimentação, transporte, salário...): ')
        data = input('Data (ex: 2025-10-21) [vazio = hoje]: ')
        if not data:
            data = datetime.today().strftime('%Y-%m-%d')

        movimentacao = {
            'descricao': descricao,
            'valor': valor,
            'categoria': categoria,
            'data': data
        }
        movimentacoes.append(movimentacao)
        salvar_movimentacoes()  
        print('Movimentação registrada com sucesso!\n')

    except Exception as e:
        print(f'Ocorreu um erro: {e}\n')

# Mostrar todas as movimentações
def mostrar_movimentacoes():
    if not movimentacoes:
        print('Nenhuma movimentação registrada.\n')
        return

    print('=== Movimentações Registradas ===')
    for i, mov in enumerate(movimentacoes, start=1):
        print(f'{i}. {mov["data"]} - {mov["descricao"]} ({mov["categoria"]}): R$ {mov["valor"]:.2f}')
    print()

# Calcular saldo 
def calcular_saldo():
    saldo = sum(mov['valor'] for mov in movimentacoes)
    print(f'Saldo atual: R$ {saldo:.2f}\n')

# Relatório por categoria
def relatorio_por_categoria():
    if not movimentacoes:
        print('Nenhuma movimentação registrada.\n')
        return

    categorias = {}
    for mov in movimentacoes:
        cat = mov['categoria']
        categorias[cat] = categorias.get(cat, 0) + mov['valor']

    print('=== Relatório por Categoria ===')
    for cat, total in categorias.items():
        print(f'{cat}: R$ {total:.2f}')
    print()

# Consultas personalizadas
def consultar_movimentacoes():
    if not movimentacoes:
        print('Nenhuma movimentação registrada.\n')
        return

    
    data_inicio = input('Data inicial (YYYY-MM-DD) [vazio = sem filtro]: ')
    data_fim = input('Data final (YYYY-MM-DD) [vazio = sem filtro]: ')
    categorias_input = input('Categorias separadas por vírgula [vazio = todas]: ')

    # cria lista de categorias se o usuário digitar algo
    categorias = [c.strip() for c in categorias_input.split(',')] if categorias_input else None

    encontrado = False  

    print('\n=== Resultados da Consulta ===')
    for mov in movimentacoes:
        if (not data_inicio or mov['data'] >= data_inicio) and \
           (not data_fim or mov['data'] <= data_fim) and \
           (not categorias or mov['categoria'] in categorias):
            print(f'{mov["data"]} - {mov["descricao"]} ({mov["categoria"]}): R$ {mov["valor"]:.2f}')
            encontrado = True

    if not encontrado:
        print('Nenhuma movimentação encontrada.')

    print()

# Estatísticas financeiras
def estatisticas():
    if not movimentacoes:
        print('Nenhuma movimentação registrada.\n')
        return

    receitas = [mov['valor'] for mov in movimentacoes if mov['valor'] > 0]
    despesas = [mov['valor'] for mov in movimentacoes if mov['valor'] < 0]

    media_receita = sum(receitas)/len(receitas) if receitas else 0
    media_despesa = sum(despesas)/len(despesas) if despesas else 0

    print('=== Estatísticas Financeiras ===')
    print(f'Média de receitas: R$ {media_receita:.2f}')
    print(f'Média de despesas: R$ {media_despesa:.2f}\n')

# Menu principal 
def menu():
    carregar_movimentacoes()
    while True:
        print('=== Sistema de Planejamento Financeiro ===')
        print('1 - Registrar movimentação')
        print('2 - Mostrar todas as movimentações')
        print('3 - Calcular saldo')
        print('4 - Relatório por categoria')
        print('5 - Consultar movimentações (filtro)')
        print('6 - Estatísticas financeiras')
        print('0 - Sair')
        opcao = input('Escolha uma opção: ')

        print()
        if opcao == '1':
            registrar_movimentacao()
        elif opcao == '2':
            mostrar_movimentacoes()
        elif opcao == '3':
            calcular_saldo()
        elif opcao == '4':
            relatorio_por_categoria()
        elif opcao == '5':
            consultar_movimentacoes()
        elif opcao == '6':
            estatisticas()
        elif opcao == '0':
            print('Saindo do sistema. Até logo!')
            break
        else:
            print('Opção inválida.\n')

    

menu()

#movimentacoes = [
#    {'descricao': 'Salário', 'valor': 3000, 'categoria': 'Trabalho', 'data': '2025-10-20'},
#    {'descricao': 'Supermercado', 'valor': -250, 'categoria': 'Alimentação', 'data': '2025-10-21'}
#]

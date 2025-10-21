movimentacoes = []

# registrar uma nova movimentação
def registrar_movimentacao():
    descricao = input("Descrição: ")
    valor = float(input("Valor (positivo = receita, negativo = despesa): "))
    categoria = input("Categoria (ex: alimentação, transporte, salário...): ")
    data = input("Data (ex: 2025-10-21): ")
    
    movimentacao = {
        "descricao": descricao,
        "valor": valor,
        "categoria": categoria,
        "data": data
    }
    movimentacoes.append(movimentacao)
    print("Movimentação registrada com sucesso!\n")

# mostrar todas as movimentações
def mostrar_movimentacoes():
    if not movimentacoes:
        print("Nenhuma movimentação registrada.\n")
        return
    
    for i, mov in enumerate(movimentacoes, start=1):
        print(f"{i}. {mov['data']} - {mov['descricao']} ({mov['categoria']}): R$ {mov['valor']:.2f}")
    print()

# calcular o saldo atual
def calcular_saldo():
    saldo = sum(mov["valor"] for mov in movimentacoes)
    print(f"Saldo atual: R$ {saldo:.2f}\n")

# gerar relatório por categoria
def relatorio_por_categoria():
    if not movimentacoes:
        print("Nenhuma movimentação registrada.\n")
        return
    
    categorias = {}
    for mov in movimentacoes:
        cat = mov["categoria"]
        categorias[cat] = categorias.get(cat, 0) + mov["valor"]
    
    print("=== Relatório por Categoria ===")
    for cat, total in categorias.items():
        print(f"{cat}: R$ {total:.2f}")
    print()

# mostrar estatísticas simples
def estatisticas():
    if not movimentacoes:
        print("Nenhuma movimentação registrada.\n")
        return
    
    receitas = [mov["valor"] for mov in movimentacoes if mov["valor"] > 0]
    despesas = [mov["valor"] for mov in movimentacoes if mov["valor"] < 0]
    
    media_receita = sum(receitas) / len(receitas) if receitas else 0
    media_despesa = sum(despesas) / len(despesas) if despesas else 0
    
    print("=== Estatísticas Financeiras ===")
    print(f"Média de receitas: R$ {media_receita:.2f}")
    print(f"Média de despesas: R$ {media_despesa:.2f}\n")

# Menu principal
def menu():
    while True:
        print("=== Sistema de Planejamento Financeiro ===")
        print("1 - Registrar movimentação")
        print("2 - Mostrar movimentações")
        print("3 - Calcular saldo")
        print("4 - Relatório por categoria")
        print("5 - Estatísticas financeiras")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")
        print()
        
        if opcao == "1":
            registrar_movimentacao()
        elif opcao == "2":
            mostrar_movimentacoes()
        elif opcao == "3":
            calcular_saldo()
        elif opcao == "4":
            relatorio_por_categoria()
        elif opcao == "5":
            estatisticas()
        elif opcao == "0":
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

menu()

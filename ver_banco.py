import sqlite3

def visualizar_banco():
    conexao = sqlite3.connect('banco_notas.db')
    cursor = conexao.cursor()

    print("\n📦 --- PRODUTOS CADASTRADOS --- 📦")

    cursor.execute("SELECT nota_fiscal_id, descricao_produto, quantidade_produto, valor_produto FROM produtos")
    produtos = cursor.fetchall()

    for produto in produtos:
        nota_fiscal_id, descricao_produto, quantidade_produto, valor_produto = produto
        print(f"Nota Fiscal ID: {nota_fiscal_id} | Produto: {descricao_produto} | Quantidade: {quantidade_produto} | Valor Unitário: {valor_produto}")  
    
    print("-" * 50)
    conexao.close()

if __name__ == "__main__":
    visualizar_banco()  

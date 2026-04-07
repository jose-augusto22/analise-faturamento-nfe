import sqlite3

def configurar_banco():
    #conecta ao banco de dados (ou cria se nao existir) e cria a tabela de notas fiscais
    conexao = sqlite3.connect('banco_notas.db')
    cursor = conexao.cursor()

    #cria a tabela apenas com o cabeçalho, sem os dados
    cursor.execute ('''
                CREATE TABLE IF NOT EXISTS notas_fiscais (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                chave_acesso TEXT UNIQUE,
                nome_emitente TEXT, 
                cnpj_emitente TEXT,
                nome_destinatario TEXT,
                cnpj_destinatario TEXT
                )
             ''')
    
    #cria a tabela de produtos, com uma chave estrangeira para a tabela de notas fiscais
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nota_fiscal_id INTEGER,
                descricao_produto TEXT,
                quantidade_produto REAL,
                valor_produto REAL,
                FOREIGN KEY (nota_fiscal_id) REFERENCES notas_fiscais(id)
                )
        ''')

    #salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()
    print("Banco de dados configurado com sucesso!")

if __name__ == "__main__":
    configurar_banco()

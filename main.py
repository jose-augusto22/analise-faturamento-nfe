
import xml.etree.ElementTree as ET
import sqlite3

def extrair_e_salvar_nfe(caminho_arquivo):

    ns = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe'
    }

    try:
        #1. Conectar ao banco de dados
        conexao = sqlite3.connect('banco_notas.db')
        cursor = conexao.cursor()

        #2. Carregar o arquivo XML
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()
        
        #3. Extrair informações do emitente
        emitente = root.find('.//nfe:emit', ns)
        nome_emitente = emitente.find('nfe:xNome', ns).text if emitente is not None else None
        cnpj_emitente = emitente.find('nfe:CNPJ', ns).text if emitente is not None else None

        #4. Extrair informações do destinatário
        destinatario = root.find('.//nfe:dest', ns)
        nome_destinatario = destinatario.find('nfe:xNome', ns).text if destinatario is not None else None
        cnpj_destinatario = destinatario.find('nfe:CNPJ', ns).text

        #5. Salvar o Cabeçalho da nota fiscal no banco de dados
        cursor.execute('''
            INSERT INTO notas_fiscais (nome_emitente, cnpj_emitente, nome_destinatario, cnpj_destinatario)
            VALUES (?, ?, ?, ?)
        ''', (nome_emitente, cnpj_emitente, nome_destinatario, cnpj_destinatario))

        #6. Obter o ID da nota fiscal recém inserida
        nota_fiscal_id = cursor.lastrowid

        #7. Extrair e salvar os produtos da nota fiscal
        produtos = root.findall('.//nfe:det', ns)
        for produto in produtos:
            descricao_produto = produto.find('.//nfe:xProd', ns).text
            quantidade_produto = float(produto.find('.//nfe:qCom', ns).text)
            valor_produto = float(produto.find('.//nfe:vUnCom', ns).text)

            cursor.execute('''
                INSERT INTO produtos (nota_fiscal_id, descricao_produto, quantidade_produto, valor_produto)
                VALUES (?, ?, ?, ?)
            ''', (nota_fiscal_id, descricao_produto, quantidade_produto, valor_produto))

        #8 Confirmar as alterações e fechar a conexão
        conexao.commit()
        conexao.close()
        print(f"✅ Nota fiscal '{nome_emitente}' salva com sucesso!")

    except FileNotFoundError:
        print("❌ Arquivo XML não encontrado. Verifique o caminho e tente novamente.")
    except Exception as e:
        print(f"❌ Erro ao processar o arquivo ou salvar no banco de dados: {e}")

# Executa a função passando o nosso XML de teste
if __name__ == "__main__":
    extrair_e_salvar_nfe('nfe_test.xml')

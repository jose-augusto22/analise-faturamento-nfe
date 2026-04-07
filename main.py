
import xml.etree.ElementTree as ET
import sqlite3
import os

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
        
        nome_arquivo = os.path.basename(caminho_arquivo)
        print(f"✅ Arquivo '{nome_arquivo}' de '{nome_emitente}' para '{nome_destinatario}' processado e salvo com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao processar o arquivo: '{caminho_arquivo}' ou salvar no banco de dados: {e}")

def processar_lotes(pasta_entradas):
    #1. Verificar se a pasta de entrada existe
    if not os.path.exists(pasta_entradas):
        print(f"❌ A pasta '{pasta_entradas}' não existe. criando a pasta...")
        os.makedirs(pasta_entradas)
        print(f"📁 Pasta '{pasta_entradas}' criada. Por favor, adicione os arquivos XML de notas fiscais e execute novamente.")
        return
    #2. Buscar todos os arquivos XML na pasta de entrada
    arquivos_xml = [f for f in os.listdir(pasta_entradas) if f.endswith('.xml')]

    if not arquivos_xml:
        print(f"📂 A pasta '{pasta_entradas}' está vazia. Por favor, adicione os arquivos XML de notas fiscais e execute novamente.")
        return

    print(f"📂 Encontrados {len(arquivos_xml)} arquivos XML na pasta '{pasta_entradas}'. Iniciando processamento...")

    #3. Faz o loop para processar cada arquivo XML encontrado
    for arquivo in arquivos_xml:
        caminho_completo = os.path.join(pasta_entradas, arquivo)
        extrair_e_salvar_nfe(caminho_completo)

    print("-" * 50)
    print("✅ Processamento de lote concluído. Todos os arquivos foram processados e salvos no banco de dados.")

# Ponto de entrada do programa
if __name__ == "__main__":
    processar_lotes('entradas')

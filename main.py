
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

        # A chave de acesso pode ser encontrada no atributo 'Id' do elemento 'infNFe'
        infNFe = root.find('.//nfe:infNFe', ns)
        chave_acesso = infNFe.attrib['Id'][3:] if infNFe is not None else "CHAVE_NAO_ENCONTRADA"

        #3Extrair a data de emissão ( pegando só os 10 primeiros caracteres)
        ide = root.find('.//nfe:ide', ns)
        data_bruta = ""
        if ide is not None:
            tag_data = ide.find('nfe:dhEmi', ns)
            if tag_data is not None:
                tag_data = ide.find('nfe:dEmi', ns) #cobre notas antigas

            data_bruta = tag_data.text if tag_data is not None else None
        data_emissao = data_bruta[:10] if data_bruta else None

        #4. Extrair o valor total da nota fiscal
        total = root.find('.//nfe:total', ns)
        valor_total = 0.0
        if total is not None:
            tag_valor = total.find('nfe:vNF', ns)
            if tag_valor is not None:
                valor_total = float(tag_valor.text)
            else:
                print(f"⚠️ Valor total não encontrado no arquivo '{os.path.basename(caminho_arquivo)}'. Definindo como 0.0.")


        #5. Extrair informações do emitente
        emitente = root.find('.//nfe:emit', ns)
        nome_emitente = ""
        cnpj_emitente = ""
        if emitente is not None:
            tag_nome = emitente.find('nfe:xNome', ns)
            tag_cnpj = emitente.find('nfe:CNPJ', ns)
            nome_emitente = tag_nome.text if tag_nome is not None else None
            cnpj_emitente = tag_cnpj.text if tag_cnpj is not None else None
        


        #6. Extrair informações do destinatário
        destinatario = root.find('.//nfe:dest', ns)
        nome_destinatario = ""
        cnpj_destinatario = "" 
        if destinatario is not None:
            tag_nome = destinatario.find('nfe:xNome', ns)
            nome_destinatario = tag_nome.text if tag_nome is not None else ""
            tag_cnpj = destinatario.find('nfe:CNPJ', ns)
            tag_cpf = destinatario.find('nfe:CPF', ns)
            if tag_cnpj is not None:
                cnpj_destinatario = tag_cnpj.text
            elif tag_cpf is not None:
                cnpj_destinatario = tag_cpf.text
        
        try:
            #. Salvar o Cabeçalho da nota fiscal no banco de dados
            cursor.execute('''
                INSERT INTO notas_fiscais (chave_acesso, nome_emitente, cnpj_emitente, nome_destinatario, cnpj_destinatario, data_emissao, valor_total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (chave_acesso, nome_emitente, cnpj_emitente, nome_destinatario, cnpj_destinatario, data_emissao, valor_total))

            #6. Obter o ID da nota fiscal recém inserida
            nota_fiscal_id = cursor.lastrowid

            #7. Extrai e Salva os Produtos na tabela 'produtos' com o ID da nota
            produtos = root.findall('.//nfe:det', ns)
            for produto in produtos:
                descricao_produto = produto.find('nfe:prod/nfe:xProd', ns).text
                quantidade_produto = float(produto.find('nfe:prod/nfe:qCom', ns).text)
                valor_produto = float(produto.find('nfe:prod/nfe:vUnCom', ns).text)

                #teste de inserção do produto
                print(f"  -> Lendo produto do XML: {descricao_produto} | Qtd: {quantidade_produto}")
                

                cursor.execute('''
                    INSERT INTO produtos (nota_fiscal_id, descricao_produto, quantidade_produto, valor_produto)
                    VALUES (?, ?, ?, ?)
                ''', (nota_fiscal_id, descricao_produto, quantidade_produto, valor_produto))

            #8 Confirmar as alterações e fechar a conexão
            conexao.commit()
            print(f"✅ sucesso: '{os.path.basename(caminho_arquivo)}' processado e salvo no banco de dados.")

        except sqlite3.IntegrityError:
            print(f"⚠️ A nota fiscal com chave de acesso '{chave_acesso}' já existe no banco de dados. Pulando o arquivo '{os.path.basename(caminho_arquivo)}'.")
        
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
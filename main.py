
import xml.etree.ElementTree as ET

def extrair_dados_nfe(caminho_arquivo):

    ns = {
        'nfe': 'http://www.portalfiscal.inf.br/nfe'
    }

    try:
        #carregar o arquivo XML
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()

        # Extrair informações do emitente
        emitente = root.find('.//nfe:emit', ns)
        if emitente is not None:
            nome_emitente = emitente.find('nfe:xNome', ns).text
            cnpj_emitente = emitente.find('nfe:CNPJ', ns).text
            print(f'Emitente: {nome_emitente} - CNPJ: {cnpj_emitente}')

        # Extrair informações do destinatário
        destinatario = root.find('.//nfe:dest', ns)
        if destinatario is not None:
            nome_destinatario = destinatario.find('nfe:xNome', ns).text
            cnpj_destinatario = destinatario.find('nfe:CNPJ', ns).text
            print(f'Destinatário: {nome_destinatario} - CNPJ: {cnpj_destinatario}')

            # Extrair informações dos produtos
            produtos = root.findall('.//nfe:det', ns)
            for produto in produtos:
                descricao_produto = produto.find('nfe:prod/nfe:xProd', ns).text
                quantidade_produto = produto.find('nfe:prod/nfe:qCom', ns).text
                valor_produto = produto.find('nfe:prod/nfe:vUnCom', ns).text
                print(f'Produto: {descricao_produto} - Quantidade: {quantidade_produto} - Valor Unitário: {valor_produto}')
    
    except FileNotFoundError:
        print(f'Arquivo {caminho_arquivo} não encontrado.')
    except Exception as e:
        print(f'Erro ao processar o arquivo: {e}')

extrair_dados_nfe('nfe_test.xml')
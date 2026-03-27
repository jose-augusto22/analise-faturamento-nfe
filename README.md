# 📊 Analisador e Gestor de Faturamento NFe (MVP)

## 🎯 O Problema

Rotinas de faturamento frequentemente envolvem a recepção de dezenas ou centenas de Notas Fiscais Eletrônicas (NFe) em formato XML. A extração manual ou dependente de sistemas legados para compilar dados de fornecedores, produtos e valores pode ser lenta e sujeita a erros, dificultando a análise rápida de métricas financeiras.

## 💡 A Solução

Este projeto é um motor de automação desenvolvido para ler, extrair e estruturar dados de arquivos XML de NFe em lote. O objetivo final é alimentar um dashboard gerencial para análise de faturamento, otimizando o tempo do setor administrativo.

## 🛠️ Tecnologias Utilizadas (Fase 1)

- **Linguagem:** Python 3.13
- **Manipulação de Dados:** Biblioteca nativa `xml.etree.ElementTree`
- **Arquitetura:** Script modular focado na extração de namespaces padrão do Portal Fiscal (NFe 4.00).

## 🚀 Como testar localmente

1. Clone este repositório.
2. Certifique-se de ter o Python instalado.
3. Execute o comando no terminal: `python main.py`
4. O sistema lerá o arquivo `nfe_test.xml` e exibirá no terminal os dados estruturados do emitente, destinatário e itens faturados.

---

_Projeto em desenvolvimento ativo. Próximos passos incluem persistência de dados em banco SQLite e construção de API com Django._

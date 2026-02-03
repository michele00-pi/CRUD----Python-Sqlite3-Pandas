import sqlite3 as sql
import pandas as pd 
from modulo import *

conexao = sql.connect("crud_cpf.db")
cursor = conexao.cursor()

#cursor.execute("CREATE TABLE cadastrados (nome varchar(50), cpf char(11) PRIMARY KEY, email varchar(60), cep char(8))")
colunas_tabela = cursor.execute("PRAGMA TABLE_INFO('cadastrados')")
colunas_tabela = cursor.fetchall()

lista_colunas_db = []
for coluna in colunas_tabela:
    lista_colunas_db.append(coluna[1]) #Na posição 1 se encontra o nome da tabela, as demais são informações sobre ela

while True:

    df_banco = pd.read_sql_query("SELECT * FROM cadastrados", conexao)#1°Comando SQL, 2° Banco onde será executado esse comando --> guarda a tabela no df
    resposta = input("1-Cadastrar\n2-Exibir\n3-Editar\n4-Excluir\n5-Exportar dados\n6-Importar dados\n7-Inserir tabela no banco de dados\n8-Encerrar\nR:")

    match resposta:

        case "1":
            nome = input("Digite seu nome: ")
            cpf = input("Digite seu CPF: ")
            email = input("Digite seu email: ")
            cep = input("Digite seu CEP: ")
            dados = cadastrar(nome,cpf,email,cep,conexao,cursor)
            validar = dados.validar_cpf()

            dados.cad_cpf(validar)

        case "2":
            print(df_banco)

        case "3":
            pedir_cpf = input("Digite o cpf do cadastro que deseja alterar: ")
            dados = modificar(pedir_cpf,conexao,cursor)
            dados.editar()

        case "4":
            cpf_excluir = input("Digite o CPF do cadastro que deseja exlcuir: ")
            dados = modificar(cpf_excluir,conexao,cursor)
            dados.excluir()

        case "5":
            tipo_exportar = input("Deseja exportar para qual formato?(xlsx,csv,json,xml): ")
            nomear_arquivo = input("Escreva o nome do arquivo: ")
            dados_transacoes_export = transacoes(df_banco,None,tipo_exportar,nomear_arquivo)
            dados_transacoes_export.exportar()

        case "6":
            caminho = input("Digite o caminho do arquivo: ")
            tipo = input("Digite o formato do arquivo(xlsx,csv,json,xml): ")
            nomear = input("Nomeie o arquivo: ")
            dados_transacoes_import = transacoes(None,caminho,tipo,nomear)
            dados_transacoes_import.importar_arquivo()

        case "7":
            nomea_arquivo = input("Digite o nome do arquivo: ")
            extensao = input("Digite a extensao do arquivo(xlsx,csv,json,xml): ")
            inserir_tabela = inserir_dados_importados(lista_colunas_db,nomea_arquivo,extensao,conexao,cursor)
            inserir_tabela.leitura_insercao()

        case "8":
            break
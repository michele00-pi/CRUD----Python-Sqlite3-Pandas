"""
--Documentação--

--> tabela 'cadastrados' com as entidades: nome, cpf(PRIMARY KEY), email, cep

módulos, classes e métodos utilizados:
sqlite3 --> banco de dados

    conexao = sql.connect() --> conecta ao banco de dados
    cursor = conexao.cursor() --> permite comandos SQL no banco de dados
    cursor.execute() --> Comandos para manipulação do banco
    cursor.execute("INSERT OR IGNORE INTO cadastrados ") --> Caso um dado for duplicado(primary key), não é inserido na tabela
    cursor.executemany() --> O executemany executa o mesmo comando SQL repetidas vezes, uma para cada tupla dentro da lista
    cursor.fetchone() --> Recupera um dado(nesse caso foi utlizado para veificar a existencia de um dado no sistema) retorna None caso não exista
    conexao.commit() --> salvar alterações feitas no banco 

pandas --> tabelas

    dataframe.to_excel() --> Baixa o dataframe no formato de excel(ou demais extensões), na pasta local
    df_import = pd.read_excel() --> Lê o arquivo excel(ou demais extensões) e armazena a tabela no df_import(dataframe)

class cadastrar() --> Responsável por cadastrar dados na tabela 'cadastrados'

    def __init__
    -->parâmetros
        nome -- entidade
        cpf -- entidade
        email -- entidade
        cep -- entidade
        conexao -- conexao com banco de dados
        cursor -- comandos sql
    
    def validar_cpf
    --> Aplica a fórmula dos ultimos dois dígitos do CPF, retorna True se condizer com os dígitos do cpf inserido no __init__

    def cad_cpf
    -->Pega o valor retornado por validar_cpf
        -->case True
             -->verifica se o cpf ja existe na tabela, caso não, insere na tabela. Caso sim 'CPF já cadastrado'
        -->case False
             -->cpf inválido
    
class modificar() --> Responsável por alterar os dados da tabela 'cadastrados'

    def __init__
    -->parâmetros
        pedir_cpf -- cpf do cadastro que será alterado
        conexao -- conexao com banco de dados
        cursor -- comandos sql

    def editar
    --> Procura na tabela o 'pedir_cpf', retorna None caso não encontrar
        -->case None
            --> 'CPF não existe no sistema'
        -->case _
            --> Pede novo email e novo cep
            --> insere na linha onde a entidade = 'pedir_cpf'
    
    def excluir
    --> Procura na tabela o 'pedir_cpf', retorna None caso não encontrar
        -->case None
            --> 'CPF não existe no sistema'
        -->case _
            --> Exclui todos os dados onde o cpf = 'pedir_cpf'

    
class transacoes -- Responsável por Exportar a tabela do banco de dados para outras extensões(xlsx,csv,json,xml)
                 -- Responsável por Importar tabelas e baixa-las na pasta local
    
    def __init__
    -->parâmetros 
        dataframe -- pega o dataframe da tabela do banco de dados
        caminho -- local do arquivo para a leitura e importação
        tipo -- extensão(.xlsx, .csv, .json, .xml)
        nome_arquivo -- Nomeia o arquivo
    
    def exportar
    -->case "xlsx","csv","json","xml" --> tipo = 'xlsx'...
        --> adicona a extensão no nome do arquivo
        --> baixa a tabela no formato inserido na pasta local
    -->case _
        --> 'opção inválida'
    
    def importar_arquivo
    -->case "xlsx","csv","json","xml" --> tipo = 'xlsx'...
        -->Try 
            --> Procura no 'caminho' o arquivo, lê e armazena no dataframe
            --> adicona a extensão no nome do arquivo
            --> baixa a tabela no formato inserido na pasta local
        -->except Exception
            --> Exibe erro e sua causa

class inserir_dados_importados --Responsável por ler tabelas de arquivos(.xlsx,.csv,.json,.xml)
                               --Inserir dados da tabela lida na tabela do banco de dados

    def __init__
    -->parâmetros
    conexao -- conexao com banco de dados
    cursor -- comandos sql
    lista_colunas_db -- Nome das colunas do banco de dados
    nome_arquivo -- Nome do arquivo que será lido e inserido na tabela do banco de dados
    extensao -- Extensão desse arquivo

    def leitura_insercao
    -->verifica se a 'extensao' é uma das opções oferecidas , caso não 'Extensão inválida'
        -->case "xlsx","csv","json","xml" -- extensao = "xlsx"... todos seguem a mesma lógica
            -->Lê o arquivo e armazena a tabela em um dataframe
            -->Armazena o nome das entidades em uma lista, e transforma em set para comparação
            --> Compara as colunas do arquivo lido com as colunas do banco de dados, caso não 'Estrutura de dados incompatível'
                -->Armazena os dados da cada linha em uma lista de tuplas
                -->Insere esses valores na tabela do banco de dados(caso houve duplicata da chave primária , ignora a linha)
                
"""

import pandas as pd

class cadastrar:

    def __init__(self,nome,cpf,email,cep,conexao,cursor):

        self.conexao = conexao
        self.cursor = cursor
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.cep = cep

    def validar_cpf(self):

        if len(self.cpf) == 11 and self.cpf.isdigit() == True:
            soma1 = (int(self.cpf[0]) * 10) +  (int(self.cpf[1]) * 9) + (int(self.cpf[2]) * 8) + (int(self.cpf[3]) * 7) + (int(self.cpf[4]) * 6) + (int(self.cpf[5]) * 5) + (int(self.cpf[6]) * 4) + (int(self.cpf[7]) * 3) + (int(self.cpf[8]) * 2)
            resto1 = soma1 % 11

            if resto1 < 2:
                dv1 = 0

            else:
                dv1 = 11 - resto1

            soma2 = (int(self.cpf[0]) * 11) + (int(self.cpf[1]) * 10) + (int(self.cpf[2]) * 9) + (int(self.cpf[3]) * 8) + (int(self.cpf[4]) * 7) + (int(self.cpf[5]) * 6 ) + (int(self.cpf[6]) * 5) + (int(self.cpf[7]) * 4) + (int(self.cpf[8]) * 3) + (dv1 * 2)
            resto2 = soma2 % 11

            if resto2 < 2:
                dv2 = 0

            else:
                dv2 = 11 - resto2

            if int(self.cpf[9]) == dv1 and int(self.cpf[10]) == dv2:
                return True
                
            else:
                return False
                
        else:
            print("Formato de CPF inválido!")

    def cad_cpf(self,bool):
        
        match bool:

            case True:
                self.cursor.execute("SELECT cpf FROM cadastrados WHERE cpf = ?", (self.cpf,))
                conferir_exis_p_cadastro = self.cursor.fetchone()

                if conferir_exis_p_cadastro == None:
                    self.cursor.execute("INSERT INTO cadastrados VALUES(?,?,?,?)", (self.nome, self.cpf, self.email, self.cep))
                    self.conexao.commit()
                    print("Dados cadastrados")
                
                else:
                    print(" CPF já cadastrado no sistema")

            case False:
                print("CPF inválido!")
    
class modificar:

    def __init__(self,pedir_cpf,conexao,cursor):

        self.conexao = conexao
        self.cursor = cursor
        self.pedir_cpf = pedir_cpf

    def editar(self):

        self.cursor.execute("SELECT cpf FROM cadastrados WHERE cpf = ?", (self.pedir_cpf,))
        exitir_no_banco = self.cursor.fetchone()

        match exitir_no_banco:

            case None:
                print("Esse CPF não existe no sistema")

            case _:
                novo_email = input("Digite o novo email: ")
                novo_cep = input("Digite o novo CEP: ")

                self.cursor.execute("UPDATE cadastrados SET email = ?, cep = ? WHERE cpf = ?",(novo_email,novo_cep,self.pedir_cpf))
                self.conexao.commit()
                print("Dados alterados com sucesso!")

    def excluir(self):

        self.cursor.execute("SELECT cpf FROM cadastrados WHERE cpf = ?", (self.pedir_cpf,))
        exitir_no_banco = self.cursor.fetchone()

        match exitir_no_banco:

            case None:
                print("Esse CPF não existe no sistema")

            case _:
                self.cursor.execute("DELETE FROM cadastrados WHERE cpf = ?", (self.pedir_cpf,))
                self.conexao.commit()
                print("Dados excluidos com sucesso")
                
class transacoes:

    def __init__(self,dataframe,caminho,tipo,nome_arquivo):
        
        self.dataframe = dataframe 
        self.caminho = caminho
        self.tipo = tipo
        self.nome_arquivo = nome_arquivo

    def exportar(self):

        match self.tipo:

            case "xlsx":
                nome_c_extensao = self.nome_arquivo + ".xlsx"
                self.dataframe.to_excel(nome_c_extensao)
                print("Dados exportados no formato ",self.tipo,", com sucesso!")


            case "csv":
                nome_c_extensao = self.nome_arquivo + ".csv"
                self.dataframe.to_csv(nome_c_extensao)
                print("Dados exportados no formato ",self.tipo,", com sucesso!")

            case "json":
                nome_c_extensao = self.nome_arquivo + ".json"
                self.dataframe.to_json(nome_c_extensao)
                print("Dados exportados no formato ",self.tipo,", com sucesso!")

            case "xml":
                nome_c_extensao = self.nome_arquivo + ".xml"
                self.dataframe.to_xml(nome_c_extensao)
                print("Dados exportados no formato ",self.tipo,", com sucesso!")

            case _:

                print("Opção inválida")

    def importar_arquivo(self):

        match self.tipo:

            case "xlsx":

                try:

                    df_import = pd.read_excel(self.caminho)
                    nome_c_extensao = self.nome_arquivo + ".xlsx"
                    df_import.to_excel(nome_c_extensao)
                    print("Dados importados no formato ",self.tipo,", com sucesso!")
                    
                except Exception as e:

                    print("Erro de inserção no formato do caminho " ,e )

            case "csv":

                try:

                    df_import = pd.read_csv(self.caminho)
                    nome_c_extensao = self.nome_arquivo + ".csv"
                    df_import.to_csv(nome_c_extensao)
                    print("Dados importados no formato ",self.tipo,", com sucesso!")

                except Exception as e:

                    print("Erro de inserção no formato do caminho " ,e )

            case "json":

                try:

                    df_import = pd.read_json(self.caminho)
                    nome_c_extensao = self.nome_arquivo + ".json"
                    df_import.to_json(nome_c_extensao) 
                    print("Dados importados no formato ",self.tipo,", com sucesso!")

                except Exception as e:

                    print("Erro de inserção no formato do caminho " ,e )

            case "xml":

                try:

                    df_import = pd.read_xml(self.caminho)
                    nome_c_extensao = self.nome_arquivo + ".xml"
                    df_import.to_xml(nome_c_extensao)
                    print("Dados importados no formato ",self.tipo,", com sucesso!")

                except Exception as e:

                    print("Erro de inserção no formato do caminho " ,e )
            
            case _:

                print("Extensão inválida!")

class inserir_dados_importados:

    def __init__(self, lista_colunas_db,nome_arquivo,extensao,conexao,cursor):

        self.conexao = conexao
        self.cursor = cursor
        self.lista_colunas_db = lista_colunas_db
        self.nome_arquivo = nome_arquivo
        self.extensao = extensao
    
    def leitura_insercao(self):

        lista_extensoes = ["xlsx","csv","json","xml"]
        set_lista_colunas_db =  set(self.lista_colunas_db)
        
        if self.extensao not in lista_extensoes:
            print("Extensao inválida!")
        
        match self.extensao:

            case "xlsx":
                
                df_tabela_import = pd.read_excel(self.nome_arquivo + ".xlsx", index_col = 0)
                colunas_tabela_import = df_tabela_import.columns
                lista_colunas_tabela_import = []

                for coluna in colunas_tabela_import:
                    lista_colunas_tabela_import.append(coluna)

                set_lista_colunas_tabela_import = set(lista_colunas_tabela_import)
                
                if set_lista_colunas_tabela_import == set_lista_colunas_db:

                    valor_linhas_tabela_import = [(valor['nome'],valor['cpf'],valor['email'],valor['cep']) for coluna, valor in df_tabela_import.iterrows()]
                    
                    self.cursor.executemany(
                        "INSERT OR IGNORE cadastrados (nome,cpf,email,cep) VALUES(?,?,?,?)",
                        valor_linhas_tabela_import
                        )
                    self.conexao.commit()
                    print("Dados do arquivo '",self.nome_arquivo,"' inseridos com sucesso!")

                else:
                    print("A estrutura da dados do arquivo ",self.nome_arquivo," é incompatível com o banco de dados.")
            
            case "csv":

                df_tabela_import = pd.read_csv(self.nome_arquivo + ".csv", index_col = 0)
                colunas_tabela_import = df_tabela_import.columns
                lista_colunas_tabela_import = []

                for coluna in colunas_tabela_import:
                    lista_colunas_tabela_import.append(coluna)

                set_lista_colunas_tabela_import = set(lista_colunas_tabela_import)
                
                if set_lista_colunas_tabela_import == set_lista_colunas_db:

                    valor_linhas_tabela_import = [(valor['nome'],valor['cpf'],valor['email'],valor['cep']) for coluna, valor in df_tabela_import.iterrows()]
                    
                    self.cursor.executemany(
                        "INSERT OR IGNORE INTO cadastrados  (nome,cpf,email,cep) VALUES(?,?,?,?)",
                        valor_linhas_tabela_import
                        )
                    self.conexao.commit()
                    print("Dados do arquivo '",self.nome_arquivo,"' inseridos com sucesso!")

                else:
                    print("A estrutura da dados do arquivo ",self.nome_arquivo," é incompatível com o banco de dados.")
                
            case "json":

                df_tabela_import = pd.read_json(self.nome_arquivo + ".json", index_col = 0)
                colunas_tabela_import = df_tabela_import.columns
                lista_colunas_tabela_import = []

                for coluna in colunas_tabela_import:
                    lista_colunas_tabela_import.append(coluna)

                set_lista_colunas_tabela_import = set(lista_colunas_tabela_import)
                
                if set_lista_colunas_tabela_import == set_lista_colunas_db:

                    valor_linhas_tabela_import = [(valor['nome'],valor['cpf'],valor['email'],valor['cep']) for coluna, valor in df_tabela_import.iterrows()]
                    
                    self.cursor.executemany(
                        "INSERT OR IGNORE INTO cadastrados (nome,cpf,email,cep) VALUES(?,?,?,?)",
                        valor_linhas_tabela_import                        
                        )
                    
                    self.conexao.commit()
                    print("Dados do arquivo '",self.nome_arquivo,"' inseridos com sucesso!")

                else:
                    print("A estrutura da dados do arquivo ",self.nome_arquivo," é incompatível com o banco de dados.")
        
            case "xml":

                df_tabela_import = pd.read_xml(self.nome_arquivo + ".xml", index_col = 0)
                colunas_tabela_import = df_tabela_import.columns
                lista_colunas_tabela_import = []

                for coluna in colunas_tabela_import:
                    lista_colunas_tabela_import.append(coluna)

                set_lista_colunas_tabela_import = set(lista_colunas_tabela_import)
                
                if set_lista_colunas_tabela_import == set_lista_colunas_db:

                    valor_linhas_tabela_import = [(valor['nome'],valor['cpf'],valor['email'],valor['cep']) for coluna, valor in df_tabela_import.iterrows()]
                    
                    self.cursor.executemany(
                        "INSERT OR IGNORE INTO cadastrados (nome,cpf,email,cep) VALUES(?,?,?,?)",                        
                        valor_linhas_tabela_import                        
                        )
                    
                    self.conexao.commit()
                    print("Dados do arquivo '",self.nome_arquivo,"' inseridos com sucesso!")

                else:
                    print("A estrutura da dados do arquivo ",self.nome_arquivo," é incompatível com o banco de dados.")
        
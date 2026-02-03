import sqlite3 as sql
import pandas as pd 
from funcoes import *

conexao = sql.connect("crud_cpf.db")
cursor = conexao.cursor()

colunas_banco = cursor.execute("PRAGMA table_info(cadastrados)")
colunas_banco = cursor.fetchall()#Resgata os dados do ultimo comando sql

lista_colunas = []

for column in colunas_banco:
    lista_colunas.append(column[1])

print(lista_colunas)

df = pd.read_excel('maria.xlsx')
print(df)

lista_colunas_df = df.columns
print(lista_colunas_df)

lista_df = []

for item in lista_colunas_df[1:]:
    lista_df.append(item)

print(lista_df)

if set(lista_df) == set(lista_colunas):
    print("te amo")

else:
    print("Nao te amo")

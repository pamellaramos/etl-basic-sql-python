#Regra de Negócio: Remover o caracter "ponto" na última coluna do arquivo e evitar oque o número seja truncado 

import pyodbc
import csv

# Definir as informações de conexão
server = 'PAMELLA\SQLEXPRESS' # ou endereço IP
database = 'host'
driver = 'SQL Server'
trusted_connection = 'yes'


#Função para substituir ponto por vazio 
def remove_ponto(valor):
    return int(valor.replace('.', ''))

# Abre o arquivo csv
with open('producao_alimentos.csv', 'r') as file:
    
    #criar um leitor de aquivo csv
    reader = csv.reader(file)
    
    #Pular o cabeçalho 
    next(reader)

     #realizar a conexão com o banco de dados
    conexao = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection='+trusted_connection)
    cursor  = conexao.cursor()
   

    #excluir a tabela, caso ela já exista
    cursor.execute('DROP TABLE IF EXISTS producao')

    #criar uma nova tabela
    cursor.execute('''CREATE TABLE producao (
    produto VARCHAR (1000),
    quantidade INT,
    preco_medio FLOAT, 
    receita_total FLOAT,
    margem_lucro FLOAT
    )''')

    for linha in reader:
        #primeira regra de negócio, quantidades vendidas > 10
        if int(linha[1]) > 10:
            
            #chamar a função que remove o ponto. 
            linha[3] = remove_ponto(linha[3])

            #margem de lucro 
            margem_lucro = (linha[3] /float(linha[1])) - float(linha[2])

            #insere esses dados
            cursor.execute('INSERT INTO producao (produto, quantidade, preco_medio, receita_total, margem_lucro) VALUES (?,?,?,?,?)', (linha[0], linha[1], linha[2], linha[3], margem_lucro))
    
    cursor.commit()
    cursor.close()
    

print('job concluído com sucesso! ')


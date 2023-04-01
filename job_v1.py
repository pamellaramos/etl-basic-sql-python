import pyodbc
import csv
import conexao

# Definir as informações de conexão
server = 'PAMELLA\SQLEXPRESS' # ou endereço IP
database = 'host'
driver = 'SQL Server'
trusted_connection = 'yes'

#Conexão com o banco de dados
conexao = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection='+trusted_connection)
cursor  = conexao.cursor()

# Se existir a tabela, fazer a exclusão
cursor.execute('DROP TABLE IF EXISTS producao')

#criar uma tabela no banco de dados
cursor.execute('''CREATE TABLE producao (
    produto VARCHAR (1000),
    quantidade INT,
    preco_medio FLOAT, 
    receita_total FLOAT
)''')


#Grava e fecha o conexão
cursor.commit()
cursor.close()



#Abre o arquivo csv com os dados de produção de alimentos 
with open('producao_alimentos.csv', 'r') as file:
    
    #leitor de CSV
    reader = csv.reader(file)

    #Pula a primeira linha (cabeçalho)
    next(reader)

    #conectar ao banco de dados
    conexao = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection='+trusted_connection)
    cursor = conexao.cursor()

    #inserir linha por linha no banco de dados 
    for linha in reader:
        cursor.execute('INSERT INTO producao (produto, quantidade, preco_medio, receita_total) VALUES (?,?,?,?)', linha)
    cursor.commit()
    cursor.close()

print('Job concluido com sucesso!')


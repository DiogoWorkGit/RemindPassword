#pip install PySimpleGUI
#pip install mysql-connector-python

import PySimpleGUI as sg
import mysql.connector
from datetime import datetime

def atualizar_sql(cursor):
    sql = f'SELECT * FROM gensen;'
    cursor.execute(sql)
    resultset = cursor.fetchall()
    result=[]
    for i in range(len(resultset)):
        x = str(resultset[i])
        x = x.replace(")","").replace("(","").replace(",","").replace("'","")
        result.append(x)
    return result

def insert_sql(cursor, conexao, user, senha, email, siteapp, nome, url, data):
    sql = f'INSERT INTO gensen (usuario, pass, email, tipo, nome, url, data_creation) VALUES ("{user}", "{senha}", "{email}", "{siteapp}", "{nome}", "{url}", "{data}");'
    try:
        cursor.execute(sql)
        conexao.commit()
        msg = f"{cursor.rowcount} colunas afetadas"
    except:
        msg = "O banco de dados encontrou um erro ao inserir os valores"
    return msg
    
def alter_sql(cursor, conexao, id, user, senha, email, siteapp, nome, url):
    sql = f'UPDATE gensen SET usuario = "{user}", pass = "{senha}", email = "{email}", tipo = "{siteapp}", nome = "{nome}", url = "{url}" WHERE id = {id})'
    try:
        cursor.execute(sql)
        conexao.commit()
        msg = f"{cursor.rowcount} colunas afetadas"
    except:
        msg = "O banco de dados encontrou um erro ao tentar alterar os valores"
    return msg

def delet_sql(id):
    sql = f'DELETE FROM gensen WHERE id = {id}'
    try:
        cursor.execute(sql)
        conexao.commit()
        msg = f"{cursor.rowcount} colunas deletadas"
    except:
        msg = "O banco de dados encontrou um erro ao tentar deletar os valores"
    return msg

def vefNull(user, senha, nome):
    mensagem = "Campos não preenchidos:"
    if user == "":
        mensagem = mensagem + " Usuário"
    if senha == "":
        mensagem = mensagem + " Senha"
    if nome == "":
        mensagem = mensagem + " Nome"
    return mensagem

def gettime():
    t = datetime.now()
    time = t.strftime('%d/%m/%Y - %H:%M;%S')
    return time
    
def inserir():
    sucesso = ""
    layout = [
        [sg.Text("Digite o usuário"), sg.Text("(*Campo obrigatório)")], [sg.InputText(key="user")],
        [sg.Text("Digite a senha da conta"), sg.Text("(*Campo obrigatório)")], [sg.InputText(key="userPass")],
        [sg.Text("Digite o email usado no cadastro")], [sg.InputText(key="userEmail")],
        [sg.Text("A conta é para um site ou aplicativo"), sg.Text("(*Campo obrigatório)")], [sg.Radio("Site", group_id=(1), key="Site", default=True),sg.Radio("Aplicativo", group_id=(1), key="App")],
        [sg.Text("Nome do site ou do app"), sg.Text("(*Campo obrigatório)")], [sg.InputText(key="nome")],
        [sg.Text("Qual o url")], [sg.InputText(key="Url")],
        [sg.Button("Registrar", key="Regis")], [sg.Text(f"{sucesso}")],
        ]
    janela = sg.Window("GERENCIADOR DE SENHAS",
                       layout)
    while True:
        evento, valores = janela.read()
        if evento == "Regis":
            usuario = valores["user"]
            senha = valores["userPass"]
            email = valores["userEmail"]
            if valores["Site"] == True:
                tipo = "Site"
            else:
                tipo = "App"
            nome = valores["nome"]
            url = valores["Url"]
            data = gettime()
            
            mensagem = vefNull(usuario, senha, nome)
            if mensagem != "Campos não preenchidos:":
                continue
            sucesso = insert_sql(cursor, conexao, usuario, senha, email, tipo, nome, url, data)
        
        if evento == sg.WIN_CLOSED:
            break


def main():
    lista = atualizar_sql(cursor)
    hlis = ["id", "Usuário", "Senha", "Email", "Site ou App", "Nome", "URL", "Data de Criação"]
    layout = [
        [sg.Table(
            lista,
            headings=hlis)],
        
        [sg.Button("ADICIONAR NOVO PERFIL", key="insInfo"),
         sg.Button("ATUALIZAR ALGUMA INFORMAÇÃO", key="attInfo"),
         sg.Button("ADICIONAR NOVO PERFIL", key="delInfo"),]
    ]
    
    janela = sg.Window("GERENCIADOR DE SENHAS",
                       layout)
    
    
    while True:
        evento, valores = janela.read()
        if evento == "insInfo":
            inserir()
        
        if evento == sg.WIN_CLOSED:
            break

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='estudos',
)
cursor = conexao.cursor(buffered=True)

main()
        
cursor.close()
conexao.close()
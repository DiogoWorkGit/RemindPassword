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
    finalresult = []
    for i in range(len(resultset)):
        resultsetpart = resultset[i]
        for y in range(len(resultsetpart)):
            x = str(resultsetpart[y])
            x = x.replace(")","").replace("(","").replace(",","").replace("'","")
            result.append(x)
        finalresult.append(result)
        result = []
    return finalresult

def insert_sql(cursor, conexao, user, senha, email, siteapp, nome, url, data):
    sql = f'INSERT INTO gensen (usuario, pass, email, tipo, nome, url, data_creation) VALUES ("{user}", "{senha}", "{email}", "{siteapp}", "{nome}", "{url}", "{data}");'
    try:
        cursor.execute(sql)
        conexao.commit()
        msg = "Registro inserido com sucesso"
    except:
        msg = "O banco de dados encontrou um erro ao inserir os valores"
    sg.popup(msg,
        no_titlebar=True,
        grab_anywhere=True,
        font=("Courier New",15))
    atualizar_sql(cursor)
    
def alter_sql(cursor, conexao, id, user, senha, email, siteapp, nome, url):
    sql = f'UPDATE gensen SET usuario = "{user}", pass = "{senha}", email = "{email}", tipo = "{siteapp}", nome = "{nome}", url = "{url}" WHERE id = {id})'
    try:
        cursor.execute(sql)
        conexao.commit()
        msg = "Registro alterado com sucesso"
    except:
        msg = "O banco de dados encontrou um erro ao tentar alterar os valores"
    sg.popup(msg,
        no_titlebar=True,
        grab_anywhere=True,
        font=("Courier New",15))
    return msg

def delet_sql(id):
    sql = f'DELETE FROM gensen WHERE id = {id}'
    try:
        cursor.execute(sql)
        conexao.commit()
        msg = "O registro foi deletado com sucesso"
    except:
        msg = "O banco de dados encontrou um erro ao tentar deletar os valores"
    sg.popup(msg,
        no_titlebar=True,
        grab_anywhere=True,
        font=("Courier New",15))
    return msg

def vefNull(user, senha, tipo, nome):
    mensagem = "Alguns campos não foram preenchidos:"
    if user == "":
        mensagem = mensagem + "\n  - Qual o usuário da conta"
    if senha == "":
        mensagem = mensagem + "\n  - Qual a senha da conta"
    if tipo == "":
        mensagem = mensagem + "\n  - A conta está em um aplicativo ou em um site?"
    if nome == "":
        mensagem = mensagem + "\n  - Qual o lugar onde a conta está hospedada"
    return mensagem

def gettime():
    t = datetime.now()
    time = t.strftime('%d/%m/%Y - %H:%M:%S')
    return time
    
def inserir():
    layout = [
        [sg.Text("Digite o usuário", font=("Courier New",15)),
         sg.Text("*Campo obrigatório*", font=("Courier New",10, ["bold"]))],
        [sg.InputText(key="user", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        [sg.Text("Digite a senha da conta", font=("Courier New",15)),
         sg.Text("*Campo obrigatório*", font=("Courier New",10, ["bold"]))],
        [sg.InputText(key="userPass", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        [sg.Text("Digite o email usado no cadastro", font=("Courier New",15))],
        [sg.InputText(key="userEmail", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        [sg.Text("A conta é para um site ou aplicativo", font=("Courier New",15))],
        [sg.Radio("Site", group_id=(1), key="Site", font=("Courier New",15, ["bold"])),
         sg.Radio("Aplicativo", group_id=(1), key="App", font=("Courier New",15, ["bold"])),
         sg.Text("*Campo obrigatório*", font=("Courier New",10, ["bold"]) ,pad=((0,0),(0,30)))],
        
        [sg.Text("Nome do site ou do app", font=("Courier New",15)),
         sg.Text("*Campo obrigatório*", font=("Courier New",10, ["bold"]))],
        [sg.InputText(key="nome", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        [sg.Text("Qual o url", font=("Courier New",15))],
        [sg.InputText(key="Url", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        [sg.Button("REGISTRAR PERFIL", key="Regis", font=("Avantgarde",15), size=48 ,pad=((0,0),(30,0)))],
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
            elif valores["App"] == True:
                tipo = "App"
            else:
                tipo = ""
            nome = valores["nome"]
            url = valores["Url"]
            data = gettime()
            
            mensagem = vefNull(usuario, senha, tipo, nome)
            if mensagem != "Alguns campos não foram preenchidos:":
                sg.popup(mensagem,
                    no_titlebar=True,
                    grab_anywhere=True,
                    font=("Courier New",15))
                continue
            janela.close()
            insert_sql(cursor, conexao, usuario, senha, email, tipo, nome, url, data)
            break
        if evento == sg.WIN_CLOSED:
            break

def main():
    lista = atualizar_sql(cursor)
    hlis = ["ID", "USUÁRIO", "SENHA", "EMAIL", "ONDE", "NOME", "URL", "DATA DE CRIAÇÃO"]
    layout = [
        [sg.Table(
            lista,
            headings=hlis,
            col_widths=[3, 10, 10, 20, 6, 10, 10, 17],
            auto_size_columns=False,
            font=("Verdana",13),
            row_height=35,
            key="Tabela")
            ],
        
        [sg.Button("ADICIONAR NOVO PERFIL", key="insInfo", font=("Avantgarde",15), size=30),
         sg.Button("ATUALIZAR ALGUMA INFORMAÇÃO", key="attInfo", font=("Avantgarde",15), size=30),
         sg.Button("DELETAR UM PERFIL", key="delInfo",font=("Avantgarde",15), size=25)]
    ]
    
    janela = sg.Window("GERENCIADOR DE SENHAS",
                       layout)
    
    
    while True:
        
        lista = atualizar_sql(cursor)
        evento, valores = janela.read()
        if evento == "insInfo":
            janela.hide()
            inserir()
            lista = atualizar_sql(cursor)
            janela._Show()
        
            
        janela["Tabela"].update(lista)
        if evento == sg.WIN_CLOSED:
            break


#Inicio do código
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='estudos',
)
cursor = conexao.cursor(buffered=True)
sg.theme("DarkTeal12")
main()
        
cursor.close()
conexao.close()
#Término
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

def buscarId_sql(cursor, id):
    sql = f'SELECT usuario, pass, email, nome, url FROM gensen WHERE id = {id};'
    try:
        cursor.execute(sql)
        resultset = cursor.fetchone()
        finalresult = []
        for y in range(len(resultset)):
            x = str(resultset[y])
            x = x.replace(")","").replace("(","").replace(",","").replace("'","")
            finalresult.append(x)
        return finalresult
    except:
        sg.popup("O id não foi encontrado no banco de dados",
                    no_titlebar=True,
                    grab_anywhere=True,
                    font=("Courier New",15))

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
    
def alter_sql(cursor, conexao, id, user, senha, email, nome, url):
    sql = f'UPDATE gensen SET usuario = "{user}", pass = "{senha}", email = "{email}", nome = "{nome}", url = "{url}" WHERE id = {id}'
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

def vefNullInser(user, senha, tipo, nome):
    mensagem = "Alguns campos não foram preenchidos:"
    if user == "":
        mensagem = mensagem + "\n  - Qual o usuário da conta?"
    if senha == "":
        mensagem = mensagem + "\n  - Qual a senha da conta?"
    if tipo == "":
        mensagem = mensagem + "\n  - A conta está em um aplicativo ou em um site?"
    if nome == "":
        mensagem = mensagem + "\n  - Qual o lugar onde a conta está hospedada?"
    return mensagem

def vefNullAlter(user, senha, nome):
    mensagem = "Alguns campos não foram preenchidos:"
    if user == "":
        mensagem = mensagem + "\n  - Qual será o novo usuário da conta?"
    if senha == "":
        mensagem = mensagem + "\n  - Qual será a nova senha da conta?"
    if nome == "":
        mensagem = mensagem + "\n  - Qual o lugar onde a conta está hospedada?"
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
            
            mensagem = vefNullInser(usuario, senha, tipo, nome)
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

def alterar():
    usuarioTxt = ""
    senhaTxt = ""
    emailTxt = ""
    nomeTxt = ""
    urlTxt = ""
    
    layout = [
        #Campo referente ao ID do registro
        [sg.Text("Verificar o ID", font=("Courier New",15)),
         sg.Text("*Campo não pode estar em branco*", font=("Courier New",10, ["bold"]))],
        [sg.InputText(key="id", font=("Courier New",15) ,pad=((0,0),(0,30)), size=10), sg.Button("Consultar o ID", key="Consultar",font=("Avantgarde",15) ,pad=((0,0),(0,30)))],
        
        #Campo referente ao usuário do registro
        [sg.Text("Alterar o usuário", font=("Courier New",15)),
         sg.Text("*Campo não pode estar em branco*", font=("Courier New",10, ["bold"]))],
        [sg.InputText(key="user", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        #Campo referente a senha do registro
        [sg.Text("Alterar a senha da conta", font=("Courier New",15)),
         sg.Text("*Campo não pode estar em branco*", font=("Courier New",10, ["bold"]))],
        [sg.InputText(key="userPass", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        #Campo referente ao email do registro
        [sg.Text("Alterar o email usado no cadastro", font=("Courier New",15))],
        [sg.InputText(key="userEmail", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        #Campo referente ao nome do aplicativo ou site do registro
        [sg.Text("Alterar nome do site ou do app", font=("Courier New",15))],
        [sg.Text("*Campo não pode estar em branco*", font=("Courier New",10, ["bold"]))],
        [sg.InputText(key="nome", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        #Campo referente ao url seja de um site do registro
        [sg.Text("Alterar o url", font=("Courier New",15))],
        [sg.InputText(key="Url", font=("Courier New",15) ,pad=((0,0),(0,30)))],
        
        #Botão para realizar a alteração do registro no banco de dados
        [sg.Button("ALTERAR REGISTRO DO PERFIL", key="alte", font=("Avantgarde",15), size=48 ,pad=((0,0),(30,0)))],
        ]
    janela = sg.Window("GERENCIADOR DE SENHAS",
                       layout)
    while True:
        evento, valores = janela.read()
        if evento == "Consultar":
            id = valores["id"]
            try:
                id = int(id)
            except:
                sg.popup("O id não é um número válido",
                    no_titlebar=True,
                    grab_anywhere=True,
                    font=("Courier New",15))
                continue
            
            result = buscarId_sql(cursor, id)
            if result == None:
                continue
            
            usuarioTxt = result[0]
            senhaTxt = result[1]
            emailTxt = result[2]
            nomeTxt = result[3]
            urlTxt = result[4]
            
            janela["user"].update(f"{usuarioTxt}")
            janela["userPass"].update(f"{senhaTxt}")
            janela["userEmail"].update(f"{emailTxt}")
            janela["nome"].update(f"{nomeTxt}")
            janela["Url"].update(f"{urlTxt}")
            
        if evento == "alte":
            usuario = valores["user"]
            senha = valores["userPass"]
            email = valores["userEmail"]
            nome = valores["nome"]
            url = valores["Url"]
            
            mensagem = vefNullAlter(usuario, senha, nome)
            if mensagem != "Alguns campos não foram preenchidos:":
                sg.popup(mensagem,
                    no_titlebar=True,
                    grab_anywhere=True,
                    font=("Courier New",15))
                continue
            
            alter_sql(cursor, conexao, id, usuario, senha, email, nome, url)
            
            janela["id"].update("")
            janela["user"].update("")
            janela["userPass"].update("")
            janela["userEmail"].update("")
            janela["nome"].update("")
            janela["Url"].update("")
            continue
            
            
        
        if evento == sg.WIN_CLOSED:
            break

def deletar():
    layout = [
        [sg.Text("Digite o id do registro que será deletado", font=("Courier New",15)),
         sg.Text("*Campo obrigatório*", font=("Courier New",10, ["bold"]))],
        
        [sg.InputText(key="id", font=("Courier New",15) ,pad=((0,0),(0,30)), size=15), sg.Button("DELETAR REGISTRO", key="Delet", font=("Avantgarde",15), size=40 ,pad=((5,0),(0,30)))]
    ]
    
    janela = sg.Window("GERENCIADOR DE SENHAS",
                       layout)
    
    while True:
        evento, valores = janela.read()
        if evento == "Delet":
            confirmar = sg.popup_ok_cancel("Tem certeza que quer deletar esse registro?",
                    no_titlebar=True,
                    grab_anywhere=True,
                    font=("Courier New",15))
            if confirmar != "OK":
                continue
            id = valores["id"]
            try:
                id = int(id)
            except:
                sg.popup("Esse Id não é um valor numérico",
                    no_titlebar=True,
                    grab_anywhere=True,
                    font=("Courier New",15))
                continue
            delet_sql(id)
            janela["id"].update("")
            
        
        if evento == sg.WIN_CLOSED:
            break
        
        
        
    



def main():
    lista = atualizar_sql(cursor)
    hlis = ["ID", "USUÁRIO", "SENHA", "EMAIL", "ONDE", "NOME", "URL", "DATA DE CRIAÇÃO"]
    layout = [
        [sg.Table(
            lista,
            headings=hlis,
            col_widths=[3, 10, 15, 20, 6, 10, 10, 17],
            auto_size_columns=False,
            font=("Verdana",13),
            header_font=("Verdana",13, ["bold"]),
            row_height=35,
            alternating_row_color = "",
            key="Tabela")
            ],
        
        [sg.Button("ADICIONAR NOVO PERFIL", key="insInfo", font=("Avantgarde",15, ["bold"]), size=30),
         sg.Button("ATUALIZAR ALGUMA INFORMAÇÃO", key="attInfo", font=("Avantgarde",15, ["bold"]), size=30),
         sg.Button("DELETAR UM PERFIL", key="delInfo",font=("Avantgarde",15, ["bold"]), size=25)]
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
            janela["Tabela"].update(lista)
            janela._Show()
        
        if evento == "attInfo":
            janela.hide()
            alterar()
            lista = atualizar_sql(cursor)
            janela["Tabela"].update(lista)
            janela._Show()
        
        if evento == "delInfo":
            janela.hide()
            deletar()
            lista = atualizar_sql(cursor)
            janela["Tabela"].update(lista)
            janela._Show()
        
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
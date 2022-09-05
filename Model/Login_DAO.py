class login:
    def __init__ (self, username, password, safetyphrase):
        username = ""
        password = ""
        safetyphrase = ""
        
    def setLogin (self, x, y, z):
        global username
        global password
        global safetyphrase
        
        username = x
        password = y
        safetyphrase = z
    
    def login (self, x, y):
        global username
        global password
        logado = False
        if username == x and password == y:
            logado = True
        else:
            logado = False
        
        return logado
    
    def forgotPassword (self, x, y):
        global username
        global safetyphrase
        
        if username == x and safetyphrase == y:
            redefinir = True
        else:
            redefinir = False
        
        return redefinir
    
    def changePassword (self, x, y):
        global password
        
        if x == True:
            password = y
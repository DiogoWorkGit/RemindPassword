class login:
    def __init__ (self):
        self.username
        self.password
        self.safetyphrase
        
    def setLogin (self, username, password, safetyphrase):
        self.username = username
        self.password = password
        self.safetyphrase = safetyphrase
    
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
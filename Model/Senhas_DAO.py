class managePasswords:
    #Instale o conector de MySQL x Python ( pip install mysql-connector-python ) 
    import 
    
    def __init__(self, username, password, email, nome, url):
        self.username = username
        self.password = password
        self.email = email
        self.nome = nome
        self.url = url
    
    def insertAccount (self, w, x, y, z):
        self.username = w
        self.password = x
        self.nome = y
        self.url = z
        
    def changePassword (self, w, x, y, z):
        self.username = w
        self.password = x
        self.nome = y
        self.url = z
        
    def deletePassword (self, w, x, y, z):
        global username
        global password
        global nome
        global url
        
        
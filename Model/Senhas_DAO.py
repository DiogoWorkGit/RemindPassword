class managePasswords:
    def __init__(self):
        username = ""
        password = ""
        nome = ""
        url = ""
    
    def insertPassword (self, w, x, y, z):
        global username
        global password
        global nome
        global url
        
        username = w
        password = x
        nome = y
        url = z
        
    def chagePassword (self, w, x, y, z):
        global username
        global password
        global nome
        global url
        
        username = w
        password = x
        nome = y
        url = z
        
    def deletePassword (self):
        global username
        global password
        global nome
        global url
        
        
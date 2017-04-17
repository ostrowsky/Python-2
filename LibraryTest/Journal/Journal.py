import Books.Books

class Journal(Books.Books.Books):
    def __init__(self,id, name, author, shelve,col_str): #конструктор класс
        super().__init__(id, name, author, shelve)
        self.col_str=col_str
    def getCol_str(self):
        return self.col_str
    def setCol_str(self,newCol_str):
        self.col_str=newCol_str
    def printer(self):
        super().printer()
        print("Количество страниц в журнале ", self.col_str)
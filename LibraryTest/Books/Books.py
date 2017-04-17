class Books:
    def __init__(self, id, name, author, shelve):  #конструктор класс
        self.id=id          #атрибут класса-уникальный идентификатор
        self.name=name      #атрибут класс-наименование
        self.author=author  #атрибут класса-автор
        self.shelve=shelve  #атрибут класса-номер полки

    #метод для возвращения текущего значения атрибута уникального идентификатора
    def getId(self):
        return self.id

    # метод для возвращения текущего значения атрибута наименования
    def getName(self):
        return self.name

    # метод для возвращения текущего значения атрибута автора
    def getAuthor(self):
        return self.author

    # метод для возвращения текущего значения атрибута номер полки
    def getShelve(self):
        return self.shelve

    # метод для установления нового значения атрибута уникального идентификатора
    def setId(self,newId):
        self.id=newId

    # метод для установления нового значения атрибута наименования
    def setName(self, newName):
        self.name = newName

    # метод для установления нового значения атрибута автора
    def setAuthor(self, newAuthor):
        self.Author = newAuthor

    # метод для установления нового значения атрибута номер полки
    def setShelve(self, newShelve):
        self.shelve = newShelve

    #метод для распечатки полной информации о книжном изделии
    def printer(self):
        print("Сведения о книге/журнале под номером ",self.id,", наименование книги/журнала - ",
              self.name, " автор - ",self.author, " номер полки - ", self.shelve)





import Books.Books
import Journal.Journal
class Library:
    n=1                 #атрибут класса - текущее количество книг
    nj=1                #атрибут класса - текущее количество журналов
    N=100               #атрибут класса - максимально клочество книг и журналов в библиотеке
    Book = {}           #атрибут класса - массив книг
    Journal = {}        #атрибут класса - массив журналов

    def __init__(self,N): #конструктор класс
        self.n=0
        self.nj = 0
        self.N=N
        for x in range(1, Library.N):
            self.Book[x] = Books.Books.Books(0,"","",0)
        for x in range(1, Library.N):
            self.Journal[x] = Journal.Journal.Journal(0, "", "", 0,0)

    # метод для распечатки общзего списка книг и журналов в библиотеке
    def printer(self):
        print("Список книг")
        for x in range(1, Library.n):
            print(Library.Book[x].name)
        print("Список журналов")
        for x in range(1, Library.nj):
            print(Library.Journal[x].name)

    # метод добавление книг
    def addBook(self, B):
        if (self.n<100):
            Library.n=Library.n+1
            Library.Book[Library.n - 1].id =B.id
            Library.Book[Library.n - 1].name = B.name
            Library.Book[Library.n - 1].author = B.author
            Library.Book[Library.n - 1].shelve = B.shelve
        else:
            print("Библиотека переполнена!")

    # метод добавление журналов
    def addJournal(self, J):
        if (self.nj<100):
            Library.nj=Library.nj+1
            Library.Journal[Library.nj - 1].id =J.id
            Library.Journal[Library.nj - 1].name = J.name
            Library.Journal[Library.nj - 1].author = J.author
            Library.Journal[Library.nj - 1].shelve = J.shelve
            Library.Journal[Library.nj - 1].col_str = J.col_str
        else:
            print("Библиотека переполнена!")

    # метод поиска книги по уникальному идентификатору
    def getBook(self,i):
        if(i<0 or i>Library.n):
            print("Такой книги нет")
        else:
            self.Book[i].printer()

    # метод поиска журнала по уникальному идентификатору
    def getJournal(self,i):
        if(i<0 or i>Library.nj):
            print("Такой книги нет")
        else:
            self.Journal[i].printer()

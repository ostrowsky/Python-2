import Books.Books
import Library.Library
import Journal.Journal

newLibrary=Library.Library.Library(100)

newBook=Books.Books.Books(1,"Пиковая дама","Пушкин",3)
newBook1=Books.Books.Books(2,"Грозовой перевал","Броннте",5)
newBook2=Books.Books.Books(3,"Унесенные ветром","Миттчел",4)
newJournal=Journal.Journal.Journal(5,"National geographic", "NC", 10, 200)
newJournal1=Journal.Journal.Journal(5,"Cosmopolitan", "Россия", 7, 150)

newLibrary.addBook(newBook)
newLibrary.addBook(newBook1)
newLibrary.addBook(newBook2)
newLibrary.addJournal(newJournal)
newLibrary.addJournal(newJournal1)

newLibrary.getBook(3)
newLibrary.getBook(6)
newLibrary.getJournal(1)
newLibrary.getJournal(13)

newLibrary.printer()




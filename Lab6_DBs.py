import sqlite3
from datetime import datetime, timedelta

def TakeBookCopy(conn, userid, bookid):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM BookCopies WHERE book_id = ? AND IsAvailabe = 1",
                   (bookid,))
    bookcopy = cursor.fetchone()
    cursor.execute("SELECT * FROM Borrows WHERE user_id = ?",
                   (userid[0],))
    borrow = cursor.fetchone()
    if(borrow is not None):
        print("На данный момент у вас уже взята книга. Верните её, чтобы взять другую.")
        cursor.close()
        return
    elif(bookcopy is None):
        print("На данный момент нет доступных копий выбранной книги.")
        cursor.close()
        return

    else:
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Borrows(receive_date, user_id, copy_id) VALUES(?, ?, ?)",
                       (formatted_date, userid[0], bookcopy[0]))
        conn.commit()
        cursor.close()
        print("Вы взяли копию выбранной книги.")


def ShowBookReviews(conn, bookid):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Reviews WHERE book_id = ?",
                   (bookid, ))
    reviews=cursor.fetchall()
    cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                        (bookid,))
    book_name = cursor.fetchone()
    users =[]
    user = ()
    for review in reviews:
        cursor.execute("SELECT * FROM Users WHERE user_id = ?",
                       (review[1], ))
        user = cursor.fetchone()
        users.append(user)
    current_user = ()
    print(f"Отзывы на книгу {book_name[0]}\n")
    for review in reviews:
            for user in users:
                if(review[1] == user[0]):
                    print(f"Пользователь: {user[1]} {user[2]} \nОценка: {review[3]} \nТекст отзыва: {review[4]} \nДата последнего редактирования отзыва: {review[5]}\n")
    cursor.close()


def DeleteReview(conn, userid, bookid):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Reviews WHERE user_id = ? AND book_id = ?",
                   (userid[0], bookid, ))
    review=cursor.fetchone()
    if(review):
        cursor.execute("DELETE FROM Reviews WHERE user_id = ? AND book_id = ?",
                       (userid[0], bookid, ))
        conn.commit()
        cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                   (bookid,))
        book_name = cursor.fetchone()
        print(f"Ваш отзыв на книгу {book_name[0]} был удалён.")
    else:
        cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                        (bookid,))
        book_name = cursor.fetchone()
        print(f"Вы ещё не написали отзыв на книгу {book_name[0]}.")
    cursor.close()


def ChangeReview(conn, userid, bookid):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Reviews WHERE user_id = ? AND book_id = ?",
                   (userid[0], bookid, ))
    review=cursor.fetchone()
    if(review):
        print("Ваш текущий отзыв:")
        cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                   (bookid,))
        book_name = cursor.fetchone()
        cursor.close()
        print(f"Книга: {book_name[0]}")
        print(f"Оценка: {review[3]}")
        print(f"Текст: {review[4]}")
        print(f"Дата последнего редактирования: {review[5]}")
        while True:
            cursor=conn.cursor()
            print("1.Изменить оценку отзыва.")
            print("2.Изменить текст отзыва.")
            print("3.Выйти из меню редактирования отзыва.")
            choice = input("Выберите действие(1/2/3): ")
            if(choice=='1'):
                while True:
                    rating = input("Введите оценку(от 1 до 5): ")
                    try:
                        ratingnumber= int(rating)
                    except ValueError:
                        print('Некорректный ввод. Повторите попытку.')
                        continue
                    if (ratingnumber not in range(1,6)):
                        print('Некорректный ввод. Повторите попытку.')
                        continue
                    else:
                        current_date = datetime.now().date()
                        formatted_date = current_date.strftime("%Y-%m-%d")
                        cursor.execute("UPDATE Reviews SET rating = ?, review_date = ? WHERE user_id = ? AND book_id = ?",
                                       (ratingnumber, formatted_date, userid[0], bookid))
                        conn.commit()
                        print("Вы обновили оценку отзыва.")
                        break
            elif(choice=='2'):
                        text = input("Введите текст отзыва: ")
                        current_date = datetime.now().date()
                        formatted_date = current_date.strftime("%Y-%m-%d")
                        cursor.execute("UPDATE Reviews SET review_text = ?, review_date = ? WHERE user_id = ? AND book_id = ?",
                                        (text, formatted_date, userid[0], bookid))
                        conn.commit()
                        print("Вы обновили текст отзыва.")
            elif(choice=='3'):
                break
            else:
                print('Некорректный ввод. Повторите попытку.')
            cursor.close()
    else:
            cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                    (bookid,))
            book_name = cursor.fetchone()
            print(f"Вы ещё не написали отзыв на книгу {book_name[0]}.")
            cursor.close()


def AddReview(conn, userid, bookid):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Reviews WHERE user_id = ? AND book_id = ?",
                   (userid[0], bookid, ))
    review=cursor.fetchone()
    if(review):
        print("Вы уже добавили отзыв на эту книгу.")
        cursor.close()
        return
    else:
        while True:
            rating = input("Введите оценку(от 1 до 5): ")
            try:
                ratingnumber= int(rating)
            except ValueError:
                print('Некорректный ввод. Повторите попытку.')
                continue
            if (ratingnumber not in range(1,6)):
                print('Некорректный ввод. Повторите попытку.')
                continue
            else:
                text = input("Введите текст отзыва: ")
                current_date = datetime.now().date()
                formatted_date = current_date.strftime("%Y-%m-%d")
                cursor.execute("INSERT INTO Reviews(user_id, book_id, rating, review_text, review_date) VALUES (?, ?, ?, ?, ?)",
                               (userid[0], bookid, ratingnumber, text, formatted_date, ))
                conn.commit()
                cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                   (bookid,))
                book_name = cursor.fetchone()
                print(f"Вы добавили отзыв на книгу {book_name[0]}. ")
                cursor.close()
                break


def DeleteFromFavorites(conn, userid, bookid):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Favorites WHERE user_id = ? AND book_id = ?",
                   (userid[0], bookid, ))
    favorite = cursor.fetchone()
    if(favorite):
        cursor.execute("DELETE FROM Favorites WHERE user_id = ? AND book_id = ?",
                   (userid[0], bookid, ))
        conn.commit()
        cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                   (bookid,))
        book_name = cursor.fetchone()
        print (f"Вы удалили книгу {book_name[0]} из избранного.")
        cursor.close
    else:
        print("Эта книга не находиться у вас в избранном.")
        cursor.close()
        return


def AddToFavorites(conn, userid, bookid):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Favorites WHERE user_id = ? AND book_id = ?",
                   (userid[0], bookid, ))
    favorite = cursor.fetchone()
    if(favorite):
        print("Вы уже добавили эту книгу в избранное.")
        cursor.close()
        return
    else:
        cursor.execute("INSERT INTO Favorites(user_id, book_id) VALUES(?, ?)",
                   (userid[0], bookid, ))
        conn.commit()
        cursor.execute("SELECT book_title FROM Books WHERE book_id = ?",
                   (bookid,))
        book_name = cursor.fetchone()
        print (f"Вы добавили книгу {book_name[0]} в избранное.")
        cursor.close


def ShowBookInfo(conn, bookid):
    cursor = conn.cursor()
    cursor.execute("SELECT genre_id FROM Books WHERE book_id = ?",
                         (bookid,))
    genre_id = cursor.fetchone()
    cursor.execute("SELECT publisher_id FROM Books WHERE book_id = ?",
                         (bookid,))
    publisher_id = cursor.fetchone()
    cursor.execute("SELECT * FROM Genres WHERE genre_id = ?",
                         (genre_id[0],))
    genre = cursor.fetchone()
    cursor.execute("SELECT * FROM Publishers WHERE publisher_id = ?",
                         (publisher_id[0],))
    publisher = cursor.fetchone()
    cursor.execute("SELECT * FROM Books WHERE book_id = ?",
                         (bookid,))
    book = cursor.fetchone()
    cursor.execute("SELECT author_id FROM AuthorsBooks WHERE book_id = ?",
                        (bookid,))
    authors_ids = cursor.fetchall()
    authors=[]
    for author_id in authors_ids:
        cursor.execute("SELECT * FROM Authors WHERE author_id = ?",
                        (author_id[0],))
        authors.append(cursor.fetchone())
    print(f"Название книги: {book[3]}")
    print("Автор(ы) книги:")
    for author in authors:
        print(f"{author[1]} {author[2]}")
    print(f"Жанр: {genre[1]}")
    print(f"Издатель: {publisher[1]}")
    print(f"ISBN: {book[4]}")
    print(f"Дата публикации: {book[5]}")
    print(f"Описание: {book[6]}")
    cursor.close()


def UserBooksActionSelector(conn, userid, bookid):
    cursor = conn.cursor()
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y-%m-%d")
    cursor.execute("UPDATE BookReports SET views = views + 1, report_date = ? WHERE book_id = ?",
                   (formatted_date, bookid))
    conn.commit()
    while True:
        print("Доступные действия:")
        print("1.Просмотреть информацию о книге")
        print("2.Добавить книгу в избранное")
        print("3.Удалить книгу из избранного")
        print("4.Добавить отзыв на книгу")
        print("5.Удалить отзыв на книгу")
        print("6.Изменить отзыв на книгу")
        print("7.Просмотреть отзывы на книгу")
        print("8.Взять копию книги")
        print("9.Возврат в предыдущее меню")
        choice = input("Выберите действие(1/2/3/4/5/6/7/8/9): ")
        if(choice=='1'):
            ShowBookInfo(conn, bookid)
        elif(choice=='2'):
            AddToFavorites(conn, userid, bookid)
        elif(choice=='3'):
            DeleteFromFavorites(conn, userid, bookid)
        elif(choice=='4'):
            AddReview(conn, userid, bookid)
        elif(choice=='5'):
            DeleteReview(conn, userid, bookid)
        elif(choice=='6'):
            ChangeReview(conn, userid, bookid)
        elif(choice=='7'):
            ShowBookReviews(conn, bookid)
        elif(choice=='8'):
            TakeBookCopy(conn, userid, bookid)
        elif(choice=='9'):
            break
        else:
            print('Некорректный ввод. Повторите попытку.')


def ShowBooksByNoCriteria(conn, userid):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books ORDER BY book_title ASC")
    books=cursor.fetchall()
    bookscount = len(books)
    if(bookscount==0):
        print("Книги отсутствуют")
        cursor.close()
        return
    else:
        while True:
            print("Результаты поиска")
            number = 1
            for book in books:
                print(f"{number}. {book[3]}")
                number = number + 1
            choice=input("Выберите номер книги в списке для дальнейших действий (для выхода в предыдущее меню введите -1): ")
            try:
                choicenumber= int(choice)
            except ValueError:
                print('Некорректный ввод. Повторите попытку.')
                continue
            if(choice=='-1'):
                break
            elif(choicenumber not in range(1, bookscount+1)):
                print('Некорректный ввод. Повторите попытку.')
            else:
                print(f"Выбранная книга: {books[choicenumber-1][3]}")
                bookid=books[choicenumber-1][0]
                UserBooksActionSelector(conn, userid, bookid)
    cursor.close()


def ShowBooksByGenre(conn, userid, genreid):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books WHERE genre_id = ?",
                   (genreid,))
    books=cursor.fetchall()
    bookscount = len(books)
    if(bookscount==0):
        print("Книги в данном жанре отсутствуют")
        cursor.close()
        return
    else:
        while True:
            print("Результаты поиска")
            number = 1
            for book in books:
                print(f"{number}. {book[3]}")
                number = number + 1
            choice=input("Выберите номер книги в списке для дальнейших действий (для выхода в предыдущее меню введите -1): ")
            try:
                choicenumber= int(choice)
            except ValueError:
                print('Некорректный ввод. Повторите попытку.')
                continue
            if(choice=='-1'):
                break
            elif(choicenumber not in range(1, bookscount+1)):
                print('Некорректный ввод. Повторите попытку.')
            else:
                print(f"Выбранная книга: {books[choicenumber-1][3]}")
                bookid=books[choicenumber-1][0]
                UserBooksActionSelector(conn, userid, bookid)
    cursor.close()


def ShowBooksByAuthor(conn, userid, authorid):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM AuthorsBooks WHERE author_id = ?",
                   (authorid,))
    authorsbooks=cursor.fetchall()
    books = []
    book = ()
    for authorbook in authorsbooks:
        cursor.execute("SELECT * FROM Books WHERE book_id = ?",
                   (authorbook[2],))
        book = cursor.fetchone()
        books.append(book)
    bookscount = len(books)
    if bookscount == 0:
        print("У этого автора нет книг.")
        cursor.close()
        return
    else:
        while True:
            print("Результаты поиска")
            number = 1
            for book in books:
                print(f"{number}. {book[3]}")
                number = number + 1
            choice=input("Выберите номер книги в списке для дальнейших действий (для выхода в предыдущее меню введите -1): ")
            try:
                choicenumber= int(choice)
            except ValueError:
                print('Некорректный ввод. Повторите попытку.')
                continue
            if(choice=='-1'):
                break
            elif(choicenumber not in range(1, bookscount+1)):
                print('Некорректный ввод. Повторите попытку.')
            else:
                print(f"Выбранная книга: {books[choicenumber-1][3]}")
                bookid=books[choicenumber-1][0]
                UserBooksActionSelector(conn, userid, bookid)
    cursor.close()

    
def GetBooksByGenre(conn, userid):
    cursor = conn.cursor()
    cursor.execute("SELECT* FROM Genres;")
    genres=cursor.fetchall()
    genrescount=len(genres)
    while True:
        print("Жанры")
        for genre in genres:
            print(f"{genre[0]}. {genre[1]}")
        choice=input("Выберите номер жанра для поиска (для выхода в предыдущее меню введите -1): ")
        try:
            choicenumber= int(choice)
        except ValueError:
            print('Некорректный ввод. Повторите попытку.')
            continue
        if(choice=='-1'):
            break
        elif(choicenumber not in range(1, genrescount+1)):
            print('Некорректный ввод. Повторите попытку.')
        else:
            print(f"Выбранный жанр: {genres[choicenumber-1][1]}")
            genreid=genres[choicenumber-1][0]
            ShowBooksByGenre(conn, userid, genreid)
    cursor.close()


def GetBooksByAuthor(conn, userid):
    cursor = conn.cursor()
    cursor.execute("SELECT* FROM Authors;")
    authors=cursor.fetchall()
    authorscount=len(authors)
    print("Авторы")
    while True:
        number = 1
        for author in authors:
            print(f"{number}. {author[1]} {author[2]}")
            number = number + 1
        choice=input("Выберите номер автора для поиска (для выхода в предыдущее меню введите -1): ")
        try:
            choicenumber= int(choice)
        except ValueError:
            print('Некорректный ввод. Повторите попытку.')
            continue
        if(choice=='-1'):
            break
        elif(choicenumber not in range(1, authorscount+1)):
            print('Некорректный ввод. Повторите попытку.')
        else:
            print(f"Выбранный автор: {authors[choicenumber-1][1]} {authors[choicenumber-1][2]}")
            authorid=authors[choicenumber-1][0]
            ShowBooksByAuthor(conn, userid, authorid)
    cursor.close()    
    

def SearchBookCriteriaSelector(conn, userid):
    while True:
        print("Критерии поиска")
        print("1.Без критериев (все, по алфавиту)")
        print("2.Жанр")
        print("3.Автор")
        print("4.Выход из меню поиска книг")
        choice=input("Выберите действие(1/2/3/4):")
        if choice=='1':
            ShowBooksByNoCriteria(conn, userid)
        elif choice=='2':
            GetBooksByGenre(conn, userid)
        elif choice=='3':
            GetBooksByAuthor(conn, userid)
        elif choice =='4':
            break
        else:
            print("Некорректный ввод. Повторите попытку.")


def ChangeUserPasswordChecker():
    while True:
        pass1=input("Введите новый пароль: ")
        pass2=input("Подтвердите новый пароль: ")
        if(pass1==pass2):
            return pass1
        else:
            print("Введённые пароли не совпадают.")

def ChangeUserPassword(conn, userid):
    password=input("Введите ваш пароль: ")
    cursor = conn.cursor()
    cursor.execute("SELECT passwrd FROM Users WHERE user_id = ?;",
                   (userid[0],))
    real_password=cursor.fetchone()
    if(password!=real_password[0]):
        print("Неверный пароль.")
    else:
        new_pass=ChangeUserPasswordChecker()
        cursor.execute("UPDATE Users SET passwrd = ? WHERE user_id = ?;",
                       (new_pass, userid[0],))
        print("Пароль изменён.")
        conn.commit()
    cursor.close()

def ChangeUserEmailAdress(conn, userid):
    password=input("Введите ваш пароль: ")
    cursor = conn.cursor()
    cursor.execute("SELECT passwrd FROM Users WHERE user_id = ?;",
                   (userid[0],))
    real_password=cursor.fetchone()
    if(password!=real_password[0]):
        print("Неверный пароль.")
    else:
        new_adress=input("Введите новый адрес электронной почты: ")
        cursor.execute("UPDATE Users SET email_adress = ? WHERE user_id = ?;",
                       (new_adress, userid[0],))
        print("Адрес электронной почты изменён.")
        conn.commit()
    cursor.close()

def ChangeUserSecondName(conn, userid):
    password=input("Введите ваш пароль: ")
    cursor = conn.cursor()
    cursor.execute("SELECT passwrd FROM Users WHERE user_id = ?;",
                   (userid[0],))
    real_password=cursor.fetchone()
    if(password!=real_password[0]):
        print("Неверный пароль.")
    else:
        new_secname=input("Введите новую фамилию: ")
        cursor.execute("UPDATE Users SET last_name = ? WHERE user_id = ?;",
                       (new_secname, userid[0],))
        print("Фамилия изменена.")
        conn.commit()
    cursor.close()

def ChangeUserFirstName(conn, userid):
    password=input("Введите ваш пароль: ")
    cursor = conn.cursor()
    cursor.execute("SELECT passwrd FROM Users WHERE user_id = ?;",
                   (userid[0],))
    real_password=cursor.fetchone()
    if(password!=real_password[0]):
        print("Неверный пароль.")
    else:
        new_name=input("Введите новое имя: ")
        cursor.execute("UPDATE Users SET first_name = ? WHERE user_id = ?;",
                       (new_name, userid[0],))
        print("Имя изменено.")
        conn.commit()
    cursor.close()

def ChangeUserInfoSelector(conn, userid):
    while True:
        print("1.Изменить имя")
        print("2.Изменить фамилию")
        print("3.Изменить адрес электронной почты")
        print("4.Изменить пароль")
        print("5.Выход из меню изменения")
        choice = input("Выберите действие(1/2/3/4/5): ")
        if choice=='1':
            ChangeUserFirstName(conn, userid)
        elif choice=='2':
            ChangeUserSecondName(conn, userid)
        elif choice=='3':
            ChangeUserEmailAdress(conn, userid)
        elif choice=='4':
            ChangeUserPassword(conn, userid)
        elif choice=='5':
            break
        else:
            print("Некорректный ввод. Повторите попытку.")


        

def ShowUserInfo(conn, userid):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id = ?;",
                   (userid[0],))
    userinfo=cursor.fetchone()
    cursor.execute("SELECT * FROM LibraryCards WHERE user_id = ?;",
                   (userid[0],))
    usercard=cursor.fetchone()
    print(f"Ваше имя: {userinfo[1]}")
    print(f"Ваша фамилия: {userinfo[2]}")
    print(f"Ваш адрес электронной почты: {userinfo[3]}")
    print(f"Ваша дата регистрации: {userinfo[5]}")
    print(f"Ваш номер библиотечной карты: {usercard[1]}")
    print(f"Дата выдачи вашей библиотечной карты: {usercard[2]}")
    print(f"Срок годности вашей библиотечной карты: {usercard[3]}")


def MyFavorites(conn, userid):
    print("Список избранного")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Favorites WHERE user_id = ?;",
                   (userid[0],))
    favorites = cursor.fetchall()
    if(len(favorites)==0):
        print("У вас нет избранных книг\n")
        cursor.close()
        return
    book=()
    number = 1
    for favorite in favorites:
        cursor.execute("SELECT * FROM Books WHERE book_id = ?;",
                   (favorite[2],))
        book=cursor.fetchone()
        print(f"{number}. {book[3]}")
        number = number+1
    print("\n")
    cursor.close()
        

def Notification(conn, userid):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Borrows WHERE user_id = ?;",
                   (userid[0],))
    borrow = cursor.fetchone()
    if(borrow is None):
        print("У вас нет взятой книги.")
        cursor.close()
        return
    datedb = borrow[1]
    date1 = datetime.strptime(datedb, "%Y-%m-%d")
    dateweneed = date1 + timedelta(days=30 * 3)
    print(f"Срок добросовестной сдачи взятой копии книги: {dateweneed}")
    cursor.close()


def ReturnBookCopy(conn, userid):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Borrows WHERE user_id = ?;",
                   (userid[0],))
    borrow = cursor.fetchone()
    if(borrow is None):
        print("У вас нет взятой книги.")
        cursor.close()
        return
    cursor.execute("DELETE FROM Borrows WHERE user_id = ?;",
                   (userid[0],))
    conn.commit()
    print("Вы вернули копию книги.")
    cursor.close()
    


def ReaderMenu(conn, userid):
    while True:
        print("1.Просмотреть информацию о вашем профиле")
        print("2.Изменить информацию о вашем профиле")
        print("3.Поиск книг и действия с ними")
        print("4.Список ваших избранных книг")
        print("5.Уведомление о сроке сдачи книги")
        print("6.Вернуть взятую книгу")
        print("7.Выход")
        choice = input("Выберите действие(1/2/3/4/5/6/7): ")
        if choice=='1':
            ShowUserInfo(conn, userid)
        elif choice=='2':
            ChangeUserInfoSelector(conn, userid)
        elif choice=='3':
            SearchBookCriteriaSelector(conn, userid)
        elif choice=='4':
            MyFavorites(conn, userid)
        elif choice=='5':
            Notification(conn, userid)
        elif choice=='6':
            ReturnBookCopy(conn, userid)
        elif choice=='7':
            break
        else:
           print("Некорректный ввод. Повторите попытку.")


def AddBook(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT* FROM Genres;")
    genres=cursor.fetchall()
    genrescount=len(genres)
    while True:
        for genre in genres:
            print(f"{genre[0]}. {genre[1]}")
        choice=input("Выберите номер жанра для книги: ")
        try:
            choicenumber= int(choice)
        except ValueError:
            print('Некорректный ввод. Повторите попытку.')
            continue
        if(choicenumber not in range(1, genrescount+1)):
            print('Некорректный ввод. Повторите попытку.')
        else:
            print(f"Выбранный жанр: {genres[choicenumber-1][1]}")
            genreid=genres[choicenumber-1][0]
            break
    cursor.execute("SELECT* FROM Authors;")
    authors=cursor.fetchall()
    authorscount=len(authors)
    while True:
        number = 1
        for author in authors:
            print(f"{number}. {author[1]} {author[2]}")
            number = number + 1
        choice=input("Выберите номер автора для книги: ")
        try:
            choicenumber= int(choice)
        except ValueError:
            print('Некорректный ввод. Повторите попытку.')
            continue
        if(choicenumber not in range(1, authorscount+1)):
            print('Некорректный ввод. Повторите попытку.')
        else:
            print(f"Выбранный автор: {authors[choicenumber-1][1]} {authors[choicenumber-1][2]}")
            authorid=authors[choicenumber-1][0]
            break
    cursor.execute("SELECT* FROM Publishers;")
    publishers=cursor.fetchall()
    publisherscount=len(publishers)
    while True:
        number = 1
        for publisher in publishers:
            print(f"{number}. {publisher[1]}")
            number = number + 1
        choice=input("Выберите номер издателя для книги: ")
        try:
            choicenumber= int(choice)
        except ValueError:
            print('Некорректный ввод. Повторите попытку.')
            continue
        if(choicenumber not in range(1, publisherscount+1)):
            print('Некорректный ввод. Повторите попытку.')
        else:
            print(f"Выбранный издатель: {publishers[choicenumber-1][1]}")
            publisherid=publishers[choicenumber-1][0]
            break    
    title = input("Введите название книги: ")
    isbn = input("Введите ISBN: ")
    while True:
        date = input("Введите дату публикации в формате yyyy-mm-dd: ")
        try:
            date_object = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            input("Дата введена некорректно.")
            continue
        break
    description = input("Введите описание книги: ")
    cursor.execute("INSERT INTO Books(genre_id, publisher_id, book_title, isbn_title, publication_date, book_description) VALUES (?, ?, ?, ?, ?, ? );",
                   (genreid, publisherid, title, isbn, date_object.date(), description,))
    conn.commit()
    cursor.execute("SELECT * FROM Books WHERE book_title = ?",
                   (title,))
    book = cursor.fetchone()
    cursor.execute("INSERT INTO AuthorsBooks(author_id, book_id ) VALUES (?, ?)",
                   (authorid, book[0], ))
    conn.commit()
    print('Книга успешно добавлена.')


def GetBookReport(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books=cursor.fetchall()
    bookscount = len(books)
    if(bookscount==0):
        print("Книги отсутствуют")
        cursor.close()
        return
    else:
        while True:
            number = 1
            for book in books:
                print(f"{number}. {book[3]}")
                number = number + 1
            choice=input("Выберите номер книги в списке для генерации отчёта: ")
            try:
                choicenumber= int(choice)
            except ValueError:
                print('Некорректный ввод. Повторите попытку.')
                continue
            if(choicenumber not in range(1, bookscount+1)):
                print('Некорректный ввод. Повторите попытку.')
            else:
                bookid=books[choicenumber-1][0]
                cursor.execute("SELECT * FROM BookReports WHERE book_id = ?",
                               (bookid,))
                report = cursor.fetchone()
                print(f"Отчёт по книге {books[choicenumber-1][3]} :")
                print(f"Кол-во просмотров страницы книги: {report[2]}")
                print(f"Кол-во взятий копий это книги: {report[4]}")
                print(f"Дата отчёта: {report[3]}")
                break
    cursor.close()


def GetSystemReport(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UserActionLogs")
    logs = cursor.fetchall()
    print("СИСТЕМНЫЙ ОТЧЁТ О ДЕЙСТВИЯХ")
    for log in logs:
        print(f"Пользователь с системным ID {log[1]} совершил действие({log[2]}) {log[3]}")


def AddAuthor(conn):
    author_first_name = input("Введите имя автора: ")
    author_last_name = input("Введите фамилию автора: ")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Authors(author_first_name, author_last_name) VALUES(?, ?)",
                   (author_first_name, author_last_name))
    conn.commit()
    print("Автор добавлен.")
    cursor.close()


def AdminMenu(conn):
    while True:
        print("1. Добавить автора")
        print("2. Добавить книгу")
        print("3. Сгенерировать отчёт о книге")
        print("4. Сгенерировать отчёт о действиях в системе")
        print("5. Выход")
        choice = input("Выберите действие(1/2/3/4/5): ")
        if choice=='1':
            AddAuthor(conn)
        elif choice=="2":
            AddBook(conn)
        elif choice =='3':
            GetBookReport(conn)
        elif choice == "4":
            GetSystemReport(conn)
        elif choice == '5':
            break
        else:
            print("Некорректный ввод. Повторите попытку.")


def RoleDecider(conn, userid):
    cursor = conn.cursor()
    cursor.execute("SELECT role_id FROM Users WHERE user_id = ?;",
                   (userid[0],))
    role_id=cursor.fetchone()
    if role_id[0]==1:
        print("Вы вошли в систему как администратор.")
        AdminMenu(conn)
    elif role_id[0]==2:
        print("Вы вошли в систему как читатель.")
        ReaderMenu(conn, userid)
    cursor.close()

def RegPasswordChecker():
    while True:
        pass1=input("Введите ваш пароль: ")
        pass2=input("Подтвердите ваш пароль: ")
        if(pass1==pass2):
            return pass1
        else:
            print("Введённые пароли не совпадают.")

def RegUser(conn, first_name, second_name, email, password):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE email_adress = ?;",
                   (email,))
    existing_user=cursor.fetchone()
    if existing_user:
        print("Пользователь с таким адресом электронной почты уже существует.")
        return
    else:
        role_id=2
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO Users(first_name, last_name, email_adress, passwrd, reg_date, role_id) VALUES (?, ?, ?, ?, ?, ?);",
                       (first_name, second_name, email, password, formatted_date, role_id,))
        conn.commit()
        print("Вы успешно зарегистрированы.")
    cursor.close()

def LoginUser(conn, email, password):
    cursor=conn.cursor()
    cursor.execute("SELECT user_id FROM Users WHERE email_adress = ? and passwrd = ?",
                   (email, password))
    existing_user=cursor.fetchone()
    if existing_user:
        print("Вы успешно вошли в систему.")
        RoleDecider(conn, existing_user)
    else:
        print("Неверный адрес электронной почты или пароль")
    cursor.close()

def StartMenu(conn):
    print("Электронная библиотека")
    while True:
        print("1.Зарегистрироваться")
        print("2.Войти")
        print("3.Выход")
        choice = input("Выберите действие(1/2/3): ")
        if choice == "1":
            first_name=input("Введите ваше имя: ")
            second_name=input("Введите вашу фамилию: ")
            email=input("Введите адрес вашей электронной почты: ")
            password=RegPasswordChecker()
            RegUser(conn, first_name, second_name, email, password)
        elif choice =='2':
            email=input("Введите адрес вашей электронной почты: ")
            password=input("Введите ваш пароль: ")
            LoginUser(conn, email, password)
        elif choice=='3':
            break
        else:
            print("Некорректный ввод. Повторите попытку.")

conn = sqlite3.connect('Library.db')
StartMenu(conn)
conn.close()
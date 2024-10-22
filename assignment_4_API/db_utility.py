import mysql.connector
from config import USER, HOST, PASSWORD


class DbConnectionError(Exception):
    pass


def connecting_db(db_name):
    conx = mysql.connector.connect(
        user=USER,
        host=HOST,
        password=PASSWORD,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return conx


def find_book(book_name):
    try:
        db_name = 'book_share'
        db_connection = connecting_db(db_name)
        cur = db_connection.cursor()
        args = (book_name,)
        cur.callproc('search_book', args)
        book_result = None
        for result in cur.stored_results():
            book_result = result.fetchone()
        cur.close()
        if book_result:
            return True
        else:
            return False

    except Exception:
        raise DbConnectionError("Failed to read data from DB")
        return False

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def reserve_book(_book_name, _user_name, _reserved_until):
    args = (_book_name, _user_name, _reserved_until)
    # result = None

    try:
        db_name = 'book_share'
        db_connection = connecting_db(db_name)
        cur = db_connection.cursor()
        cur.callproc('add_book_reserve', args)
        # result = cur.stored_results()
        db_connection.commit()
        cur.close()
        return True

    except Exception as error:
        print("Database Update Failed !: {}".format(error))
        db_connection.rollback()
        return False

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")


def cancel_reserved_book(book_name, user_name):
    try:
        db_name = 'book_share'
        db_connection = connecting_db(db_name)
        cur = db_connection.cursor()

        book_query = f"SELECT book_id FROM book WHERE book_name = '{book_name}'"
        cur.execute(book_query)
        book_id = cur.fetchone()
        book_fetch = book_id[0]

        user_query = f"SELECT user_id FROM users WHERE user_name = '{user_name}'"
        cur.execute(user_query)
        user_id = cur.fetchone()
        user_fetch = user_id[0]

        cur.execute(
            f'SELECT book_id, user_id FROM book_reserved WHERE book_id = {book_fetch} AND user_id = {user_fetch}')
        fetched_value = cur.fetchone()
        result = fetched_value[0]
        if result:
            args = (book_name, user_name)
            cur.callproc('cancel_book_reserve', args)
            db_connection.commit()
            cur.close()
            return True
        else:
            return False

    except Exception as error:
        print("Database Update Failed !: {}".format(error))
        db_connection.rollback()
        return False

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection is closed")

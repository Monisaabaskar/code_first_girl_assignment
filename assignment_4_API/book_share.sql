CREATE DATABASE IF NOT EXISTS book_share;
USE book_share;

CREATE TABLE IF NOT EXISTS users (
	user_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS author (
	author_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    author_name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS book (
	book_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    book_name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS author_to_book (
	id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    CONSTRAINT
    FOREIGN KEY (book_id)
    REFERENCES book(book_id),
	FOREIGN KEY (author_id)
    REFERENCES author(author_id)
);


CREATE TABLE IF NOT EXISTS book_stock(
	stock_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
	CONSTRAINT
    FOREIGN KEY(book_id)
    REFERENCES book(book_id)
);

CREATE TABLE IF NOT EXISTS book_reserved(
	reserved_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL UNIQUE,
    user_id INT NOT NULL,
    reserved_until DATE NOT NULL,
	CONSTRAINT
    FOREIGN KEY(book_id)
    REFERENCES book(book_id),
	CONSTRAINT
    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
);

DELIMITER //
CREATE PROCEDURE add_user (
	IN _user_name VARCHAR(100))
BEGIN
	INSERT INTO users (user_name) VALUES(_user_name);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE search_book (
	IN _book_name VARCHAR(100))
BEGIN
	SELECT book_name
	FROM book
	WHERE book_name = _book_name;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE add_author_book (
	IN _book_name VARCHAR(100),
	IN _author_name VARCHAR(100))
BEGIN

	DECLARE _book_id INT;
    DECLARE _author_id INT;

    INSERT  INTO book (book_name) VALUES (_book_name);
    INSERT  INTO author (author_name) VALUES (_author_name);

    (SELECT book_id INTO _book_id FROM book WHERE book_name = _book_name);
    (SELECT author_id INTO _author_id FROM author WHERE author_name = _author_name);

	INSERT INTO author_to_book (book_id, author_id) VALUES(_book_id, _author_id);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE add_book_stock (
	IN _book_name VARCHAR(100))
BEGIN
	DECLARE _book_id INT;

    (SELECT book_id INTO _book_id FROM book WHERE book_name = _book_name);

	INSERT INTO book_stock ( book_id) VALUES( _book_id);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE add_book_reserve(
	IN _book_name VARCHAR(100),
    IN _user_name VARCHAR(100),
    IN _reserved_until DATE )
BEGIN
	DECLARE _book_id INT;
    DECLARE _user_id INT;

    (SELECT book_id INTO _book_id FROM book WHERE book_name = _book_name);
    (SELECT user_id INTO _user_id FROM users WHERE user_name = _user_name);

	INSERT
    INTO book_reserved (user_id, book_id, reserved_until)
	VALUES(_user_id, _book_id, _reserved_until);

	DELETE FROM book_stock WHERE book_id = _book_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE cancel_book_reserve(
	IN _book_name VARCHAR(100),
    IN _user_name VARCHAR(100))
BEGIN
	DECLARE _book_id INT;
    DECLARE _user_id INT;

    (SELECT book_id INTO _book_id FROM book WHERE book_name = _book_name);
	(SELECT user_id INTO _user_id FROM users WHERE user_name = _user_name);

	DELETE
    FROM book_reserved
    WHERE (book_id = _book_id
		   AND user_id = _user_id);

    INSERT
    INTO book_stock(book_id)
	VALUES (_book_id);
END //
DELIMITER ;

CALL add_author_book("The Three-Body Problem", "Liu Cixin");
CALL add_author_book("Dune", "Frank Herbert");
CALL add_author_book("Stories of Your Life and Others", "Ted Chiang");
CALL add_author_book("White Wolf and Other Stories", "TC Baker ");
CALL add_author_book("The Stand", "Stephen King ");
CALL add_author_book("The Book Thief", "Markus Zusak");
CALL add_author_book("Harbinger", " P.A. Vasey");

CALL add_book_stock("Stories of Your Life and Others");
CALL add_book_stock("The Three-Body Problem");
CALL add_book_stock("Dune");
CALL add_book_stock("White Wolf and Other Stories");
CALL add_book_stock("The Stand");
CALL add_book_stock("The Book Thief");
CALL add_book_stock("Harbinger");

CALL add_user("moni");
CALL add_user("hari");

select * from book;
select * from users;
select * from book_reserved;
select * from book_stock;
select * from author_to_book;

CALL add_book_reserve("Dune", "moni", "2022-08-09");
CALL cancel_book_reserve("Dune", "moni");
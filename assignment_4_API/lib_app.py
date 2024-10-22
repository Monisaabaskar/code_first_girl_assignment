from flask import Flask, jsonify, request
from db_utility import find_book, reserve_book, cancel_reserved_book

import datetime

lib_app = Flask(__name__)


class DbConnectionError(Exception):
    pass


@lib_app.route('/')
def home():
    return "Welcome to the Book share!"


# checking for the book
@lib_app.route('/book_availability', methods=['GET'])
def book_availability():
    required_book = request.args.get("book_name")

    if not required_book:
        return jsonify({"error": "book_name is required"}), 400
    try:
        book_exist = find_book(required_book)
        return jsonify({"exists": book_exist}), 200

    except DbConnectionError as error:
        return jsonify({"error": f"{error}"}), 500


@lib_app.route('/reserve_book', methods=['POST'])
def book_reservation():
    data = request.get_json()

    if not ("book_name" in data and "user_name" in data and "reserved_until" in data):
        return jsonify({"error": "Parameters book_name, user_name and reserved_until are required"})

    book_name = data['book_name']
    user_name = data['user_name']
    reserved_until = datetime.datetime.strptime(data['reserved_until'], "%Y-%m-%d").date()

    try:
        successful_reservation = reserve_book(book_name, user_name, reserved_until)
        if successful_reservation:
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "Failed to reserve the book"}), 500
    except DbConnectionError as error:
        return jsonify({"error": f"{error}"}), 500


@lib_app.route('/book_cancellation', methods=['POST'])
def book_cancellation():
    data = request.get_json()
    book_name = data['book_name']
    user_name = data['user_name']

    if not (book_name and user_name):
        return jsonify({"error": "All parameters (book_name, user_name) are required"}), 400

    try:
        book_cancellation = cancel_reserved_book(book_name, user_name)

        if book_cancellation:
            return jsonify({"success": True}), 200

        else:
            return jsonify({"error": "Failed to reserve the book"}), 500

    except DbConnectionError as error:
        return jsonify({"error": f"{error}"}), 500


if __name__ == '__main__':
    lib_app.run(debug=True, port=5000)

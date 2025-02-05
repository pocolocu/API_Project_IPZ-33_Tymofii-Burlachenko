from flask import Flask, request, jsonify

app = Flask(__name__)

# Начальный список книг
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960}
]

# Главная страница для проверки
@app.route('/')
def home():
    return "Welcome to the Library API!"

# Получение всех книг
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Получение конкретной книги по ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book)

# Добавление новой книги
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()

    # Проверка наличия ID
    if not new_book.get("id"):
        return jsonify({"error": "ID is required"}), 400

    # Проверка уникальности ID
    if any(book["id"] == new_book["id"] for book in books):
        return jsonify({"error": "Book with this ID already exists"}), 400

    books.append(new_book)
    return jsonify(new_book), 201

# Обновление информации о книге
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    updated_data = request.get_json()
    book.update(updated_data)
    return jsonify(book)

# Удаление книги
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)  # Исправлено "idx" -> "id"
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=7689)

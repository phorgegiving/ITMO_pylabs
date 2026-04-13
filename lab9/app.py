from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#бд
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Book {self.name} — {self.author}>'

#маршруты

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        author = request.form.get('author', '').strip()
        name = request.form.get('name', '').strip()

        if author and name:
            new_book = Book(author=author, name=name)
            db.session.add(new_book)
            db.session.commit()

        return redirect(url_for('index'))

    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/clear', methods=['POST'])
def clear():
    Book.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
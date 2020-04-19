import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.String(80), unique=False, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return "<Title: {}><Price: {}><Author: {}>".format(self.title, self.price, self.author)


@app.route("/save", methods=["POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"),
                        price=request.form.get("price"),
                        author=request.form.get("author"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)

    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/get", methods=["GET"])
def update():
    try:
        books = Book.query.all()
        return render_template("view.html", books=books)
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add')
def add():
    return render_template("add.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

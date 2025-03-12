from flask import Blueprint, render_template, redirect, url_for, request
import os
from werkzeug.utils import secure_filename
from flask_login import login_required
from app import db
from app.models import Author, Book
from app.main.forms import CreateAuthorForm, CreateBookForm

main = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static', 'images')

@main.route('/')
@main.route('/books', methods=['GET', 'POST'])
def all_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@main.route('/book/<int:book_id>', methods=['GET'])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('details.html', book=book)

@main.route('/author/<int:author_id>', methods=['GET'])
def author_details(author_id):
    author = Author.query.get_or_404(author_id)
    books = Book.query.filter_by(author_id=author.id).all()
    return render_template('author_details.html', author=author, books=books)

@main.route('/create_author', methods=['GET', 'POST'])
@login_required
def create_author():
    form = CreateAuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('main.all_books'))
    return render_template('create_author.html', form=form)

@main.route('/create_book', methods=['GET', 'POST'])
@login_required
def create_book():
    form = CreateBookForm()
    form.author_id.choices = [(author.id, author.name) for author in Author.query.all()]
    if form.validate_on_submit():
        image_file = form.image.data

        if image_file and hasattr(image_file, 'filename'):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)
        else:
            filename = 'default.jpg'

        book = Book(
            name=form.name.data,
            description=form.description.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            age_group=form.age_group.data,
            author_id=form.author_id.data,
            image=filename
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('main.all_books'))

    return render_template('create_book.html', form=form)

@main.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = CreateBookForm(obj=book)

    form.author_id.choices = [(author.id, author.name) for author in Author.query.all()]

    if request.method == 'GET':
        form.author_id.data = book.author_id

    if form.validate_on_submit():
        book.name = form.name.data
        book.description = form.description.data
        book.publish_date = form.publish_date.data
        book.price = form.price.data
        book.age_group = form.age_group.data
        book.author_id = int(form.author_id.data)


        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            image_file.save(image_path)
            book.image = filename

        db.session.commit()
        return redirect(url_for('main.all_books'))

    return render_template('create_book.html', form=form, book=book)

@main.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('main.all_books'))

@main.route('/authors/edit/<int:author_id>', methods=['GET', 'POST'])
@login_required
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = CreateAuthorForm(obj=author)

    if form.validate_on_submit():
        author.name = form.name.data
        db.session.commit()
        return redirect(url_for('main.all_books'))

    return render_template('create_author.html', form=form, author=author)

@main.route('/authors/delete/<int:author_id>', methods=['POST'])
@login_required
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('main.all_books'))



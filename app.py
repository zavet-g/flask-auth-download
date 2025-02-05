from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, render_template, url_for, send_from_directory
import hashlib
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_downloader.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Participant {self.name}>'


with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        try:
            login = request.form.get('login')
            password = request.form.get('password')
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            user = db.session.query(Users).filter_by(login=login).first()

            if login and user.password == hashed_password:
                return redirect(url_for('download_page'))

            return 'Ошибка: Неверный логин или пароль', 401

        except Exception as e:
            return f'Произошла ошибка: {e} попробуйте снова', 500

    return render_template('main.html')



@app.route('/download')
def download_page():
    return render_template('download.html')

@app.route('/download/<file_type>')
def download_file(file_type):
    file_map = {'csv': 'sample.csv', 'pdf': 'sample.pdf', 'xlsx': 'sample.xlsx'}

    if file_type not in file_map:
        return 'Файла не существует', 404

    filename = file_map[file_type]
    file_path = os.path.join('files', filename)

    if not os.path.exists(file_path):
        return 'Файл не найден', 404

    return send_from_directory(os.path.dirname(file_path), filename)

if __name__ == '__main__':
    app.run(debug=True)
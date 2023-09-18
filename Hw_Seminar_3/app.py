from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = r'sqlite:///D:\My education\Flask and FastApi\Flask-and-FastAPI\Hw_Seminar_3\users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


@app.route('/')
def index():
    return render_template('index.html', title="Домашнее задание к третьему семинару",
                           subtitle="Фреймворки Flask и FastAPI")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        try:
            user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            return render_template('index.html', message="Пользователь успешно зарегистрирован",
                                   title="Домашнее задание к третьему семинару", subtitle="Фреймворки Flask и FastAPI")

        except:
            error_message = "Пользователь с таким email уже существует."
            return render_template('register.html', error_message=error_message)

    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

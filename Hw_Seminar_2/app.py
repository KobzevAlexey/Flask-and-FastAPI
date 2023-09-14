from flask import Flask, request, make_response, render_template, session, redirect, url_for
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('greeting'))
    else:
        return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username', 'NoName')
        session['email'] = request.form.get('email', 'NoEmail')
        return redirect(url_for('greeting'))

    return render_template('login_form.html')


@app.route('/greeting/')
def greeting():
    if 'username' in session:
        context = {'title': 'Welcome', 'username': session['username'], 'email': session['email']}
        return render_template('greeting.html', **context)
    else:
        return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

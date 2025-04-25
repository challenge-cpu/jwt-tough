from flask import Flask, request, redirect, make_response, render_template, send_from_directory
import jwt
import datetime
import os

app = Flask(__name__)
SECRET = "peshwa1234567890abcdefghijklmnopqrstuvwxyz!@#PESHWA"

# Route to serve robots.txt
@app.route('/robots.txt')
def robots():
    return send_from_directory(os.getcwd(), 'robots.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')

    if username.lower() == 'admin':
        return "You can't impersonate the Peshwa 👑", 403

    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, SECRET, algorithm="HS256")

    resp = make_response(redirect('/dashboard'))
    resp.set_cookie('auth', token)
    return resp

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('auth')
    if not token:
        return redirect('/')

    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        if data.get('user', '').lower() == 'admin':
            return render_template('dashboard.html', flag="PeshwasCTF{cook!3_monst3r_4tt4ck}")
        return f"<h3 style='color:white;text-align:center;margin-top:20vh;'>Welcome, {data['user']}! But you're not admin 😏</h3>"
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

@app.route('/vault-entry')
def vault_entry():
    return render_template('vault.html')

@app.route('/hint')
def hint():
    return render_template('hint.html')

if __name__ == '__main__':
    app.run(debug=True)

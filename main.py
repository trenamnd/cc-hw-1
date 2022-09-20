from flask import Flask, render_template, request, redirect, send_file
from loguru import logger

app = Flask(__name__)

active_users = {}
users = {'noahtren': '112123'}
number_of_words = len(
    open("Limerick.txt").read().replace("\n", " ").split(" "))


@app.route('/', methods=['GET'])
def index():
  if request.remote_addr in active_users:
    username = active_users[request.remote_addr]
  else:
    username = None
  return render_template('index.html',
                         username=username,
                         users=list(users.keys()),
                         number_of_words=number_of_words)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    users[username] = password
    return redirect('/login')
  else:
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    logger.info(users)
    if username in users:
      logger.info(username, password)
      if users[username] == password:
        active_users[request.remote_addr] = username
        return redirect('/')
      else:
        return render_template('login.html', error='Invalid password')
  return render_template('login.html')

@app.route('/download', methods=['GET'])
def download():
  return send_file('Limerick.txt', as_attachment=True)


if __name__ == '__main__':
  app.run(debug=True)
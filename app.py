from flask import Flask, render_template, request, redirect, session
from database import init_db, get_all_messages, add_message, get_message_count, delete_message

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_guestbook'

init_db()

def format_russian_date(date_str):
    months = {
        '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
        '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
        '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
    }
    try:
        parts = date_str.split('-')
        year = parts[0]
        month = months[parts[1]]
        day = str(int(parts[2]))
        return f"{day} {month} {year}"
    except:
        return date_str

@app.route('/')
def index():
    raw_messages = get_all_messages()
    messages = []
    for msg in raw_messages:
        messages.append({
            'id': msg['id'],
            'name': msg['name'],
            'message': msg['message'],
            'created_at': format_russian_date(msg['created_at'])
        })
    count = get_message_count()
    error = request.args.get('error')
    return render_template('index.html', messages=messages, error=error, count=count)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    if not name or not message:
        return redirect('/?error=1')
    add_message(name, message)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == '123':
            session['logged_in'] = True
            session['username'] = 'admin'
            return redirect('/')
        else:
            error = 'Неверный логин или пароль!'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    if not session.get('logged_in'):
        return redirect('/login')
    delete_message(message_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

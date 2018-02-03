from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextAreaField, validators, StringField, PasswordField, IntegerField
import sqlite3

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
user_id = None

class register_form(Form):
    name = StringField('Tu nombre:', validators=[validators.required()])
    password = PasswordField('Contraseña:  ', validators=[validators.required()])
    password2 = PasswordField('Repite la contraseña:', validators=[validators.required()])


class login_form(Form):
    name = StringField('Tu nombre:', validators=[validators.required()])
    password = PasswordField('Contraseña:  ', validators=[validators.required()])

class new_task_form(Form):
    description = TextAreaField('Descripción:', validators=[validators.required()])


def createSqliteObj(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    return conn, c

def createTables():
    conn, c = createSqliteObj('dataBase/dataBase.db')
    sql = 'create table if not exists users (id integer, name text, password text)'
    c.execute(sql)
    conn.commit()

    sql = 'create table if not exists tasks (id integer, user_id integer, date text, ' \
          'description text, status text, priority integer)'
    c.execute(sql)
    conn.commit()

@app.route("/", methods=['GET', 'POST'])
def register():

    form = register_form(request.form)
    print(form.errors)

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        password2 = request.form['password2']

        if form.validate():
            if password == password2:
                # TODO comprobar que el user_name no exista ya
                createUser(name, password)
                return redirect("/tasks")
            else:
                flash('Las contraseñas no coinciden')
                return render_template('register.html', form=form, link=None)
        else:
            flash('All the form fields are required. ')
            return render_template('register.html', form=form, link=None)

    else:
        return render_template('register.html', form=form, link=None)

@app.route("/login", methods=['GET', 'POST'])
def login():

    form = login_form(request.form)
    print(form.errors)

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if form.validate():
            getUserId(name, password)
            if user_id:
                return redirect("/tasks")
            else:
                flash('No hay ningún usuario con esos datos')
                return render_template('login.html', form=form, link=None)
        else:
            flash('All the form fields are required. ')
            return render_template('login.html', form=form, link=None)

    else:
        return render_template('login.html', form=form, link=None)

def getUserId(name, password):
    conn, c = createSqliteObj('dataBase/dataBase.db')
    c.execute('SELECT id FROM users where name = ? and password = ?', (name, password))
    try:
        global user_id
        user_id = c.fetchone()[0]
        print(user_id)
        return user_id
    except:
        user_id = None
        return None



def selectTasks():
    print('SelectTasks, user_id:', user_id)

    conn, c = createSqliteObj('dataBase/dataBase.db')
    c.execute('SELECT * FROM tasks where user_id=?', (user_id,))
    try:
        tasks = c.fetchall()
        # flash(tasks)
        print(tasks)
        q = [n for n in range(len(tasks))]
        tasks = ['|'.join(task[2:-1]) for task in tasks]
        tasks = ';'.join(tasks)
        print(tasks)
        return tasks, q
    except Exception as e:
        print(e)
        flash('Aún no hay tareas')
        print('Aún no hay tareas')
        return None, 0


@app.route("/tasks", methods=['GET', 'POST'])
def renderTasks():
    if not user_id:
        return redirect('/login')
    form = new_task_form(request.form)
    print('form errors', form.errors)

    if request.method == 'POST' and request.form['description']:
        print('request method = post')
        description = request.form['description']
        createTask(description)
    tasks, q = selectTasks()
    return render_template('tasks.html', form=form, tasks=tasks, user_id=user_id, q=q)


def createTask(description):
    conn, c = createSqliteObj('dataBase/dataBase.db')
    c.execute('SELECT id FROM tasks')
    conn.commit()
    try:
        ids = c.fetchall()
        last = ids[-1][0]
        values = (last + 1, user_id, 'hoy', description, 'pendiente', 1)
        c.execute('insert into tasks values (?, ?, ?, ?, ?, ?)', values)
        conn.commit()

    except Exception as e:
        print('error', e)
        values = (1, user_id, 'hoy', description, 'pendiente', 1)
        c.execute('insert into tasks values (?, ?, ?, ?, ?, ?)', values)
        conn.commit()


def createUser(name, password):
    conn, c = createSqliteObj('dataBase/dataBase.db')
    c.execute('SELECT id FROM users')
    global user_id
    try:
        ids = c.fetchall()
        last = ids[-1][0]
        user_id = last+1
        values = (user_id, name, password)
        c.execute('insert into users values (?, ?, ?)', values)
        conn.commit()

    except Exception as e:
        print('error', e)
        user_id = 1
        values = (1, name, password)
        c.execute('insert into users values (?, ?, ?)', values)
        conn.commit()


if __name__ == "__main__":
    createTables()
    app.run()
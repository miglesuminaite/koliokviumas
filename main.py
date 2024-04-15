from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Duomenų failo pavadinimas
TASKS_FILE = 'tasks.txt'

# Funkcija, kuri nuskaito užduotis iš failo
def read_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []

# Funkcija, kuri įrašo užduotis į failą
def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        file.writelines(tasks)

# Pagrindinis puslapis su užduočių sąrašu
@app.route('/')
def index():
    tasks = read_tasks()
    return render_template('index.html', tasks=tasks)

# Pridėti naują užduotį
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = 'Neatlikta'
        user = request.form['user']
        
        with open(TASKS_FILE, 'a') as file:
            file.write(f"{title}|{description}|{status}|{user}\n")
        
        return redirect(url_for('index'))
    return render_template('add_task.html')

# Ištrinti užduotį
@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    tasks = read_tasks()
    del tasks[task_id]
    write_tasks(tasks)
    return redirect(url_for('index'))

# Redaguoti esamą užduotį
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    tasks = read_tasks()
    task_data = tasks[task_id].split('|')
    if request.method == 'POST':
        task_data[0] = request.form['title']
        task_data[1] = request.form['description']
        task_data[3] = request.form['user']
        tasks[task_id] = '|'.join(task_data) + '\n'
        
        write_tasks(tasks)
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task_data, task_id=task_id)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create tables before the first request
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form['todo']
    new_todo = Todo(task=task)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'todos': [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in Todo.query.all()]})

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return jsonify({'todos': [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in Todo.query.all()]})

@app.route('/update/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.completed = not todo.completed  # Toggle completion status
        db.session.commit()
    todos = Todo.query.all()  # Get all todos
    return jsonify({
        'todos': [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in todos]
    })

@app.route('/clear-tasks', methods=['DELETE'])
def clear_tasks():
    db.session.query(Todo).delete()  # Clear all tasks
    db.session.commit()
    return jsonify({'todos': [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in Todo.query.all()]})

@app.route('/clear-completed', methods=['DELETE'])
def clear_completed():
    db.session.query(Todo).filter_by(completed=True).delete()  # Clear only completed tasks
    db.session.commit()
    return jsonify({'todos': [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in Todo.query.all()]})


if __name__ == '__main__':
    app.run(debug=True)

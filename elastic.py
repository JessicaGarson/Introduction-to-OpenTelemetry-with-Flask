from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.contrib.opentelemetry import Tracer
import os


# Initialize Flask app and database configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Elastic APM configuration
app.config['ELASTIC_APM'] = {
  'SERVICE_NAME': 'todo',
  'SECRET_TOKEN': os.environ.get('ELASTIC_APM_SECRET_TOKEN'),
  'SERVER_URL': os.environ.get('ELASTIC_APM_SERVER_ENDPOINT'),
  'ENVIRONMENT': 'my-environment',
  'DEBUG': True,
}

# Initialize Elastic APM monitoring and SQLAlchemy ORM
apm = ElasticAPM(app)
db = SQLAlchemy(app)

# Initialize the OpenTelemetry Tracer
tracer = Tracer(__name__)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)

# Create the tasks database table if not already created
with app.app_context():
    db.create_all()

# HTML template with inline CSS for the to-do list application
HOME_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>To-Do List</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      margin: 40px auto;
      padding: 20px;
      max-width: 600px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    h1 {
      color: #333;
    }
    form {
      margin-bottom: 20px;
    }
    input[type="text"] {
      padding: 10px;
      width: calc(100% - 22px);
      margin-bottom: 10px;
    }
    input[type="submit"] {
      background-color: #5cb85c;
      border: none;
      color: white;
      padding: 10px 20px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      cursor: pointer;
    }
    ul {
      list-style-type: none;
      padding: 0;
    }
    li {
      position: relative;
      padding: 8px;
      background-color: #fff;
      border-bottom: 1px solid #ddd;
    }
    .delete-button {
      position: absolute;
      right: 10px;
      top: 10px;
      background-color: #ff6347;
      color: white;
      border: none;
      padding: 5px 10px;
      border-radius: 5px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <h1>To-Do List</h1>
  <form action="/add" method="post">
    <input type="text" name="task" placeholder="Add new task">
    <input type="submit" value="Add Task">
  </form>
  <ul>
    {% for task in tasks %}
      <li>{{ task.description }} <button class="delete-button" onclick="location.href='/delete/{{ task.id }}'">Delete</button></li>
    {% endfor %}
  </ul>
</body>
</html>
"""

# Route to display the to-do list and input form
@app.route('/', methods=['GET'])
def home():
    with tracer.start_as_current_span("querying_tasks"):
        tasks = Task.query.all()
    return render_template_string(HOME_HTML, tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add():
    task_description = request.form['task']
    new_task = Task(description=task_description)
    with tracer.start_as_current_span("adding_task"):
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))


# Route to delete an existing task
@app.route('/delete/<int:task_id>', methods=['GET'])
def delete(task_id):
    with tracer.start_as_current_span("deleting_task"):
            task_to_delete = Task.query.get(task_id)
            if task_to_delete:
                db.session.delete(task_to_delete)
                db.session.commit()
            return redirect(url_for('home'))


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
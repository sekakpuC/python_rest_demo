from flask import Flask, jsonify, request
from werkzeug.exceptions import abort

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    print('line 29')
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks', methods=['POST','PUT'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):

    if len(tasks) == 0:
        abort(404)
    deleted_task_idx = -1
    for idx, t in enumerate(tasks):
        if task_id == t["id"]:
            deleted_task_idx = idx
            break
    if deleted_task_idx > -1:
        deleted_task = tasks.pop(deleted_task_idx)
    else:
        abort(404)
    return jsonify({'task': deleted_task})


if __name__ == '__main__':
    app.run(debug=True)

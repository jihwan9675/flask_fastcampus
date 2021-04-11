from flask import jsonify, request, Blueprint
import requests
from . import api
from models import Todo, db

@api.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        res = requests.post('https://hooks.slack.com/services/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',
                            json={'text': 'hello world'}, headers={'Content-Type': 'application/json'})

    elif request.method == 'GET':
        pass

    data = request.get_json()
    return jsonify(data)


@api.route('/slack/todos', methods=['POST'])
def slack_todos():
    res = request.form['text'].split(' ')
    cmd, *args = res
    ret_msg = ' '
    if cmd == 'create':
        todo_name = args[0]
        todo = Todo()
        
        todo.title = todo_name
        db.session.add(todo)
        db.session.commit()

        ret_msg = 'todo가 생성되었습니다.'

    elif cmd == 'list':
        todos = Todo.query.all()
        

    return ret_msg

from flask import jsonify, request, Blueprint
import requests
from . import api
from models import Todo, db
import datetime

def send_slack(msg):
    res = requests.post('https://hooks.slack.com/services/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',
                            json={'text': msg}, headers={'Content-Type': 'application/json'})

@api.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'POST':
        send_slack('TODO가 생성되었습니다.') # 사용자 정보, 할일 제목, 기한

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
        send_slack('[%s] %s'%(str(datetime.datetime.now()), todo_name))

    elif cmd == 'list':
        todos = Todo.query.all()
        for idx, todo in enumerate(todos):
            ret_msg += '%d. %s (~ %s)\n'%(idx+1, todo.title, str(todo.tstamp))

    return ret_msg

from flask import jsonify, request, Blueprint, session
import requests
from . import api
from models import Todo, db, Fcuser
import datetime

def send_slack(msg):
    res = requests.post('https://hooks.slack.com/services/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',
                            json={'text': msg}, headers={'Content-Type': 'application/json'})

@api.route('/todos', methods=['GET', 'POST','DELETE'])
def todos():
    userid = session.get('userid', 1)
    if not userid:
        return jsonify(), 401

    if request.method == 'POST':
        data=request.get_json()
        todo = Todo()
        
        todo.title = data.get('title')
        fcuser = Fcuser.query.filter_by(userid=userid).first()
        todo.fcuser_id = fcuser.id
        todo.due = data.get('due')
        todo.status = 0
        db.session.add(todo)
        db.session.commit()

        send_slack('TODO가 생성되었습니다.') # 사용자 정보, 할일 제목, 기한
        
        return jsonify(), 201

    elif request.method == 'GET':
        todos = Todo.query.filter_by(fcuser_id=1)

        return jsonify([t.serialize for t in todos])

    elif request.method == 'DELETE':
        data=request.get_json()
        todo_id = data.get('todo_id')
        todo = Todo.query.filter_by(id=todo_id).first()

        db.session.delete()
        db.session.commit()

        return jsonify(), 203

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

from flask import jsonify, request, Blueprint
import requests
from . import api

@api.route('/todos',methods=['GET','POST'])
def todos():
    if request.method=='POST':
        res = requests.post('https://hooks.slack.com/services/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',json={'text':'hello world'},headers={'Content-Type':'application/json'})


    elif request.method=='GET':
        pass

    data = request.get_json()
    return jsonify(data)


@api.route('/test',methods=['POST'])
def test():
    res = request.form['text']
    print(res)
    
    return jsonify(res)
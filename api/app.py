#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from camera import Camera

auth = HTTPBasicAuth()
app = Flask(__name__)
camera = Camera()

@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unathorized access'}), 401)

@app.route('/todo/api/v1.0/actions',methods=['GET'])
#@auth.login_required
def get_actions():
    return jsonify({'actions': [make_public_action(action) for action in camera.getActions()]})

@app.route('/todo/api/v1.0/actions/<int:action_id>', methods=['GET'])
def get_action(action_id):
    action = camera.getActions(action_id)
    if len(action)==0:
        abort(404)
    return jsonify({'actions':make_public_action(action[0])})

@app.route('/todo/api/v1.0/action', methods=['POST'])
def create_action():
    folder = request.json.get('folder',None)
    time = request.json.get('time',None)
    minutes = request.json.get('minutes',None)
    action = camera.snapPicture(folder=folder, time=time,minutes=minutes)
    return jsonify({'action': str(action)}), 201
#
#@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
#def update_task(task_id):
#    task = [task for task in tasks if task['id'] == task_id]
#    if len(task)==0:
#        abort(404)
#    if not request.json:
#        abort(400)
#    if 'title' in request.json and type(request.json['title']) != unicode:
#        abort(400)
#    if 'description' in request.json and type(request.json['description']) is not unicode:
#        abort(400)
#    if 'done' in request.json and type(request.json['done']) is not bool:
#        abort(400)
#    task[0]['title'] = request.json.get('title', task[0]['title'])
#    task[0]['description'] = request.json.get('description', task[0]['description'])
#    task[0]['done'] = request.json.get('done',task[0]['done'])
#    return jsonify({'task': task[0]})

#@app.route('/todo/api/v1.0/actions/<int:action_id>', methods=['DELETE'])
#def delete_task(task_id):
#    task = [task for task in tasks if task['id'] == task_id]
#    if len(task)==0:
#        abort(404)
#    tasks.remove(task[0])
#    return jsonify({'result': True})

def make_public_action(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
    


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

@app.route('/raspberry-spy/api/v1.0/actions',methods=['GET'])
#@auth.login_required
def get_actions():
    return jsonify({'actions': [make_public_action(action) for action in camera.getActions()]})

@app.route('/raspberry-spy/api/v1.0/actions/<int:action_id>', methods=['GET'])
def get_action(action_id):
    action = camera.getActions(action_id)
    if len(action)==0:
        abort(404)
    return jsonify({'actions':make_public_action(action[0])})

@app.route('/raspberry-spy/api/v1.0/action', methods=['POST'])
def create_action():
    folder = request.json.get('folder',None)
    time = request.json.get('time',None)
    minutes = request.json.get('minutes',None)
    thread = camera.snapPicture(folder=folder, time=time, minutes=minutes)
    action = camera.getActions(thread.threadID)
    return jsonify({'action': make_public_action(action[0])}), 200

@app.route('/raspberry-spy/api/v1.0/tasks/<int:action_id>', methods=['PUT'])
def update_action(action_id):
    actions = camera.getActions([action_id])
    if len(actions)==0:
        abort(404)
    if not request.json:
        abort(400)
    if 'folder' in request.json and type(request.json['folder']) != unicode:
        abort(400)
    if 'time' in request.json and type(request.json['time']) is not unicode:
        abort(400)
    if 'minutes' in request.json and type(request.json['minutes']) is not int:
        abort(400)
    actions[0]['folder'] = request.json.get('folder', actions[0]['folder'])
    actions[0]['time'] = request.json.get('time', actions[0]['time'])
    actions[0]['minutes'] = request.json.get('minutes',actions[0]['minutes'])
    return jsonify({'actions': actions[0]}), 200

@app.route('/raspberry-spy/api/v1.0/actions/<int:action_id>', methods=['DELETE'])
def delete_task(action_id):
    actions = camera.getActions(action_id)
    if len(actions)==0:
        abort(404)
    camera.stopActions(action_id)
    return jsonify({'actions':actions[0]}), 200

def make_public_action(action):
    new_action = {}
    for field in action:
        if field == 'id':
            new_action['uri'] = url_for('get_action', action_id=action['id'], _external=True)
        else:
            new_action[field] = action[field]
    return new_action

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request paramenters'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
    


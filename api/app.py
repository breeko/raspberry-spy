#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from camera import Camera

auth = HTTPBasicAuth()
app = Flask(__name__)
camera = Camera()

@auth.get_password
def get_password(username):
    if username == 'spy':
        return 'raspberry'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unathorized access'}), 401)

@app.route('/raspberry-spy/api/v1.0/jobs',methods=['GET'])
#@auth.login_required
def get_jobs():
    return jsonify({'jobs': [make_public_job(job) for job in camera.get_cron_job()]})

@app.route('/raspberry-spy/api/v1.0/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = camera.get_cron_job(job_id)
    if len(job)==0:
        abort(404)
    return jsonify({'jobs':make_public_job(job[0])})

@app.route('/raspberry-spy/api/v1.0/jobs', methods=['POST'])
def create_job():
    folder = request.json.get('folder',None)
    minute = request.json.get('minute',None)
    hour = request.json.get('hour',None)
    month = request.json.get('month',None)    
    dow = request.json.get('dow',None)
    dom = request.json.get('dom',None)
    response = camera.new_job(folder=folder, minute=minute, hour=hour, month=month, day_of_month=dom, day_of_week=dow)
    return jsonify({'jobs': make_public_job(response)}), 200

@app.route('/raspberry-spy/api/v1.0/tasks/<int:action_id>', methods=['PUT'])
def update_job(action_id):
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

@app.route('/raspberry-spy/api/v1.0/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = camera.get_cron_job(job_id)
    if len(job)==0:
        abort(404)
    jobs = camera.delete_job(job_id)
    return jsonify({'jobs': [make_public_job(job) for job in jobs]}), 200

@app.route('/raspberry-spy/api/v1.0/jobs', methods=['DELETE'])
def delete_all_jobs():
    jobs = camera.delete_job()
    return jsonify({'jobs': [make_public_job(job) for job in jobs]}), 200

def make_public_job(job):
    if job is None: return None

    public_job = {}
    public_job['minute'] = str(job.minute)
    public_job['hour'] = str(job.hour)
    public_job['month'] = str(job.month)
    public_job['day of month'] = str(job.dom)
    public_job['day of week'] = str(job.dow)
    public_job['id'] = str(job.comment)
    return public_job

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request paramenters'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
    



from flask import Flask, render_template, request, url_for,jsonify
from celery import Celery
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Configure Celery to use Redis
#app.config['CELERY_BROKER_URL'] = 'redis://:Zf61JQ5ffQ0nVBE7Vk8RbJZIFHHAeZcr@redis-16168.c8.us-east-1-2.ec2.cloud.redislabs.com:16168'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://:Zf61JQ5ffQ0nVBE7Vk8RbJZIFHHAeZcr@redis-16168.c8.us-east-1-2.ec2.cloud.redislabs.com:16168'
app.config['broker_url'] = 'redis://:Zf61JQ5ffQ0nVBE7Vk8RbJZIFHHAeZcr@redis-16168.c8.us-east-1-2.ec2.cloud.redislabs.com:16168'
app.config['result_backend'] = 'redis://:Zf61JQ5ffQ0nVBE7Vk8RbJZIFHHAeZcr@redis-16168.c8.us-east-1-2.ec2.cloud.redislabs.com:16168'


# Initialize Celery
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# Initialize Celery
celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

# Initialize Flask-SocketIO
socketio = SocketIO(app)

# Define a Celery task for addition
@celery.task(bind=True)
def add(self, x, y):
    result = x + y
    # Emit a message to the client when the task is done
    socketio.emit('task_complete', {'result': result, 'task_id': self.request.id}, room=self.request.id)
    return result

# Route for the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x = int(request.form['x'])
        y = int(request.form['y'])
        task = add.apply_async(args=[x, y])
        return render_template('index.html', task_id=task.id)
    return render_template('index.html')

# Route to display the result

@app.route('/result/<task_id>')
def result(task_id):
    # Just render the result template; the result will be sent via WebSocket
    return render_template('result.html', task_id=task_id)

@app.route('/status/<task_id>')
def task_status(task_id):
    task = add.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'status': task.result  # if SUCCESS, just return the result
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('result', 0) if isinstance(task.info, dict) else task.info
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    socketio.run(app, debug=True)
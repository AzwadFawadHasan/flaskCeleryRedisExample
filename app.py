
from flask import Flask, render_template, request, url_for
from celery import Celery

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure Celery to use Redis

app.config['broker_url'] = 'your url'
app.config['result_backend'] = 'your url'


# Initialize Celery
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

# Define a Celery task for addition
@celery.task(bind=True)
def add(self, x, y):
    return x + y

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
    result = add.AsyncResult(task_id)
    if result.ready():
        return render_template('result.html', result=result.get())
    else:
        return render_template('result.html', result="Waiting for result...", task_id=task_id)

if __name__ == '__main__':
    app.run(debug=True)

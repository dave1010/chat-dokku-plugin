from flask import Flask, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/app-list')
def app_list():
    try:
        result = subprocess.run(['ssh', 'chatdokku@172.17.0.1', 'dokku', 'apps:list'], capture_output=True, text=True, check=True)
        return f"<pre>{result.stdout}</pre>"
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"



@app.route('/self-update')
def self_update():
    def generate():
        process = subprocess.Popen(['/app/api-scripts/self-update.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ''):
            yield line

    return Response(generate(), content_type='text/plain')


if __name__ == '__main__':
    app.run()

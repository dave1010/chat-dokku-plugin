from flask import Flask
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


if __name__ == '__main__':
    app.run()

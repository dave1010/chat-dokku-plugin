from flask import Flask, jsonify, request
from src.auth import auth_bp, check_auth
from src.self_update import self_update_bp
from src.exec_util import exec_as_chatdokku, exec_script_as_chatdokku, scp_to_app, is_safe_path

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(self_update_bp)

@app.before_request
def global_before_request():
    return check_auth()

@app.route('/')
def home():
    return 'Hello, World!\n'


@app.route('/app-list')
def app_list():
    result = exec_as_chatdokku('dokku apps:list | grep -v "My Apps"')
    return jsonify(result['output'].strip().split('\n'))


def generate_random_app_name():
    import random
    adjectives = ['happy', 'sad', 'angry', 'silly', 'calm', 'brave', 'shy', 'bold', 'lazy', 'energetic']
    nouns = ['dog', 'cat', 'bird', 'fish', 'tree', 'car', 'boat', 'plane', 'star', 'moon']
    number = random.randint(10, 99)
    return f"{random.choice(adjectives)}-{random.choice(nouns)}-{number}"


@app.route('/app-create')
def app_create():
    app_name = request.args.get('app_name', generate_random_app_name())
    return jsonify(exec_script_as_chatdokku(f'create-app.sh {app_name}'))


@app.route('/write-file', methods=['POST'])
def write_file():
    app_name = request.json.get('app_name')
    if not app_name:
        return {"error": "App name is required. Check what apps exist with app-list."}, 400

    path = request.json.get('path')
    if not path:
        return {"error": "path is required"}, 400

    if not is_safe_path(app_name, path):
        return {"error": "invalid path"}, 400

    contents = request.json.get('contents')
    if not contents:
        return {"error": "contents is required"}, 400

    return jsonify(scp_to_app(file_contents=contents, app_name=app_name, path=path))



if __name__ == '__main__':
    app.run()

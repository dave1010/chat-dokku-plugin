import subprocess
import re
import os
import tempfile
import shlex

SSH_OPTIONS = "-o ConnectTimeout=5"
SSH_USER_HOST = "chatdokku@172.17.0.1"
WORK_DIR = "/home/chatdokku/apps"

# relies on 2>&1
def result_to_dict(result):
    return {
        'returncode': result.returncode,
        'output': result.stdout,
    }

def exec_as_chatdokku(command):
    escaped_command = shlex.quote(command)
    ssh_command = f'ssh {SSH_OPTIONS} {SSH_USER_HOST} {escaped_command} 2>&1'
    result = subprocess.run(ssh_command, capture_output=True, text=True, shell=True)
    return result_to_dict(result)

# runs scripts that are in ./scripts/local
def exec_script_as_chatdokku(script):
    return exec_as_chatdokku(f'{WORK_DIR}/chat-dokku-plugin/scripts/local/{script}')

def exec_command_in_app_workdir(app_name, command):
    return exec_as_chatdokku(f'cd {WORK_DIR}/{app_name} && {command}')

def is_safe_path(app_name, path):
    # Regex to check app_name and path only contain safe characters
    if not re.match("^[a-zA-Z0-9-]+$", app_name):
        return False
    if not re.match("^[a-zA-Z0-9-/.]+$", path):
        return False

    # Construct the full path
    full_path = os.path.join(WORK_DIR, app_name, path)

    # Normalize the path to resolve any '..' or '.' components
    normalized_path = os.path.normpath(full_path)

    # Check that the normalized path is still under the intended directory
    if not normalized_path.startswith(WORK_DIR + "/"):
        return False

    return True


def scp_to_app(file_contents, app_name, path):
    destination = WORK_DIR + "/" + app_name + "/" + path

    check_command = f'ssh {SSH_OPTIONS} {SSH_USER_HOST} test -e {destination} && echo "File exists" || echo "File does not exist"'
    check_result = subprocess.run(check_command, capture_output=True, text=True, shell=True)

    if "File exists" in check_result.stdout:
        return {"output": "Error: File already exists", "returncode": 1}

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_contents.encode())
        tmp_path = tmp_file.name

    scp_command = f'scp {SSH_OPTIONS} {tmp_path} {SSH_USER_HOST}:{destination}'
    result = subprocess.run(scp_command, capture_output=True, text=True, shell=True)
    return result_to_dict(result)


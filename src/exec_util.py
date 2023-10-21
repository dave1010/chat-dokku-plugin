import subprocess

# relies on 2>&1
def result_to_dict(result):
    return {
        'returncode': result.returncode,
        'output': result.stdout,
    }

def exec_as_chatdokku(command):
    ssh_command = f'ssh -o ConnectTimeout=5 chatdokku@172.17.0.1 {command} 2>&1'
    result = subprocess.run(ssh_command, capture_output=True, text=True, shell=True)
    return result_to_dict(result)

def exec_script_as_chatdokku(script):
    return exec_as_chatdokku(f'/home/chatdokku/apps/chat-dokku-plugin/scripts/local/{script}')


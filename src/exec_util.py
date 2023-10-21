import subprocess

def result_to_dict(result):
    return {
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
    }

def exec_as_chatdokku(command):
    ssh_command = f'ssh -o ConnectTimeout=5 chatdokku@172.17.0.1 {command}'
    result = subprocess.run(ssh_command, capture_output=True, text=True, shell=True)
    return result_to_dict(result)

def exec_script_as_chatdokku(script):
    return exec_as_chatdokku(f'/app/scripts/api/{script}')


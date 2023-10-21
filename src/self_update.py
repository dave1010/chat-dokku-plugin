import os
import subprocess
from flask import Blueprint, Response

self_update_bp = Blueprint('self_update', __name__)

@self_update_bp.route('/self-update')
def self_update():
    def generate():
        process = subprocess.Popen(['ssh -o ConnectTimeout=5 chatdokku@172.17.0.1 /home/chatdokku/apps/chat-dokku-plugin/scripts/local/self-update.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        for line in iter(process.stdout.readline, ''):
            yield line

    return Response(generate(), content_type='text/plain')

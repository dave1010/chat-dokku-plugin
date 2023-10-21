import os
import subprocess
from flask import Blueprint, Response

self_update_bp = Blueprint('self_update', __name__)

@self_update_bp.route('/self-update')
def self_update():
    def generate():
        process = subprocess.Popen(['/app/scripts/api/self-update.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in iter(process.stdout.readline, ''):
            yield line

    return Response(generate(), content_type='text/plain')

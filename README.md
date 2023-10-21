# chat-dokku-plugin
Plugin for Chat Dokku

## Running in debug mode

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


    PSK=secret flask run --debug

# FAQ

How do I find the PSK?

    dokku config:show chat-dokku-plugin | grep PSK

Debugging

    dokku logs chat-dokku-plugin

# API docs

To update `public/openapi.yaml`:

    python write_spec.py

Docs are served at `/api/docs`
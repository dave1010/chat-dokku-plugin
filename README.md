# chat-dokku-plugin
Plugin for Chat Dokku

## Running in debug mode

    PSK=secret flask run --debug

# FAQ

How do I find the PSK?

    dokku config:show chat-dokku-plugin | grep PSK

Debugging

    dokku logs chat-dokku-plugin
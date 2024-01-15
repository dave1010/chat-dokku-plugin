# Generates an OpenAPI specification
# The generated specific is written to ./public/openapi.yaml and outputted

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

import yaml

from app import *


OPENAPI_SPEC = """
servers:
- url: http://127.0.0.1:5000/
  description: The development API server
security:
  - ApiKeyAuth: []
"""
settings = yaml.safe_load(OPENAPI_SPEC)

spec = APISpec(
    title="Chat Dokku",
    version="1.0.0",
    openapi_version="3.0.1",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    **yaml.safe_load(OPENAPI_SPEC)
)
api_key_scheme = {"type": "apiKey", "in": "header", "name": "Authorization"}
spec.components.security_scheme("ApiKeyAuth", api_key_scheme)


class ExecResultSchema(Schema):
    returncode = fields.Int(required=True)
    output = fields.Str(required=True)

with app.test_request_context():
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':  # Skip static files
            view_function = app.view_functions[rule.endpoint]
            spec.path(view=view_function)

# with app.test_request_context():
#     spec.path(view=app_list)
#     spec.path(view=write_file)
#     spec.path(view=app_create)


spec_yaml = spec.to_yaml()

with open('./public/openapi.yaml', 'w') as f:
    f.write(spec_yaml)

print(spec_yaml)

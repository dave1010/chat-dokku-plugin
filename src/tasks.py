from flask import Blueprint, jsonify, request, make_response, redirect, url_for

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks
    ---
    get:
      summary: Get all tasks
      responses:
        '200':
          description: Returns all tasks with their statuses
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    detail:
                      type: string
                    done:
                      type: boolean
    """    
    return jsonify([])

@tasks_bp.route('/tasks', methods=['POST'])
def post_tasks():
    """Update tasks
    ---
    post:
      summary: Add or complete tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                add:
                  type: array
                  items:
                    type: string
                complete:
                  type: array
                  items:
                    type: string
      responses:
        '200':
          description: Returns all tasks with their statuses
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    detail:
                      type: string
                    done:
                      type: boolean
    """
    return jsonify([])

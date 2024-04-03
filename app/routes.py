from app import webserver
from flask import request, jsonify

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    # TODO
    # Check if job_id is valid
    if int(job_id) > webserver.job_counter:
        return jsonify({"status": "error",
                        "reason" : "Invalid job_id"}), 400

    # Check if job_id is done and return the result
    try:
        with open(f'./results/{job_id}', 'r') as f:
            return jsonify({
            'status': 'done',
            'data': json.load(f)
        }), 200
    except Exception as e:
        return jsonify({
                    'status': 'running'
                })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    data = request.json
    print(f"Got request {data}")

    webserver.tasks_runner.queue.put((webserver.job_counter,
                                      webserver.data_ingestor.states_mean(data['question'])))
    webserver.job_counter += 1

    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.json
    print(f"Got request {data}")
    
    webserver.tasks_runner.queue.put((webserver.job_counter,
                                    webserver.data_ingestor.state_mean(data['question'], data['state'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })



@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.json
    
    webserver.tasks_runner.queue.put((webserver.job_counter,
                                    webserver.data_ingestor.best5(data['question'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.json
    
    webserver.tasks_runner.queue.put((webserver.job_counter,
                                    webserver.data_ingestor.worst5(data['question'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.json
    
    webserver.tasks_runner.queue.put((webserver.job_counter,
                                    webserver.data_ingestor.global_mean(data['question'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    data = request.json
    
    webserver.tasks_runner.queue.put((webserver.job_counter,
                                    webserver.data_ingestor.diff_from_mean(data['question'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.json
    
    webserver.tasks_runner.queue.put((webserver.job_counter,
                                    webserver.data_ingestor.state_diff_from_mean(data['question'], data['state'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.json
    
    webserver.tasks_runner.queue.put((webserver.job_counter,
                                    webserver.data_ingestor.mean_by_category(data['question'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes

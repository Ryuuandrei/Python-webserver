"""
This module contains the API endpoints for the webserver.
"""
import json

from flask import request, jsonify
from app import webserver

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """
    Handle the POST request and process the received data.

    Returns:
        If the request is successful, returns a JSON response with a success
        message and the received data. If the request method is not allowed, returns
        a JSON response with an error message and a status code of 405.
    """
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    Get the response for a given job ID.

    Args:
        job_id (int): The ID of the job.

    Returns:
        dict: A JSON response containing the status and data of the job.

    Raises:
        None

    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s', request.method, request.url)

    if int(job_id) > webserver.job_counter:
        return jsonify({"status": "error",
                        "reason" : "Invalid job_id"})

    try:
        with open(f'./results/{job_id}', 'r', encoding='utf-8') as f_in:

            return jsonify({
                'status': 'done',
                'data': json.load(f_in)
            })
    except Exception:
        return jsonify({
            'status': 'running'
        })

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Handle the request for calculating the mean of states.

    Returns:
        A JSON response containing the status of the request and the job ID.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

    data = request.json

    webserver.tasks_runner.queue.put((webserver.job_counter,
                                      webserver.data_ingestor.states_mean(data['question'])))
    webserver.job_counter += 1

    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Handles the state mean request.

    This function is responsible for processing the state mean request received by the server.
    It checks if the server is down, logs the request details, and adds the request to the task
    queue. It returns a JSON response with the status and job ID.

    Returns:
        A JSON response containing the status and job ID.

    Raises:
        None
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

    data = request.json

    webserver.tasks_runner.queue.put((webserver.job_counter,
                        webserver.data_ingestor.state_mean(data['question'], data['state'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Handles the request for the best5 endpoint.

    Returns:
        A JSON response containing the status of the request and the job ID.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

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
    """
    Handles the worst5_request API endpoint.

    This function is responsible for processing the worst5_request API endpoint.
    It checks if the server is down and returns an error message if it is.
    It logs the request details and the received JSON data.
    It puts the task in the tasks_runner queue to calculate the worst 5 sports based on the
    given question. It increments the job_counter and returns the status and job_id of the task.

    Returns:
        A JSON response containing the status and job_id of the task.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

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
    """
    Handle the request for calculating the global mean.

    Returns:
        A JSON response containing the status of the request and the job ID.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

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
    """
    Handle the request to calculate the difference from the mean.

    Returns:
        A JSON response containing the status of the job and the job ID.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)
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
    """
    Handles the state_diff_from_mean request.

    This function is responsible for processing the state_diff_from_mean request
    by retrieving the data from the request JSON, queuing the task to calculate
    the state difference from the mean, and returning the job ID.

    Returns:
        A JSON response containing the status of the request and the job ID.

    Raises:
        None
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

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
    """
    Handle the request to calculate the mean by category.

    Returns:
        A JSON response containing the status of the request and the job ID.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

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
    """
    Handles the request to calculate the mean by category for a given state.

    Returns:
        A JSON response containing the status of the request and the job ID.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s %s', request.method, request.url, request.json)

    data = request.json

    webserver.tasks_runner.queue.put((webserver.job_counter,
                webserver.data_ingestor.state_mean_by_category(data['question'], data['state'])))
    webserver.job_counter += 1
    return jsonify({
        'status': 'running',
        'job_id': webserver.job_counter - 1
    })

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """
    Gracefully shuts down the server.

    This function logs the method and URL of the request, sets the `shutdown` flag to True,
    and shuts down the tasks runner. It then returns a JSON response indicating the status
    of the server shutdown.

    Returns:
        A JSON response indicating the status of the server shutdown.
    """
    webserver.logger.info('%s %s', request.method, request.url)

    webserver.shutdown = True
    webserver.tasks_runner.shutdown()
    return jsonify({"status" : "shutting down server"})


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """
    Returns the status of the jobs running on the server.

    Returns:
        A JSON response containing the status of the jobs.
    """
    if webserver.shutdown:
        webserver.logger.error('%s %s - server down', request.method, request.url)
        return jsonify({"status": "server down"})

    webserver.logger.info('%s %s',request.method, request.url)

    return jsonify({
        'status': 'done',
        'data' : [{str(i) : "done" if i in webserver.tasks_runner.tasks else "running"}
                for i in range(1, webserver.job_counter)]
    })


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """
    Returns a message containing the defined routes of the webserver.

    Returns:
        str: A message displaying the defined routes as HTML <p> tags.
    """
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """
    Returns a list of defined routes in the webserver.

    Returns:
        list: A list of strings representing the defined routes,
        along with the HTTP methods allowed for each route.
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """
    Returns the number of jobs currently running.

    Returns:
        A JSON response containing the number of jobs.
    """
    return jsonify({"num_jobs": webserver.job_counter - len(webserver.tasks_runner.tasks) - 1})

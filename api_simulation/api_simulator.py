import json
from uuid import uuid4

from flask import Flask, jsonify
import datetime
import random

app = Flask(__name__)

simulated_agent_uuids = {"agent_uuid": str(uuid4()),
                         "work_package_uuid": str(uuid4()),
                         "agent_tier": "AGENT",
                         "task_uuid": str(uuid4())}

with open('simulated_response.json', 'r') as files:
    simulated_response = json.loads(files.read())

with open('simulated_checkpoints.json', 'r') as files:
    simulated_checkpoints = json.loads(files.read())


@app.route('/api/register_heartbeat', methods=['GET', 'POST'])
def register_heartbeat():
    """Simulate agent registration and heartbeat"""
    return jsonify(simulated_agent_uuids), 200

@app.route('/api/get_task_information', methods=['GET', 'POST'])
def get_task_information():
    """Simulate agent task information request"""
    return jsonify({"task_information_obj": simulated_response}), 200

@app.route('/api/check_checkpoint_information', methods=['GET', 'POST'])
def check_checkpoint_information():
    """Simulate agent checkpoint information request"""
    return jsonify({"checkpoint_information": simulated_checkpoints}), 200


if __name__ == '__main__':
    app.run(debug=True)
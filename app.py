from flask import Flask, render_template, request, jsonify
import numpy as np
import deadlock  # Importing the deadlock detection module

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        processes = int(data.get('processes', 0))
        resources = int(data.get('resources', 0))
        allocation = np.array(data.get('allocation', []), dtype=int).reshape((processes, resources))
        request_matrix = np.array(data.get('request', []), dtype=int).reshape((processes, resources))

        if processes <= 0 or resources <= 0:
            return jsonify({"error": "Invalid input! Number of processes and resources must be greater than zero."}), 400

        if allocation.shape != (processes, resources) or request_matrix.shape != (processes, resources):
            return jsonify({"error": "Matrix dimensions do not match the given number of processes and resources."}), 400

        deadlock_detected, message = deadlock.detect_deadlock(processes, resources, allocation, request_matrix)

        return jsonify({"deadlock": deadlock_detected, "message": message})

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

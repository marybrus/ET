from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template('layout.html')

# API route to run Python code
@app.route('/run_code', methods=['POST'])
def run_code():
    try:
        # Get the Python code from the request
        code = request.json.get('code')

        # Define a safe execution environment
        exec_env = {}

        # Execute the provided code safely
        exec(code, {'np': np}, exec_env)

        # Get the result from the environment
        result = exec_env.get('result', 'Code executed without output')
        return jsonify({'output': str(result)})
    except Exception as e:
        # Handle errors
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, jsonify, render_template
import numpy as np
import io
import sys

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

        # Create a StringIO buffer to capture output
        output_buffer = io.StringIO()
        sys.stdout = output_buffer  # Redirect stdout to the buffer

        # Define a safe execution environment
        exec_env = {}

        # Execute the provided code safely
        exec(code, {'np': np}, exec_env)

        # Get the result from the environment and buffer
        sys.stdout = sys.__stdout__  # Reset stdout back to default

        # Capture printed output
        output = output_buffer.getvalue()

        # If no output, provide a default message
        if not output:
            output = "Code executed without output."

        return jsonify({'output': output})
    except Exception as e:
        # Handle errors
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

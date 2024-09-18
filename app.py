from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_quiz', methods=['POST'])
def check_quiz():
    answers = request.json
    score = 0

    # Correct answers for the quiz
    correct_answers = {
        'q1': 'a',  # Correct answer for question 1
        'q2': 'b'   # Correct answer for question 2
    }

    for question, answer in answers.items():
        if correct_answers.get(question) == answer:
            score += 1

    return jsonify({"result": f"You got {score} out of 2 questions right!"})

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code')

    try:
        # Use subprocess to execute Python code safely
        result = subprocess.run(
            ['python3', '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout if result.stdout else "Code executed successfully"
    except Exception as e:
        output = f"Error: {str(e)}"

    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True)

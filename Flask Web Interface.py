from flask import Flask, request, jsonify

app = Flask(__name__)
backend = StayziaBackend()

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    backend.execute(code)
    return jsonify({"message": "Execution completed", "errors": backend.compiler.error_log})

if __name__ == '__main__':
    app.run(debug=True)

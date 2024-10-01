from flask import Flask, request, jsonify

app = Flask(__name__)
backend = StayziaBackend()

@app.route('/execute', methods=['POST'])
def execute():
    code = request.json.get('code')
    compile_first = request.json.get('compile_first', False)
    if code:
        try:
            if compile_first:
                backend.compiler.compile_to_cpp(code)
                return jsonify({"status": "compiled", "message": "Compilation successful."}), 200
            else:
                backend.interpreter.run(code)
                return jsonify({"status": "executed", "message": "Execution successful."}), 200
        except Exception as e:
            logging.error(f"Execution error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 400
    return jsonify({"status": "error", "message": "No code provided."}), 400

if __name__ == '__main__':
    app.run(debug=True)

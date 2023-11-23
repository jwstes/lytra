from flask import Flask, jsonify, request
import subprocess
import psutil

app = Flask(__name__)

python_process = None
myID = None

@app.route('/start', methods=['POST'])
def start_script():
    global python_process
    global myID
    if python_process is not None and python_process.poll() is None:
        return jsonify(error='Python script is already running'), 400

    try:
        data = request.get_json()
        python_process = subprocess.Popen(['python3', 'lytra.py', f'{data["trg"]}', '1'])
        myID = data['id']

        return jsonify(message=f'Lyta {data["id"]} Started!')
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/stop', methods=['POST'])
def stop_script():
    global python_process
    global myID

    if python_process is None or python_process.poll() is not None:
        return jsonify(error='No running Python script to stop'), 400

    try:
        process = psutil.Process(python_process.pid)
        for child in process.children(recursive=True):
            child.terminate()
        python_process.terminate()
        python_process.wait()
        python_process = None
        return jsonify(message=f'Lytra {myID} Stopped')
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/sanityCheck', methods=['POST'])
def sanityCheck():
    return jsonify({"stauts" : "200"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)

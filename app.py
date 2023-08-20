from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_nums():
    try:
        data =  request.get_json()
        num1 = data['num1']
        num2 = data['num2']
        result = num1 + num2
        return jsonify({'result': result})
    except KeyError:
        return jsonify({"error": "Invalid input."})

@app.route('/subtract', methods=['POST'])
def subtract_numbers():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 - num2
    return jsonify({'result': result})

@app.route('/divide', methods=['POST'])
def divide_numbers():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 / num2
    return jsonify({'result': result})

@app.route('/multiply', methods=['POST'])
def multiply_numbers():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 * num2
    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8989)
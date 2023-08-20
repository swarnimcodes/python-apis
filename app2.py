from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/multiply', methods=['POST'])
def multiply_nums():
    data = request.get_json()
    num1, num2 = data['num1'], data['num2']
    result = num1 * num2
    return jsonify({'result': result}), 200

@app.route('/divide', methods=['POST'])
def divide_nums():
    data = request.get_json()
    num1, num2 = float(data['num1']), float(data['num2'])
    result = num1 / num2
    result = round(result, 3)
    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8988, debug=True)
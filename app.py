from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

# 创建模型
@app.route('/create_model', methods=['POST'])
def create_model():
    data = request.json
    model_id = data.get('model_id')
    model_params = data.get('model_params')

    # 根据模型参数创建萨维模型（这里简单起见，直接返回模型参数）
    return jsonify({'message': 'Model created successfully', 'model_id': model_id, 'model_params': model_params})

if __name__ == '__main__':
    app.run(debug=True)

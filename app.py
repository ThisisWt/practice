from flask import Flask, request, jsonify

app = Flask(__name__)

# 用于存储模型数据的全局变量，这里简单起见，以字典形式存储模型参数
models = {}

# 处理新建结构模型请求
@app.route('/create_model', methods=['POST'])
def create_model():
    data = request.json
    model_id = data.get('model_id')
    model_params = data.get('model_params')

    # 在模型字典中添加新模型
    models[model_id] = model_params

    return jsonify({'message': 'Model created successfully', 'model_id': model_id})

# 其他路由和处理函数可以根据需要添加

if __name__ == '__main__':
    app.run(debug=True)

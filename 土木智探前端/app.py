from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # 添加跨域支持

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

ALLOWED_EXTENSIONS = {'obj'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part found'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': f'File successfully uploaded to {filepath}', 'success': True})
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/create_model', methods=['POST'])
def create_model():
    data = request.get_json()
    length = data.get('length')
    width = data.get('width')
    height = data.get('height')
    # 在此处处理创建模型的逻辑
    return jsonify({'message': 'Model successfully created', 'success': True})

@app.route('/', methods=['GET'])
def index():
    return send_file('新建结构模型.html')  # 替换为你的前端HTML文件路径

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

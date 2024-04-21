from flask import Flask, request, jsonify, redirect, url_for, send_file
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

app = Flask(__name__)
CORS(app)  # 允许所有域进行跨域请求

# 配置文件上传目录和允许的文件类型
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'  # 假定有一个名为 static 的文件夹用于保存生成的图像

# 确保上传和静态目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# 允许的文件扩展名集合
ALLOWED_EXTENSIONS = {'cad', 'jpg', 'png', 'jpeg'}  # 添加更多文件类型如需要


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/plot_model', methods=['POST'])
def plot_model():
    dimensions = request.json['dimensions'].split(',')
    if len(dimensions) != 3:
        return jsonify({'success': False, 'message': '请输入三个数值'})
    length, width, height = map(float, dimensions)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid([0, length], [0, width])
    Z = np.array([[0, 0], [height, height]])
    ax.plot_surface(X, Y, Z)
    ax.set_xlabel('Length')
    ax.set_ylabel('Width')
    ax.set_zlabel('Height')

    # 将图片转为Base64编码
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return jsonify({'success': True, 'image': img_str})

@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'model_file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['model_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': f'Model imported and saved to {filename}'})
    else:
        return jsonify({'error': 'File not allowed'})


if __name__ == '__main__':
    app.run(debug=True)

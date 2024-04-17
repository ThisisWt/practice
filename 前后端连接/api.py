from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

app = Flask(__name__)

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


@app.route('/new_model', methods=['POST'])
def new_model():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    length = data.get('length')
    width = data.get('width')
    height = data.get('height')

    if length is None or width is None or height is None:
        return jsonify({"error": "Missing data for length, width, or height"}), 400

    try:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid([0, float(length)], [0, float(width)])
        Z = np.array([[0, 0], [float(height), float(height)]])
        ax.plot_surface(X, Y, Z)
        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')

        image_path = os.path.join(app.config['STATIC_FOLDER'], 'model_plot.png')
        plt.savefig(image_path)
        plt.close()

        return jsonify({'message': 'Model plotted and image saved.', 'image_url': f'/static/model_plot.png'})
    except Exception as e:
        return jsonify({'error': str(e)})


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

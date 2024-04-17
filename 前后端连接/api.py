from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

app = Flask(__name__)

# 配置文件上传目录和允许的文件类型
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'cad'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/new_model', methods=['POST'])
def new_model():
    try:
        length = float(request.form['length'])
        width = float(request.form['width'])
        height = float(request.form['height'])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid([0, length], [0, width])
        Z = np.array([[0, 0], [height, height]])
        ax.plot_surface(X, Y, Z)
        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        
        image_path = os.path.join(app.config['static_folder'], 'model_plot.png')
        plt.savefig(image_path)
        plt.close()
        
        return jsonify({'message': 'Model plotted and image saved.', 'image_url': '/static/model_plot.png'})
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

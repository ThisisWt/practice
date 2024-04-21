from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'cad', 'jpg', 'png', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/plot_model', methods=['POST'])
def plot_model():
    dimensions = request.json.get('dimensions', '').split(',')
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

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return jsonify({'success': True, 'image': img_str})

@app.route('/upload_model', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': f'Model imported and saved to {filename}'})
    else:
        return jsonify({'error': 'File not allowed'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

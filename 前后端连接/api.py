from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)

@app.route('/plot_model', methods=['POST'])
def plot_model():
    data = request.json
    dimensions = data.get('dimensions', '').split(',')
    if len(dimensions) != 3:
        return jsonify({'success': False, 'message': 'Please enter three numeric values separated by commas.'}), 400

    length, width, height = map(float, dimensions)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid([0, length], [0, width])
    Z = np.array([[0, 0], [height, height]])
    ax.plot_surface(X, Y, Z)
    ax.set_xlabel('Length')
    ax.set_ylabel('Width')
    ax.set_zlabel('Height')

    # Convert plot to PNG image
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return jsonify({'success': True, 'image': image_base64})

@app.route('/upload_model', methods=['POST'])
def upload_model():
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(f"./uploads/{filename}")
        return jsonify({'message': f'Model imported from {filename}', 'success': True})
    return jsonify({'message': 'No file uploaded', 'success': False})

if __name__ == '__main__':
    app.run(debug=True)

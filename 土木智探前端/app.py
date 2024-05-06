from flask import Flask, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import base64

app = Flask(__name__)

class StructuralModelingApp:
    def __init__(self):
        self.text = ""
        self.image_data = None

    def process_action(self, action, dimensions):
        try:
            if action == '矩形梁' and len(dimensions) == 3:
                self.plot_beam(*map(float, dimensions))
            elif action == '圆柱体' and len(dimensions) == 2:
                self.plot_cylinder(*map(float, dimensions))
            elif action == '球体' and len(dimensions) == 1:
                self.plot_sphere(float(dimensions[0]))
            else:
                self.text += "请选择有效的操作并提供正确的尺寸。\n"
        except ValueError:
            self.text += "请输入有效的数字。\n"

    def plot_beam(self, length, width, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid([0, length], [0, width])
        Z = np.array([[0, 0], [height, height]])
        ax.plot_surface(X, Y, Z, color='blue')
        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        self.image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    def plot_cylinder(self, radius, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        z = np.linspace(0, height, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = radius * np.cos(theta_grid)
        y_grid = radius * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color='red')
        ax.set_xlabel('Radius')
        ax.set_ylabel('Height')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        self.image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    def plot_sphere(self, radius):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='green')
        ax.set_xlabel('Radius')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        self.image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

@app.route('/', methods=['POST'])
def index():
    app_instance = StructuralModelingApp()
    action = request.form['action']
    dimensions = request.form['dimensions'].split(',')
    app_instance.process_action(action, dimensions)
    if app_instance.image_data:
        return jsonify({'text': app_instance.text, 'image_data': app_instance.image_data})
    return jsonify({'text': app_instance.text})

if __name__ == '__main__':
    app.run(debug=True, port=8000)

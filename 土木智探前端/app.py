from flask import Flask, request, jsonify
from flask_cors import CORS
import ezdxf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

app = Flask(__name__)
CORS(app)

class StructuralModelingApp:
    def __init__(self):
        self.filename = None

    def process_action(self, action, dimensions):
        response_text = ""
        try:
            if action == '矩形梁' and len(dimensions) == 3:
                response_text = self.plot_beam(*map(float, dimensions))
            elif action == '圆柱体' and len(dimensions) == 2:
                response_text = self.plot_cylinder(*map(float, dimensions))
            elif action == '球体' and len(dimensions) == 1:
                response_text = self.plot_sphere(float(dimensions[0]))
            elif action.startswith('导入') and action.endswith('DXF'):
                self.import_dxf()
                response_text = f"文件已加载: {self.filename}"
            elif self.filename and action.endswith('DXF'):
                getattr(self, action.lower().replace(' ', '_'))()
                response_text = f"执行操作: {action}"
            else:
                response_text = "请检查输入或选择的操作。"
        except ValueError:
            response_text = "请输入有效的数字。"
        return response_text

    def plot_beam(self, length, width, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid([0, length], [0, width])
        Z = np.array([[0, 0], [height, height]])
        ax.plot_surface(X, Y, Z, color='blue')
        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        plt.savefig("plot.png")
        return "plot.png"

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
        plt.savefig("plot.png")
        return "plot.png"

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
        plt.savefig("plot.png")
        return "plot.png"

    def import_dxf(self):
        self.filename = "example.dxf"  # For testing purposes

    def export_dxf(self):
        pass  # Add your code for exporting DXF here

@app.route('/create_model', methods=['POST'])
def create_model():
    data = request.json
    action = '矩形梁'  # Assuming default action is '矩形梁'
    dimensions = [data['length'], data['width'], data['height']]
    return modeling_app.process_action(action, dimensions)

@app.route('/upload_model', methods=['POST'])
def upload_model():
    file = request.files['file']
    # Save the uploaded file
    file.save("uploaded_model.dxf")
    # Now set the filename in the modeling app
    modeling_app.filename = "uploaded_model.dxf"
    return "File uploaded successfully"

if __name__ == '__main__':
    modeling_app = StructuralModelingApp()
    app.run(debug=True)

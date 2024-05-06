from flask import Flask, render_template, request, jsonify
import tkinter as tk
from tkinter import filedialog
#import ezdxf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

app = Flask(__name__)

class StructuralModelingApp:
    def __init__(self):
        self.text = ""
        self.filename = None

    def process_action(self, action, dimensions):
        try:
            if action == '矩形梁' and len(dimensions) == 3:
                self.plot_beam(*map(float, dimensions))
            elif action == '圆柱体' and len(dimensions) == 2:
                self.plot_cylinder(*map(float, dimensions))
            elif action == '球体' and len(dimensions) == 1:
                self.plot_sphere(float(dimensions[0]))
            elif action.startswith('导入') and action.endswith('DXF'):
                self.import_dxf()
            elif self.filename and action.endswith('DXF'):
                getattr(self, action.lower().replace(' ', '_'))()
            else:
                self.text += "请检查输入或选择的操作。\n"
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
        plt.savefig('plot.png')
        plt.close()

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
        plt.savefig('plot.png')
        plt.close()

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
        plt.savefig('plot.png')
        plt.close()

    def import_dxf(self):
        self.filename = filedialog.askopenfilename(title="选择DXF模型文件", filetypes=[("DXF files", "*.dxf")])
        if self.filename:
            self.text += f"文件已加载: {self.filename}\n"

    def analyze_dxf(self):
        pass  # Implement your DXF analysis logic here

    def modify_dxf(self):
        pass  # Implement your DXF modification logic here

    def visualize_dxf(self):
        pass  # Implement your DXF visualization logic here

    def export_dxf(self):
        pass  # Implement your DXF export logic here

@app.route('/', methods=['GET', 'POST'])
def index():
    app_instance = StructuralModelingApp()
    if request.method == 'POST':
        action = request.form['action']
        dimensions = request.form['dimensions'].split(',')
        app_instance.process_action(action, dimensions)
    return render_template('index.html', text=app_instance.text)

if __name__ == '__main__':
    app.run(debug=True)

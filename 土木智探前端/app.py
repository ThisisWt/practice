from flask import Flask, request, jsonify
from flask_cors import CORS
import tkinter as tk
from tkinter import filedialog
import ezdxf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

app = Flask(__name__)
CORS(app)  # 处理跨域请求

class StructuralModelingApp:
    def __init__(self, master):
        self.master = master
        master.title("结构模型与DXF文件处理")

        # 创建主界面
        self.label = tk.Label(master, text="请输入尺寸（用逗号分隔）或操作DXF文件:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        # 下拉菜单，选择形状或DXF操作
        self.shape_var = tk.StringVar(master)
        self.shape_var.set("矩形梁")  # 默认值
        self.shapes = ['矩形梁', '圆柱体', '球体', '导入DXF', '分析DXF', '修改DXF', '可视化DXF', '导出DXF']
        self.shape_menu = tk.OptionMenu(master, self.shape_var, *self.shapes)
        self.shape_menu.pack()

        self.action_button = tk.Button(master, text="执行操作", command=self.process_action)
        self.action_button.pack()

        self.text = tk.Text(master, height=10, width=80)
        self.text.pack()

        self.filename = None

    def process_action(self):
        action = self.shape_var.get()
        dimensions = self.entry.get().split(',')
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
                self.text.insert(tk.END, "请检查输入或选择的操作。\n")
        except ValueError:
            self.text.insert(tk.END, "请输入有效的数字。\n")

    def plot_beam(self, length, width, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid([0, length], [0, width])
        Z = np.array([[0, 0], [height, height]])
        ax.plot_surface(X, Y, Z, color='blue')
        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        plt.show()

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
        plt.show()

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
        plt.show()

    def import_dxf(self):
        self.filename = filedialog.askopenfilename(title="选择DXF模型文件", filetypes=[("DXF files", "*.dxf")])
        if self.filename:
            self.text.insert(tk.END, f"文件已加载: {self.filename}\n")

    def 分析dxf(self):
        doc = ezdxf.readfile(self.filename)
        msp = doc.modelspace()
        entity_types = {}
        for entity in msp:
            entity_type = entity.dxftype()
            entity_types[entity_type] = entity_types.get(entity_type, 0) + 1
        self.text.insert(tk.END, "分析结果:\n")
        for entity_type, count in entity_types.items():
            self.text.insert(tk.END, f"{entity_type}: {count}\n")

    def 修改dxf(self):
        doc = ezdxf.readfile(self.filename)
        msp = doc.modelspace()
        # 将所有线条颜色改为红色
        for entity in msp.query('LINE'):
            entity.dxf.color = 1
        doc.saveas('modified_dxf.dxf')
        self.text.insert(tk.END, "修改已保存到 'modified_dxf.dxf'\n")

    def 可视化dxf(self):
        doc = ezdxf.readfile(self.filename)
        msp = doc.modelspace()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for entity in msp.query('LINE'):
            start = entity.dxf.start
            end = entity.dxf.end
            ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], 'gray')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    def 导出dxf(self):
        doc = ezdxf.readfile(self.filename)
        doc.saveas('exported_dxf.dxf')
        self.text.insert(tk.END, "文件已导出为 'exported_dxf.dxf'\n")

@app.route('/process_action', methods=['POST'])
def process_action():
    data = request.get_json()
    action = data.get('action')
    dimensions = data.get('dimensions')

    try:
        if action == '矩形梁' and len(dimensions) == 3:
            root.plot_beam(*map(float, dimensions))
        elif action == '圆柱体' and len(dimensions) == 2:
            root.plot_cylinder(*map(float, dimensions))
        elif action == '球体' and len(dimensions) == 1:
            root.plot_sphere(float(dimensions[0]))
        elif action.startswith('导入') and action.endswith('DXF'):
            root.import_dxf()
        elif root.filename and action.endswith('DXF'):
            getattr(root, action.lower().replace(' ', '_'))()
        else:
            return jsonify({'result': "请检查输入或选择的操作。"})
    except ValueError:
        return jsonify({'result': "请输入有效的数字。"})

    return jsonify({'result': "操作成功执行。"})

if __name__ == '__main__':
    root = StructuralModelingApp(None)  # 创建Tkinter应用
    app.run(debug=True)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ezdxf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

@csrf_exempt
def process_action(request):
    if request.method == 'POST':
        data = request.POST
        action = data.get('action')
        dimensions = data.get('dimensions').split(',')
        response_data = {}
        
        try:
            if action == '矩形梁' and len(dimensions) == 3:
                plot_beam(*map(float, dimensions))
                response_data['message'] = "矩形梁绘制完成"
            elif action == '圆柱体' and len(dimensions) == 2:
                plot_cylinder(*map(float, dimensions))
                response_data['message'] = "圆柱体绘制完成"
            elif action == '球体' and len(dimensions) == 1:
                plot_sphere(float(dimensions[0]))
                response_data['message'] = "球体绘制完成"
            elif action == '导入DXF':
                filename = request.FILES['file'].name
                import_dxf(filename)
                response_data['message'] = f"{filename} 文件已加载"

            return JsonResponse(response_data)
        except ValueError:
            return JsonResponse({'error': '请输入有效的数字'})

def plot_beam(length, width, height):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid([0, length], [0, width])
    Z = np.array([[0, 0], [height, height]])
    ax.plot_surface(X, Y, Z, color='blue')
    ax.set_xlabel('Length')
    ax.set_ylabel('Width')
    ax.set_zlabel('Height')
    plt.show()

def plot_cylinder(radius, height):
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

def plot_sphere(radius):
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

def import_dxf(filename):
    # 处理导入DXF文件的逻辑
    pass

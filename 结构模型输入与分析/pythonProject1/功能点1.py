import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class StructuralModelingApp:
    def __init__(self, master):
        self.master = master
        master.title("Structural Model Input and Editing")

        # Create main interface
        self.label = tk.Label(master, text="Enter the dimensions of a beam (length, width, height):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.plot_button = tk.Button(master, text="Plot Model", command=self.plot_model)
        self.plot_button.pack()

        self.import_button = tk.Button(master, text="Import Model", command=self.import_model)
        self.import_button.pack()

    def plot_model(self):
        dimensions = self.entry.get().split(',')
        if len(dimensions) != 3:
            print("Please enter three numeric values separated by commas.")
            return
        length, width, height = map(float, dimensions)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y = np.meshgrid([0, length], [0, width])
        Z = np.array([[0, 0], [height, height]])
        ax.plot_surface(X, Y, Z)
        ax.set_xlabel('Length')
        ax.set_ylabel('Width')
        ax.set_zlabel('Height')
        plt.show()

    def import_model(self):
        filename = filedialog.askopenfilename(title="Select a model file", filetypes=(("CAD files", "*.cad"), ("All files", "*.*")))
        print(f"Model imported from {filename}")

root = tk.Tk()
app = StructuralModelingApp(root)
root.mainloop()

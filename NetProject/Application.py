import tkinter as tk
import Graph as G

class Application(tk.Tk):
    graph = G.Graph()
    canvas = None
    __names, __obj_values = None, None

    def __init__(self):
        super().__init__()
        self.title("LPSolver")
        self.geometry("400x430")
        self.resizable(False, False)

        self.canvas = tk.Canvas(background='black', width=396, height=396)
        self.canvas.pack()

        self.graph.generateGraph()

        self.__names = ['x'+eName for eName in self.graph.getNames()]
        self.__obj_values = [value for value in self.graph.getWeights()]

        self.__drawGraph()

        lbl = tk.Label(text=f"Result : {self.graph.lpsolving()}", font=("Arial", 12))
        lbl.pack()

    def __drawGraph(self):
        coords = self.graph.constructGraph(396)
        
        for mass in coords:
            self.canvas.create_oval(mass[0] - 15, 
                                    mass[1] - 15, 
                                    mass[0] + 15, 
                                    mass[1] + 15, fill='brown', outline='blue')
            self.canvas.create_text(mass[0] - 5, 
                                    mass[1] - 5, 
                                    text=mass[2], font=('Arial', 15, 'bold'), fill='burlywood1')
        
        for name in self.__names:
            x1, y1, x2, y2 = 0, 0, 0, 0
            if name[1] == 'S':
                x1, y1, x2, y2 = coords[0][0], coords[0][1], coords[int(name[2])][0], coords[int(name[2])][1]
            elif name[2] == 'D':
                x1, y1, x2, y2 = coords[int(name[1])][0], coords[int(name[1])][1], coords[-1][0], coords[-1][1]
            else:
                x1, y1, x2, y2 = coords[int(name[1])][0], coords[int(name[1])][1], coords[int(name[2])][0], coords[int(name[2])][1]
            self.canvas.create_line(x1, y1, x2, y2, fill='grey', arrow='last')
            self.canvas.create_text(abs(x1 + x2) // 2, 
                                    abs(y1 + y2) // 2, 
                                    text=self.__obj_values[self.__names.index(name)], 
                                    fill='red', font=('Arial', 8, 'bold'))

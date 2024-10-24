import tkinter as tk
from maze_solver import MazeSolver
import random
from typing import List, Tuple, Set
import time

class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bidirectional Maze Solver")
        
        # Constants
        self.CELL_SIZE = 25
        self.MAZE_SIZE = 31
        
        # Initialize maze and solver
        self.maze = self.generate_complex_maze()
        self.solver = MazeSolver(self.maze)
        
        # Create main container frame
        self.container_frame = tk.Frame(root)
        self.container_frame.pack(padx=20, pady=20, expand=True, fill=tk.BOTH)
        
        # Create left frame for maze
        self.maze_frame = tk.Frame(self.container_frame)
        self.maze_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        # Canvas setup
        self.canvas = tk.Canvas(
            self.maze_frame,
            width=self.MAZE_SIZE * self.CELL_SIZE,
            height=self.MAZE_SIZE * self.CELL_SIZE,
            bg='white'
        )
        self.canvas.pack()
        
        # Create right frame for buttons and status
        self.right_frame = tk.Frame(self.container_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.Y, pady=20)
        
        # Buttons
        self.solve_button = tk.Button(
            self.right_frame, 
            text="Solve Maze", 
            command=self.solve_maze,
            width=15,
            height=2
        )
        self.solve_button.pack(pady=(0, 10))
        
        self.reset_button = tk.Button(
            self.right_frame, 
            text="Generate New Maze", 
            command=self.reset_maze,
            width=15,
            height=2
        )
        self.reset_button.pack()
        
        # Speed control
        self.speed_label = tk.Label(self.right_frame, text="Animation Speed:")
        self.speed_label.pack(pady=(20, 5))
        self.speed_scale = tk.Scale(
            self.right_frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            length=150
        )
        self.speed_scale.set(50)
        self.speed_scale.pack()
        
        # Status label
        self.status_label = tk.Label(
            self.right_frame, 
            text="Click 'Solve Maze' to start bidirectional search",
            font=('Arial', 10),
            wraplength=150
        )
        self.status_label.pack(pady=(20, 0))
        
        # Legend
        self.create_legend()
        
        # Initialize the display
        self.draw_maze()
    
    def create_legend(self):
        legend_frame = tk.Frame(self.right_frame)
        legend_frame.pack(pady=(20, 0))
        
        tk.Label(legend_frame, text="Legend:", font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Start search
        start_frame = tk.Frame(legend_frame)
        start_frame.pack(fill='x', pady=2)
        tk.Canvas(start_frame, width=20, height=20, bg='#FF9999').pack(side='left', padx=5)
        tk.Label(start_frame, text="Start Search").pack(side='left')
        
        # End search
        end_frame = tk.Frame(legend_frame)
        end_frame.pack(fill='x', pady=2)
        tk.Canvas(end_frame, width=20, height=20, bg='#99FF99').pack(side='left', padx=5)
        tk.Label(end_frame, text="End Search").pack(side='left')
        
        # Final path
        path_frame = tk.Frame(legend_frame)
        path_frame.pack(fill='x', pady=2)
        tk.Canvas(path_frame, width=20, height=20, bg='#F1C40F').pack(side='left', padx=5)
        tk.Label(path_frame, text="Final Path").pack(side='left')

    def generate_complex_maze(self) -> List[List[str]]:
        maze = [['#' for _ in range(self.MAZE_SIZE)] for _ in range(self.MAZE_SIZE)]
        
        def recursive_backtracker(x: int, y: int, visited: Set[Tuple[int, int]]):
            visited.add((x, y))
            maze[x][y] = ' '
            
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                mid_x, mid_y = x + dx // 2, y + dy // 2
                
                if (0 < new_x < self.MAZE_SIZE-1 and 
                    0 < new_y < self.MAZE_SIZE-1 and 
                    (new_x, new_y) not in visited):
                    maze[mid_x][mid_y] = ' '
                    recursive_backtracker(new_x, new_y, visited)

        start_x, start_y = 1, 1
        visited = set()
        recursive_backtracker(start_x, start_y, visited)
        
        maze[1][1] = ' '
        maze[self.MAZE_SIZE-2][self.MAZE_SIZE-2] = ' '
        
        return maze
    
    def draw_maze(self):
        self.canvas.delete("all")
        
        for i in range(self.MAZE_SIZE):
            for j in range(self.MAZE_SIZE):
                x1 = j * self.CELL_SIZE
                y1 = i * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                if self.maze[i][j] == '#':
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill='#2C3E50',
                        outline='#34495E'
                    )
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill='white',
                        outline='#ECF0F1'
                    )
        
        # Draw start position
        start_x = 1 * self.CELL_SIZE + self.CELL_SIZE // 2
        start_y = 1 * self.CELL_SIZE + self.CELL_SIZE // 2
        self.canvas.create_oval(
            start_x - 8, start_y - 8,
            start_x + 8, start_y + 8,
            fill='#2ECC71',
            outline='#27AE60'
        )
        
        # Draw end position
        end_x = (self.MAZE_SIZE-2) * self.CELL_SIZE + self.CELL_SIZE // 2
        end_y = (self.MAZE_SIZE-2) * self.CELL_SIZE + self.CELL_SIZE // 2
        self.canvas.create_oval(
            end_x - 8, end_y - 8,
            end_x + 8, end_y + 8,
            fill='#E74C3C',
            outline='#C0392B'
        )
    
    def visualize_exploration(self, pos: Tuple[int, int], is_start_side: bool):
        """Callback function to visualize the exploration from both sides"""
        x, y = pos
        x1 = y * self.CELL_SIZE
        y1 = x * self.CELL_SIZE
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        
        # Different colors for start and end exploration
        color = '#FF9999' if is_start_side else '#99FF99'  # Light red for start, light green for end
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=color,
            outline='#ECF0F1'
        )
        self.canvas.update()
        
        # Control animation speed
        delay = int(100 - self.speed_scale.get())  # Invert scale so higher = faster
        time.sleep(delay / 1000)  # Convert to seconds
    
    def solve_maze(self):
        self.status_label.config(text="Solving maze using bidirectional search...")
        self.root.update()
        
        # Clear previous solution
        self.draw_maze()
        
        # Find path
        start = (1, 1)
        end = (self.MAZE_SIZE-2, self.MAZE_SIZE-2)
        
        path = self.solver.solve(start, end, self.visualize_exploration)
        
        if path:
            # Draw final path
            for i in range(len(path) - 1):
                current = path[i]
                next_pos = path[i + 1]
                
                # Calculate Manhattan distance between points
                manhattan_dist = abs(current[0] - next_pos[0]) + abs(current[1] - next_pos[1])
                
                # Only draw if points are adjacent
                if manhattan_dist == 1:
                    x1 = current[1] * self.CELL_SIZE + self.CELL_SIZE // 2
                    y1 = current[0] * self.CELL_SIZE + self.CELL_SIZE // 2
                    x2 = next_pos[1] * self.CELL_SIZE + self.CELL_SIZE // 2
                    y2 = next_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2

                    self.canvas.create_line(
                        x1, y1, x2, y2,
                        fill='#F1C40F',
                        width=3,
                        capstyle=tk.ROUND,
                        joinstyle=tk.ROUND
                    )
                    self.canvas.update()
                    time.sleep(0.05)
                
            self.status_label.config(text="Path found! Search completed from both directions.")
        else:
            self.status_label.config(text="No path found!")

    def reset_maze(self):
        self.maze = self.generate_complex_maze()
        self.solver = MazeSolver(self.maze)
        self.draw_maze()
        self.status_label.config(text="Click 'Solve Maze' to start bidirectional search")
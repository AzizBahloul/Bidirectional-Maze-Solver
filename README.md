

**Bidirectional Maze Solver**

**Overview**  
This project is a graphical user interface (GUI) application for a bidirectional maze solver, developed using Python and Tkinter. The application generates a complex maze using a recursive backtracking algorithm and visualizes the solving process using a bidirectional search algorithm.

**Features**  
- Generates a random maze of adjustable complexity.
- Uses a bidirectional search algorithm to find the path from the start to the end.
- Interactive visualization of the maze-solving process, allowing users to see the search in real-time.
- Control over the animation speed of the solver.
- Legend to understand the different visual elements in the maze.

**Requirements**  
To run this application, ensure you have the following installed:  
- Python 3.x  
- Tkinter library (included with most Python installations)  
- Additional libraries if needed for maze generation and solving (e.g., `random`, `time`)

**Installation**  
1. Clone the repository:  
   git clone https://github.com/yourusername/bidirectional-maze-solver.git  
2. Navigate to the project directory:  
   cd bidirectional-maze-solver  
3. Run the application:  
   python main.py  

**Usage**  
- Upon launching the application, a maze will be generated.
- Click on "Solve Maze" to initiate the bidirectional search for the path from the top left to the bottom right of the maze.
- Use the slider to adjust the speed of the animation.
- Click "Generate New Maze" to create a new maze and start the process again.

**Legend**  
- Green Circle: Start of the search  
- Red Circle: End of the search  
- Light Red: Cells explored from the start  
- Light Green: Cells explored from the end  
- Yellow Path: Final path found by the solver  

**Contributing**  
Contributions are welcome! Please feel free to submit a pull request or report issues.


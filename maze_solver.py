from typing import List, Tuple, Optional, Dict, Set, Callable
from collections import deque

class MazeSolver:
    def __init__(self, maze: List[List[str]]):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        neighbors = []
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.rows and 
                0 <= new_y < self.cols and 
                self.maze[new_x][new_y] == ' '):
                neighbors.append((new_x, new_y))
        
        return neighbors

    def construct_path(self, 
                      intersection: Tuple[int, int], 
                      parent_start: Dict[Tuple[int, int], Tuple[int, int]], 
                      parent_end: Dict[Tuple[int, int], Tuple[int, int]]) -> List[Tuple[int, int]]:
        path = []
        current = intersection
        
        # Build path from start to intersection
        while current in parent_start:
            path.append(current)
            current = parent_start[current]
        path.append(current)
        path = path[::-1]
        
        # Build path from intersection to end
        current = intersection
        while current in parent_end:
            current = parent_end[current]
            path.append(current)
        
        return path

    def solve(self, start: Tuple[int, int], end: Tuple[int, int], 
             on_explore: Callable[[Tuple[int, int], bool], None]) -> Optional[List[Tuple[int, int]]]:
        """
        Bidirectional search with visualization callback
        on_explore is called with (position, is_start_side) for visualization
        """
        if start == end:
            return [start]
            
        queue_start = deque([start])
        queue_end = deque([end])
        
        visited_start = {start}
        visited_end = {end}
        
        parent_start = {}
        parent_end = {}
        
        while queue_start and queue_end:
            # Expand from start side
            for _ in range(len(queue_start)):
                current = queue_start.popleft()
                on_explore(current, True)  # Visualize start-side exploration
                
                for neighbor in self.get_neighbors(current):
                    if neighbor in visited_end:
                        parent_start[neighbor] = current
                        return self.construct_path(neighbor, parent_start, parent_end)
                    
                    if neighbor not in visited_start:
                        visited_start.add(neighbor)
                        parent_start[neighbor] = current
                        queue_start.append(neighbor)
            
            # Expand from end side
            for _ in range(len(queue_end)):
                current = queue_end.popleft()
                on_explore(current, False)  # Visualize end-side exploration
                
                for neighbor in self.get_neighbors(current):
                    if neighbor in visited_start:
                        parent_end[neighbor] = current
                        return self.construct_path(neighbor, parent_start, parent_end)
                    
                    if neighbor not in visited_end:
                        visited_end.add(neighbor)
                        parent_end[neighbor] = current
                        queue_end.append(neighbor)
        
        return None
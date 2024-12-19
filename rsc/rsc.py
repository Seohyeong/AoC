class Reader:
    def __init__(self, file_path: str, sep: str = '\n\n'):
        with open(file_path) as f:
            string = ''.join(f)
        self.input_items = string.split(sep)
        
    def get_item(self) -> list[str]:
        return self.input_items
    

class Matrix:
    def __init__(self, string: str):
        self.grid = [list(x) for x in string.split('\n')]
        self.num_row = len(self.grid)
        self.num_col = len(self.grid[0])
    
    def to_list(self) -> list[list[str]]:
        return self.grid
    
    def to_graph(self) -> dict[tuple[int, int]: list[tuple[int, int]]]:
        graph = {}
        for i in range(1, self.num_row - 1):
            for j in range(1, self.num_col - 1):
                if self.grid[i][j] != '#':
                    graph[(i, j)] = []
                    if self.grid[i - 1][j] != '#':
                        graph[(i, j)].append((i - 1, j))
                    if self.grid[i + 1][j] != '#':
                        graph[(i, j)].append((i + 1, j))
                    if self.grid[i][j - 1] != '#':
                        graph[(i, j)].append((i, j - 1))
                    if self.grid[i][j + 1] != '#':
                        graph[(i, j)].append((i, j + 1))
        return graph
                        
    def get_loc(self, item: str) -> tuple[int, int]:
        for i, row in enumerate(self.grid):
            for j, char in enumerate(row):
                if char == item:
                    return (i, j) 
        return None
    
    
def prettyprint(grid):
    for row in grid:
        print(''.join(row))
    print('\n')
        
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
        
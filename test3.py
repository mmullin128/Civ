class Board:
    def __init__(self,board={},boardSize=[0,0]):
        self.board = board
        self.boardSize = boardSize
    def __setitem__(self,space: str,data):
        self.board[space] = data
    def __getitem__(self, space: str):
        return self.board[space]
    def __iter__(self):
        self.itx = 0
        self.ity = 0
        self.it = f'({self.itx}, {self.ity})'
        return self
    def __next__(self):
        if (self.itx == self.boardSize[0]-1):
            self.ity += 1
            self.itx = 0
        else:
            self.itx += 1
        if (self.itx == self.boardSize[0]-1 and self.ity == self.boardSize[1]-1):
            raise StopIteration
        self.it = f'({self.itx}, {self.ity})'
        return self.it
        
    def get_items(self):
        return self.board

b = {
    '(0, 0)': 0,
    '(1, 0)': 1,
    '(2, 0)': 2,
    '(0, 1)': 3,
    '(1, 1)': 1,
    '(2, 1)': 2,
    '(0, 2)': 3,
    '(1, 2)': 2,
    '(2, 2)': 3,
}
s = [3,3]

board = Board(b,s)
for space in board:
    print(board[space])
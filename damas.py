import tkinter as tk

class Piece:
    def __init__(self, color):
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def __str__(self):
        return 'K' if self.king else 'M' if self.color == 'white' else 'm'

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        for i in range(8):
            if i % 2 != 0:
                self.board[0][i] = Piece('black')
                self.board[2][i] = Piece('black')
                self.board[6][i] = Piece('white')
            else:
                self.board[1][i] = Piece('black')
                self.board[5][i] = Piece('white')
                self.board[7][i] = Piece('white')

    def draw(self, canvas):
        for i in range(8):
            for j in range(8):
                x1 = j * 60
                y1 = i * 60
                x2 = x1 + 60
                y2 = y1 + 60
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.board[i][j]
                if piece:
                    piece_color = 'white' if piece.color == 'white' else 'black'
                    canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=piece_color)
                    if piece.king:
                        canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='K', fill='red', font=("Arial", 24))

    def move_piece(self, from_pos, to_pos):
        x1, y1 = from_pos
        x2, y2 = to_pos
        piece = self.board[x1][y1]
        if piece:
            moves = self.get_valid_moves(piece, x1, y1)
            if (x2, y2) in moves:
                self.board[x2][y2] = piece
                self.board[x1][y1] = None
                if abs(x2 - x1) == 2:  # Capturing move
                    mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                    self.board[mid_x][mid_y] = None
                if (piece.color == 'white' and x2 == 0) or (piece.color == 'black' and x2 == 7):
                    piece.make_king()
                return True
        return False

    def get_valid_moves(self, piece, x, y):
        moves = []
        if piece.color == 'white' or piece.king:
            if x > 0:
                if y > 0 and self.board[x-1][y-1] is None:
                    moves.append((x-1, y-1))
                if y < 7 and self.board[x-1][y+1] is None:
                    moves.append((x-1, y+1))
            if x > 1:
                if y > 1 and self.board[x-2][y-2] is None and self.board[x-1][y-1] and self.board[x-1][y-1].color != piece.color:
                    moves.append((x-2, y-2))
                if y < 6 and self.board[x-2][y+2] is None and self.board[x-1][y+1] and self.board[x-1][y+1].color != piece.color:
                    moves.append((x-2, y+2))
        if piece.color == 'black' or piece.king:
            if x < 7:
                if y > 0 and self.board[x+1][y-1] is None:
                    moves.append((x+1, y-1))
                if y < 7 and self.board[x+1][y+1] is None:
                    moves.append((x+1, y+1))
            if x < 6:
                if y > 1 and self.board[x+2][y-2] is None and self.board[x+1][y-1] and self.board[x+1][y-1].color != piece.color:
                    moves.append((x+2, y-2))
                if y < 6 and self.board[x+2][y+2] is None and self.board[x+1][y+1] and self.board[x+1][y+1].color != piece.color:
                    moves.append((x+2, y+2))
        return moves

class CheckersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Damas")
        self.canvas = tk.Canvas(self.root, width=480, height=480)
        self.canvas.pack()
        self.board = Board()
        self.selected_piece = None
        self.turn = 'white'
        self.canvas.bind("<Button-1>", self.click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        self.board.draw(self.canvas)

    def click(self, event):
        row = event.y // 60
        col = event.x // 60
        if self.selected_piece:
            if self.board.move_piece(self.selected_piece, (row, col)):
                self.draw_board()
                self.turn = 'black' if self.turn == 'white' else 'white'
            self.selected_piece = None
        else:
            piece = self.board.board[row][col]
            if piece and piece.color == self.turn:
                self.selected_piece = (row, col)

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersApp(root)
    root.mainloop()

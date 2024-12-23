from game.algorithm.algorithm import Algorithm

from game.algorithm.algorithm import Algorithm

class FourInARow:
    def __init__(self, depth=4, first_player='X'): 
        self.ROWS = 6
        self.COLS = 7
        self.board = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = first_player
        self.alg = Algorithm()
        self.depth = depth  

    def print_board(self):
        print("\n  1   2   3   4   5   6   7")
        for row in self.board:
            print('| ' +  ' | '.join(row) + ' |')

    def drop_piece(self, col):
        if col < 1 or col > self.COLS:
            print("Недопустимая колонка!")
            return False
        col -= 1

        for row in reversed(range(self.ROWS)):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.current_player
                return row  
        print("Колонка уже заполнена!")
        return False

    def check_winner(self):
        return self.alg.check_winner(self.board)

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def play_game(self):
        print("Добро пожаловать в игру 4 в ряд! (7x6)")
        self.print_board()

        while True:
            if self.current_player == 'X':  
                try:
                    col = int(input(f"Игрок {self.current_player}, выберите колонку (1-7): "))
                    row = self.drop_piece(col)
                    if row is not False:
                        self.print_board()
                        if self.check_winner():
                            self.print_board()  
                            print(f"Игрок {self.current_player} победил!")
                            break
                        self.switch_player()
                    else:
                        print("Попробуйте снова!")
                except ValueError:
                    print("Введите корректный номер колонки!")
            else: 
                print(f"Ход компьютера ({self.current_player}):")
                best_score = float('-inf')
                best_col = None

                for col in range(7):
                    if self.alg.is_valid_move(self.board, col):
                        row = self.alg.get_next_open_row(self.board, col)
                        new_board = self.alg.make_new_board(self.board, row, col, 'O')
                        score = self.alg.minimax(new_board, self.depth, float('-inf'), float('inf'), False)  
                        if score > best_score:
                            best_score = score
                            best_col = col

                if best_col is not None:
                    row = self.drop_piece(best_col + 1)
                    self.print_board()
                    if self.check_winner():
                        print(f"Игрок {self.current_player} победил!")
                        break
                    self.switch_player()

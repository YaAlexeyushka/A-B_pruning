class Algorithm:
    def estimate_window(self, window):
        score = 0
        player_count = window.count('O')
        opponent_count = window.count('X')
        
        if player_count == 4:
            score += 10000
        elif player_count == 3 and opponent_count == 0:
            score += 100
        elif player_count == 2 and opponent_count == 0:
            score += 10
        elif player_count == 1 and opponent_count == 0:
            score += 1
            
        elif opponent_count == 4:
            score -= 10000
        elif opponent_count == 3 and player_count == 0:
            score -= 100
        elif opponent_count == 2 and player_count == 0:
            score -= 10
        elif opponent_count == 1 and opponent_count == 0:
            score += 1
        
        return score
    
    def estimate_board(self, board):
        score = 0
        
        center_col = [board[row][3] for row in range(6)]
        center_count = center_col.count('O')
        score += center_count * 6
        
        for row in range(6):
            for col in range(4):  
                window = [board[row][col + i] for i in range(4)]
                score += self.estimate_window(window)
        
        for col in range(7):
            for row in range(3):  
                window = [board[row + i][col] for i in range(4)]
                score += self.estimate_window(window)
        
        for row in range(3):
            for col in range(4):
                window = [board[row + i][col + i] for i in range(4)]
                score += self.estimate_window(window)
        
        for row in range(3):
            for col in range(3, 7):
                window = [board[row + i][col - i] for i in range(4)]
                score += self.estimate_window(window)
        
        return score

    def is_valid_move(self, board, col):
        return board[0][col] == ' '  

    def get_next_open_row(self, board, col):
        for row in range(5, -1, -1):  
            if board[row][col] == ' ':
                return row
        return -1  

    def make_new_board(self, board, row, col, player):
        new_board = [row.copy() for row in board] 
        new_board[row][col] = player
        return new_board

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_final_vertex(board):
            return self.estimate_board(board)
        
        if maximizing_player:
            max_estim = float('-inf')
            for column in range(7):
                if self.is_valid_move(board, column):
                    row = self.get_next_open_row(board, column)
                    new_board = self.make_new_board(board, row, column, 'O')  
                    estim = self.minimax(new_board, depth-1, alpha, beta, False)
                    max_estim = max(max_estim, estim)
                    alpha = max(alpha, estim)
                    if beta <= alpha:
                        break
            return max_estim
        else:
            min_estim = float('inf')
            for column in range(7):
                if self.is_valid_move(board, column):
                    row = self.get_next_open_row(board, column)
                    new_board = self.make_new_board(board, row, column, 'X')  
                    estim = self.minimax(new_board, depth-1, alpha, beta, True)
                    min_estim = min(min_estim, estim)
                    beta = min(beta, estim)
                    if beta <= alpha:
                        break
            return min_estim

    def is_final_vertex(self, board):
        return self.check_winner(board) or all(board[0][col] != ' ' for col in range(7))

    def check_winner(self, board):
        for row in range(6):
            for col in range(7):
                if board[row][col] == ' ':
                    continue
                if self.check_direction(board, row, col, 1, 0) or \
                   self.check_direction(board, row, col, 0, 1) or \
                   self.check_direction(board, row, col, 1, 1) or \
                   self.check_direction(board, row, col, 1, -1):
                    return True
        return False

    def check_direction(self, board, row, col, d_row, d_col):
        piece = board[row][col]
        for i in range(1, 4):
            r, c = row + i * d_row, col + i * d_col
            if not (0 <= r < 6 and 0 <= c < 7) or board[r][c] != piece:
                return False
        return True

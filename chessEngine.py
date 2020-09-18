class GameStart:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.move_functions = {"p": self.pawn_moves, "R": self.rook_moves, "N": self.knight_moves,
                               "B": self.bishoop_moves, "Q": self.queen_moves, "K": self.king_moves}
        self.moveLog = []
        self.whiteToMove = True
        self.checkmate = False
        self.stalemate = False
        self.black_king = (0, 4)
        self.white_king = (7, 4)
        self.empassantPossible = ()

    def make_move(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # swap players

        if move.pieceMoved == "bK":
            self.black_king = (move.endRow, move.endCol)
        if move.pieceMoved == "wK":
            self.white_king = (move.endRow, move.endCol)

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch Turns back

            if move.pieceMoved == "bK":
                self.black_king = (move.startRow, move.startCol)
            if move.pieceMoved == "wK":
                self.white_king = (move.startRow, move.startCol)

    def valid_moves(self):
        moves = self.all_possible_moves()

        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.in_check():
                moves.remove(moves[i])  # if they attack your king not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.stalemate = False
            self.checkmate = False
        return moves

    def all_possible_moves(self):  # considering without check
        moves = [Move((6, 4), (4, 4), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves)
        return moves

    def in_check(self):
        if self.whiteToMove:
            return self.under_attack(self.white_king[0], self.white_king[1])
        else:
            return self.under_attack(self.black_king[0], self.black_king[1])

    def under_attack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opps turn
        ops_moves = self.all_possible_moves()
        self.whiteToMove = not self.whiteToMove  # back to your turn
        for move in ops_moves:
            if move.endRow == r and move.endCol == c:  # under attack
                return True
        return False

    def pawn_moves(self, r, c, moves):
            if self.whiteToMove:
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
# kll the black pawns
                if c - 1 >= 0:  # kill to the left
                    if self.board[r - 1][c - 1][0] == "b":  # enemy piece to kill
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                if c + 1 <= 7:  # kill to the right
                    if self.board[r - 1][c + 1][0] == "b":
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
            else:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if c - 1 >= 0:
                    if self.board[r + 1][c - 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if c + 1 <= 7:  # kill to the right
                    if self.board[r + 1][c + 1][0] == "w":
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def rook_moves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    endpiece = self.board[end_row][end_col]
                    if endpiece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif endpiece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def knight_moves(self, r, c, moves):
        knight_directions = ((-2, -1), (-1, -2), (-2, 1), (2, -1), (-1, 2), (1, -2), (1, 2),  (2, 1))
        enemycolor = "w" if self.whiteToMove else "b"
        for km in knight_directions:
            end_row = r + km[0]
            end_col = c + km[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                endpiece = self.board[end_row][end_col]
                if endpiece[0] != enemycolor:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def bishoop_moves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # top left, #topright #bottom left #bottom right
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    endpiece = self.board[end_row][end_col]
                    if endpiece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif endpiece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def queen_moves(self, r, c, moves):
        self.bishoop_moves(r, c, moves)
        self.rook_moves(r, c, moves)

    def king_moves(self, r, c, moves):
        moves_king = ((-1, -1), (1, -1), (-1, 1), (1, 1), (-1, 0),  (0, -1), (0, 1),  (1, 0))
        enemy_color = "b" if self.whiteToMove else "w"
        for i in range(8):
            end_row = r + moves_king[i][0]
            end_col = c + moves_king[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                endpiece = self.board[end_row][end_col]
                if endpiece[0] != enemy_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))


class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board, isempassantmove = False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):  # overriding the object
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def get_chess_notation(self):
            return self.get_rank_file(self.startRow, self.startCol) + self.get_rank_file(self.endRow, self.endCol)

    def get_rank_file(self, r, c):
            return self.colsToFiles[c] + self.rowsToRanks[r]

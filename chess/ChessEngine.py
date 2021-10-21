"""
This class is responsible for storing all the information about the current state of a chess gameIt will also be
responsible for determining the valid moves at the current state. It wll also kep a move log
"""

class GameState():
    def __init__(self):
        # The board is in 8x8 and each element of the list has 2 characters
        # 1st characterrepresent the color of keys (b/w), 2nd character represents the type of the piece
        # K, Q, R, B, N or P
        # The string epty epresents an empty space with no keys
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []


    """
    Takes a move as a parameter and executes it (This will not work for castling, pawn promotion and en pessant
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)#TO display the history
        self.whiteToMove = not self.whiteToMove# swap players

    """Undo the last move"""
    def undoMove(self):
        if len(self.moveLog) != 0: #makes sure that there is a move
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Switch turn back

    """All moves considering checks"""
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    """All moves without considering checks"""
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    """Get all the valid pawn moves for the pawn located at row and col and add these to th list"""
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == '--': #1 square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c - 1 >= 0: #checks for left
                if self.board[r-1][c-1][0] == 'b': # there is an enemy piece to capture on left
                    moves.append(Move((r, c), (r - 1, c-1), self.board))
            if c+1 <= 7: #captures for right
                if self.board[r-1][c+1][0] == 'b': # there is an enemy piece to capture on right
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        else:
            if self.board[r+1][c] == '--': #1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+1][c] == '--': #2 square move
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:  # checks for left
                if self.board[r+1][c-1][0] == 'w':  # there is an enemy piece to capture on left
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: #checks for right
                if self.board[r+1][c+1][0] == 'w': # there is an enemy piece to capture on right
                    moves.append(Move((r, c),(r+1, c+1), self.board))


    """Get all the valid rook moves for the pawn located at row and col and add these to th list"""
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i;
                endCol = c + d[1] * i;
                if 0 <= endRow < 8 and 0 <= endCol < 8: #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: #enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #friendly piece invalid
                        break
                else: #off board
                    break

    """Get all the valid knight moves for the pawn located at row and col and add these to th list"""
    def getKnightMoves(self, r, c, moves):
        pass


    """Get all the valid bishop moves for the pawn located at row and col and add these to th list"""
    def getBishopMoves(self, r, c, moves):
        pass


    """Get all the valid queen moves for the pawn located at row and col and add these to th list"""
    def getQueenMoves(self, r, c, moves):
        pass


    """Get all the valid king moves for the pawn located at row and col and add these to th list"""
    def getKingMoves(self, r, c, moves):
        pass


class Move:
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    """Overriding the equal method"""
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]












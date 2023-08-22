class gamestate():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        
        self.whitetomove = True
        self.movelog = []

        self.movefunctions = {"p": self.getpawnmoves, "R": self.getrookmoves, "N": self.getknightmoves, "B": self.getbishopmoves, "Q": self.getqueenmoves, "K": self.getkingmoves}

        self.whitekinglocation = (7, 4)
        self.blackkinglocation = (0, 4)
        self.incheck = False
        self.enpassentpossible = ()
        self.pins = []
        self.checks = []

    def makmove(self, move):
        self.board[move.startrow][move.startcol] = "--"
        self.board[move.endrow][move.endcol] = move.peicemoved
        self.movelog.append(move)
        self.whitetomove = not self.whitetomove
        if move.peicemoved == 'wK':
            self.whitekinglocation = (move.endrow, move.endcol)
        elif move.peicemoved == 'bK':
            self.blackkinglocation = (move.endrow, move.endcol)

        if move.ispawnpromotion:
            self.board[move.endrow][move.endcol] = move.peicemoved[0] + 'Q'
    def getvalidmoves(self):
        moves = []
        self.incheck, self.pins, self.checks = self.checkforpinsandchecks()

        if self.whitetomove:
            kingrow = self.whitekinglocation[0]
            kingcol = self.whitekinglocation[1]
        else:
            kingrow = self.blackkinglocation[0]
            kingcol = self.blackkinglocation[1]

        if self.incheck:
            if len(self.checks) == 1:
                moves = self.getallmoves()
                check = self.checks[0]
                checkrow = check[0]
                checkcol = check[1]
                piecechecking = self.board[checkrow][checkcol]
                validsquares = []
                if piecechecking[1] == 'N':
                    validsquares = [(checkrow, checkcol)]
                else:
                    for i in range(1, 8):
                        validsquare = (kingrow + check[2] * i, kingcol + check[3] * i)
                        validsquares.append(validsquare)
                        if validsquare[0] == checkrow and validsquare[1] == checkcol:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].peicemoved [1] != 'K':
                        if not (moves[i].endrow, moves[i].endcol) in validsquares:
                            moves.remove(moves[i])
            else:
                self.getkingmoves(kingrow, kingcol, self.board)
        else:
            moves = self.getallmoves()

        return moves


    def getallmoves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if(turn == "w" and self.whitetomove) or (turn == "b" and not self.whitetomove):
                    piece = self.board[i][j][1]

                    self.movefunctions[piece](i, j, moves)
        return moves

    def getpawnmoves(self, i, j, moves):
        piecepinned = False
        pindirection = ()

        for p in range(len(self.pins)-1, -1, -1):
            if self.pins[p][0] == i and self.pins[p][1] == j:
                piecepinned = True
                pindirection = (self.pins[p][2], self.pins[p][3])
                self.pins.remove(self.pins[p])
                break

        if self.whitetomove:
            if self.board[i - 1][j] == "--":
                if not piecepinned or pindirection == (-1, 0):
                    moves.append(move((i, j), (i - 1, j), self.board))
                    if i == 6 and self.board[i - 2][j] == "--":
                        moves.append(move((i, j), (i - 2, j), self.board))

            if j - 1 >= 0:
                if self.board[i - 1][j - 1][0] == "b":
                    if not piecepinned or pindirection == (-1, -1):
                        moves.append(move((i, j), (i - 1, j - 1), self.board))

            if j + 1 <= 7:
                if self.board[i - 1][j + 1][0] == "b":
                    if not piecepinned or pindirection == (-1, 1):
                        moves.append(move((i, j), (i - 1, j + 1), self.board))
        else:
            if self.board[i + 1][j] == "--":
                if not piecepinned or pindirection == (1, 0):
                    moves.append(move((i, j), (i + 1, j), self.board))
                    if i == 1 and self.board[i + 2][j] == "--":
                        moves.append(move((i, j), (i + 2, j), self.board))

            if j - 1 >= 0:
                if self.board[i + 1][j - 1][0] == "w":
                    if not piecepinned or pindirection == (1, -1):
                        moves.append(move((i, j), (i + 1, j - 1), self.board))

            if j + 1 <= 7:
                if self.board[i + 1][j + 1][0] == "w":
                    if not piecepinned or pindirection == (1, 1):
                        moves.append(move((i, j), (i + 1, j + 1), self.board))


    def getrookmoves(self, i, j, moves):
        piecepinned = False
        pindirection = ()
        for p in range(len(self.pins)-1, -1, -1):
            if self.pins[p][0] == i and self.pins[p][1] == j:
                piecepinned = True
                pindirection = (self.pins[p][2], self.pins[p][3])
                if self.board[i][j][1] != "Q":
                    self.pins.remove(self.pins[p])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemycolor = "b" if self.whitetomove else "w"
        for d in directions:
            for p in range(1, 8):
                endrow = i + d[0] * p
                endcol = j + d[1] * p

                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    if not piecepinned or pindirection == d or pindirection == (-d[0], -d[1]):
                        endpiece = self.board[endrow][endcol]

                        if endpiece == "--":
                            moves.append(move((i, j), (endrow, endcol), self.board))
                        elif endpiece[0] == enemycolor:
                            moves.append(move((i, j), (endrow, endcol), self.board))
                            break
                        else:
                            break
                else:
                    break

    def getqueenmoves(self, i, j, moves):
        self.getbishopmoves(i, j, moves)
        self.getrookmoves(i, j, moves)

    def getbishopmoves(self, i, j, moves):
        piecepinned = False
        pindirection = ()

        for p in range(len(self.pins) - 1, -1, -1):
            if self.pins[p][0] == i and self.pins[p][1] == j:
                piecepinned = True
                pindirection = (self.pins[p][2], self.pins[p][3])
                self.pins.remove(self.pins[p])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemycolor = "b" if self.whitetomove else "w"
        for d in directions:
            for p in range(1, 8):
                endrow = i + d[0] * p
                endcol = j + d[1] * p

                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    if not piecepinned or pindirection == d or pindirection == (-d[0], -d[1]):
                        endpiece = self.board[endrow][endcol]
                        if endpiece == "--":
                            moves.append(move((i, j), (endrow, endcol), self.board))
                        elif endpiece[0] == enemycolor:
                            moves.append(move((i, j), (endrow, endcol), self.board))
                            break
                        else:
                            break
                else:
                    break
    def getknightmoves(self, i, j, moves):
        piecepinned = False

        for p in range(len(self.pins) - 1, -1, -1):
            if self.pins[p][0] == i and self.pins[p][1] == j:
                piecepinned = True
                self.pins.remove(self.pins[p])
                break

        knightsmoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allycolor = "w" if self.whitetomove else "b"

        for m in knightsmoves:
            endrow = i + m[0]
            endcol = j + m[1]

            if 0 <= endrow < 8 and 0 <= endcol < 8:
                if not piecepinned:
                    endpiece = self.board[endrow][endcol]

                    if endpiece[0] != allycolor:
                        moves.append(move((i, j), (endrow, endcol), self.board))
    def getkingmoves(self, i, j, moves):
        rowmoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colmoves = (-1, 0, 1, -1, 1, -1, 0, 1)

        allycolor = "w" if self.whitetomove else "b"
        for p in range(8):
            endrow = i + rowmoves[p]
            endcol = j + colmoves[p]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                if allycolor == "w":
                    self.whitekinglocation = (endrow, endcol)
                else:
                    self.blackkinglocation = (endrow, endcol)

                incheck, pins, checks = self.checkforpinsandchecks()

                if not incheck:
                    moves.append(move((i, j), (endrow, endcol), self.board))

                if allycolor == "w":
                    self.whitekinglocation = (i, j)
                else:
                    self.blackkinglocation = (i, j)

    def checkforpinsandchecks(self):
        pins = []
        checks = []
        incheck = []
        if self.whitetomove:
            enemycolor = "b"
            allycolor = "w"
            startrow = self.whitekinglocation[0]
            startcol = self.whitekinglocation[1]
        else:
            enemycolor = "w"
            allycolor = "b"
            startrow = self.blackkinglocation[0]
            startcol = self.blackkinglocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for i in range(len(directions)):
            d = directions[i]
            possiblepin = ()
            for j in range(1, 8):
                endrow = startrow + d[0] * j
                endcol = startcol + d[1] * j
                if 0 <= endrow < 8 and 0 <= endcol < 8:
                    endpiece = self.board[endrow][endcol]
                    if endpiece[0] == allycolor:
                        if possiblepin == ():
                            possiblepin = (endrow, endcol, d[0], d[1])
                        else:
                            break
                    elif endpiece[0] == enemycolor:
                        type = endpiece[1]
                        if(0 <= i <= 3 and type == 'R') or \
                            (4 <= i <= 7 and type == "B") or \
                                (j == 1 and type == "p" and ((enemycolor == "w" and 6 <= i <= 7) or (enemycolor == "b" and 4 <= i <= 5))) or \
                                (type == "Q") or (j == 1 and type == "K"):
                            if possiblepin == ():
                                incheck = True
                                checks.append((endrow, endcol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblepin)
                                break
                        else:
                            break
        knightsmoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightsmoves:
            endrow = startrow + m[0]
            endcol = startcol + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] == enemycolor and endpiece[1] == 'N':
                    incheck = True
                    checks.append((endrow, endcol, m[0], m[1]))
        return incheck, pins, checks
class move():
    rankstorow = {"1": 7, "2": 6, "3": 5, "4": 4,
                  "5": 3, "6": 2, "7": 1, "8": 0}

    rowstoranks = {v: k for k, v in rankstorow.items()}

    filestocol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    coltofiles = {v: k for k, v in filestocol.items()}


    def __init__(self, startsq, endsq, board):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.peicemoved = board[self.startrow][self.startcol]
        self.peicecaptured = board[self.endrow][self.endcol]
        self.ispawnpromotion = False
        if(self.peicemoved == "wp" and self.endrow == 0) or (self.peicemoved == "bp" and self.endrow == 7):
            self.ispawnpromotion = True
        self.moveid = self.startrow * 1000 + self.startcol * 100 + self.endrow * 10 + self.endcol

    def __eq__(self, other):
        if isinstance(other, move):
            return self.moveid == other.moveid
        return False

    def getchessnotation(self):
        return self.getrankfile(self.startrow, self.startcol) + self.getrankfile(self.endrow, self.endcol)

    def getrankfile(self, i, j):
        return self.coltofiles[j] + self.rowstoranks[i]
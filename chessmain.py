import pygame as p
import chessengine

width = height = 512
dimension = 8
SQ_size = height // dimension
print(SQ_size)
maxfps = 15
images = {}


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_size, SQ_size))
    
    
def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))
    gs = chessengine.gamestate()
    validmoves = gs.getvalidmoves()
    movemade = False
    load_images()
    running = True
    sqselected = ()
    playerclicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_size
                row = location[1] // SQ_size
                if sqselected == (row, col):
                    sqselected = ()
                    playerclicks = []
                else:
                    sqselected = (row, col)
                    playerclicks.append(sqselected)
                if len(playerclicks) == 2:
                    move = chessengine.move(playerclicks[0], playerclicks[1], gs.board)
                    print(move.getchessnotation())
                    for i in range(len(validmoves)):
                        if move in validmoves[i]:
                            gs.makmove(move)
                            movemade = True
                            sqselected = ()
                            playerclicks = []
                    else:
                        playerclicks = [sqselected]
        if movemade:
            validmoves = gs.getvalidmoves()
            movemade = False
        drawgamestate(screen, gs)
        clock.tick(maxfps)
        p.display.flip()
    

def drawgamestate(screen, gs):
    drawboard(screen)
    drawpieces(screen, gs.board)

def drawboard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for i in range(dimension):
        for j in range(dimension):
            color = colors[((i + j) % 2)]
            p.draw.rect(screen, color, p.Rect(i*SQ_size, j*SQ_size, SQ_size, SQ_size))
    
    
def drawpieces(screen, board):
    for i in range(dimension):
        for j in range(dimension):
            piece = board[i][j]

            if piece != "--":

                screen.blit(images[piece], p.Rect(j*SQ_size, i*SQ_size, SQ_size, SQ_size))
            
if __name__ == "__main__":
    main()
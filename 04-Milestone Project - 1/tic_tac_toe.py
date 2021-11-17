def display(board):
    print(board[0])
    print(board[1])
    print(board[2])

def get_coordinates():
    complete = False
    x = 0
    y = 0
    while (not complete):
        result = input("Please enter a coordinate as X,Y: ")
        if ',' not in result:
            print('Comma not found. Enter coordinate in X,Y format.')
            continue
        coords = result.split(",")
        try:
            x = int(coords[0])
            y = int(coords[1])
        except ValueError:
            print('One of the coordinates could not be converted to an int.')
            continue
        if (0 <= x <= 2 and 0 <= y <= 2):
            complete = True
        else:
            print('X and Y values must be between 0 and 2 inclusive.')
    return [x,y]

def get_player(turn):
    return 2 if turn % 2 == 0 else 1

def get_token(player):
    return 'X' if player == 1 else 'O'

def is_win(board, player):
    val = get_token(player)
    if (board[0][0] == val and board[1][1] == val and board[2][2] == val):
        return True
    if (board[2][0] == val and board[1][1] == val and board[0][2] == val):
        return True
    for i in range(0,3):
        if (board[i][0] == val and board[i][1] == val and board[i][2] == val):
            return True
        if (board[0][i] == val and board[1][i] == val and board[2][i] == val):
            return True
    return False

def get_turn_wins(board, player):
    print(f'Player {player} Turn!')
    turnDone = False
    while (not turnDone):
        coordinate = get_coordinates()
        x = coordinate[0]
        y = coordinate[1]
        if (board[y][x] != ' '):
            print('Uh Oh! That space is already occupied, please pick another.')
        else:
            board[y][x] = get_token(player)
            turnDone = True
    return True if is_win(board, player) else False

def print_demo():
    demoboard = [['0,0','0,1','0,2'],['1,0','1,1','1,2'],['2,0','2,1','2,2']]
    display(demoboard)
    print('Feel free to scroll up if you ever forget how the cooridnates work!')
    print('----')

def play_game():
    print('Welcome! See the example below to know which coordinates are which.')
    board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    gameOver = False
    turn = 1
    print_demo()
    while (not gameOver):
        display(board)
        if (turn == 10):
            print('The game is a draw!')
            break
        player = get_player(turn)
        if (get_turn_wins(board, player)):
            display(board)
            print(f'Congratulations! Player {player} wins!')
            gameOver = True
        else:
            turn += 1

play_game()
"""
----------------------------------------
Project Name      : Gomoku Simulation
Project Start Time: May 12th, 2014
Project Type      : Simulation/Game
Language Used     : Python 3.4.0
License           : GNU GPL 3
Interface         : Text-based/No GUI
Author(s)         : Jiahui Xie
Version           : 0.1
Final             : No
----------------------------------------
"""
def main() -> None:
    print("-" * 40)
    print("Welcome to the Gomoku Simulation")
    print("-" * 40)
    start_choice = int(input("Press 1 and enter to start the game, 2 to exit > "))

    if start_choice == 1:
        gomoku_main(chessboard_size = 5)
        
    elif start_choice == 2:
        print("Program exited!")

def gomoku_main(*, chessboard_size: int = 0) -> None:
    """
    2 players are denoted by O and X, respectively.
    """
    chessboard = [[None] * chessboard_size for i in range(chessboard_size)]
    player_cycle = 0; info_hint = 1
    
    while not winning_check(chessboard):

        if info_hint:
            print("-" * 40)
            print("Please be aware that both players have to enter the row and\n + \
                  column numbers that they would like to place their pieces!")
            print("Player A is denoted by O, Player B is denoted by X")
            print("-" * 40)
            info_hint -= 1
            
        if player_cycle == 0:   # Please note that this conditional clause ASSUME the player make no mistakes
            print("-" * 40)
            print("Player A's turn!")
            row_number = int(input("Please enter the row number > "))
            col_number = int(input("Please enter the column number > "))
            coordinate = (row_number, col_number)
            chessboard = update_chessboard(board_input = chessboard, position = coordinate, player = player_cycle)
            player_cycle += 1
            continue

        elif player_cycle == 1: # ASSUME no mistakes made by players
            print("-" * 40)
            print("Player B's turn!")
            row_number = int(input("Please enter the row number > "))
            col_number = int(input("Please enter the column number > "))
            coordinate = (row_number, col_number)
            chessboard = update_chessboard(board_input = chessboard, position = coordinate, player = player_cycle)
            player_cycle -= 1
            continue

    print("-" * 40)
    print("Player %s Win!\nGame ends here!" %winning_check(chessboard))
    print(chessboard)
    print("-" * 40)

def update_chessboard(*, board_input: list = [], position: tuple = (), player: int = 0) -> list:

    #update = lambda inp, pos, plyr: inp[pos[0]][pos[1]] = plyr

    #update(board_input, position, 'O') if player == 0 else update(board_input, position, 'X')

    board_input[position[0]][position[1]] = 'O' if player == 0 else 'X'
    return board_input

def winning_check(board: list = []) -> (bool, str):

    # Handles row
    for row in board:           
        if len(set(row)) == 1:

            if row[0] == 'O':
                return 'A'

            elif row[0] == 'X':
                return 'B'

    # Handles column
    col_entry = [[row[i] for row in board] for i in range(len(board))]
    
    for col in col_entry:

        if len(set(col)) == 1:

            if col[0] == 'O':
                return 'A'

            elif col[0] == 'X':
                return 'B'

    # Handles diagonal
    diagonal_entry = [board[i][i] for i in range(len(board))]

    if len(set(diagonal_entry)) == 1: 
        
        if row[0] == 'O':
            return 'A'

        elif row[0] == 'X':
            return 'B'

    # Handles anti-diagonal

    # ----------------------------------------
    # The following lines are obsolete
    # ----------------------------------------

    #anti_diag_count = len(board) - 1
    #anti_diag_entry = []
    #for row in board:
    #    anti_diag_entry.append(row[anti_diag_count])
    #    anti_diag_count -= 1
    #
    #if len(set(anti_diag_entry)) == 1:
    #
    #    if anti_diag_entry[0] == 'O':
    #        return 'A'
    #
    #    elif anti_diag_entry[0] == 'X':
    #        return 'B'
    # ----------------------------------------

    anti_diag_entry = [board[i][len(board) - 1 - i] for i in range(len(board))]
    
    if len(set(anti_diag_entry)) == 1:

        if anti_diag_entry[0] == 'O':
            return 'A'

        elif anti_diag_entry[0] == 'X':
            return 'B'
            
    return False
    
main()
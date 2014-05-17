"""
----------------------------------------
Project Name      : Gomoku Simulation
Project Start Time: May 12th, 2014
Project Type      : Simulation/Game
Language Used     : Python 3.4.0
License           : GNU GPL 3
Interface         : Text-based/No GUI
Author(s)         : Jiahui Xie
Version           : 0.2
Final             : No
----------------------------------------
"""
def main() -> None:
    print("-" * 40)
    print("Welcome to the Gomoku Simulation")
    print("-" * 40)
    start_choice = int(input("Press 1 and enter to start the game, 2 to exit > "))

    if start_choice == 1:
        gomoku_main(chessboard_size = 9)
        
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
            draw_ascii_chessboard(chessboard)
            
        if player_cycle == 0:   # Please note that this conditional clause ASSUME the player make no mistakes
            print("-" * 40)
            print("Player A's turn!")
            row_number = int(input("Please enter the row number > "))
            col_number = int(input("Please enter the column number > "))
            coordinate = (row_number, col_number)
            chessboard = update_chessboard(board_input = chessboard, position = coordinate, player = player_cycle)
            player_cycle += 1
            draw_ascii_chessboard(chessboard)
            continue

        elif player_cycle == 1: # ASSUME no mistakes made by players
            print("-" * 40)
            print("Player B's turn!")
            row_number = int(input("Please enter the row number > "))
            col_number = int(input("Please enter the column number > "))
            coordinate = (row_number, col_number)
            chessboard = update_chessboard(board_input = chessboard, position = coordinate, player = player_cycle)
            player_cycle -= 1
            draw_ascii_chessboard(chessboard)
            continue

    print("-" * 40)
    print("Player %s Win!\nGame ends here!" %winning_check(chessboard))
    print(chessboard)
    print("-" * 40)

def update_chessboard(*, board_input: list = [], position: tuple = (), player: int = 0) -> list:

    #update = lambda inp, pos, plyr: inp[pos[0]][pos[1]] = plyr

    #update(board_input, position, 'O') if player == 0 else update(board_input, position, 'X')
    if board_input[position[0]][position[1]] == None:
        board_input[position[0]][position[1]] = 'O' if player == 0 else 'X'
        return board_input

    elif board_input[position[0]][position[1]] in 'OX':

        if player == 0:
            print("You cannot place anoter piece onto the previous one!")
        elif player == 1:
            print("You cannot place your piece onto the other player's!")
            
def winning_check(board_input: list = []) -> (bool, str):

    # Handles row
    for row in board_input:   

        if determine_winner(mode = "count", line_input = row):

            return determine_winner(mode = "count", line_input = row)
            
    # Handles column
    col_entry = [[row[i] for row in board_input] for i in range(len(board_input))]
    
    for col in col_entry:

        if determine_winner(mode = "count", line_input = col):

            return determine_winner(mode = "count", line_input = col)
            
    # Handles diagonal
    for row_ind in range(len(board_input)):
        
        for col_ind in range(len(board_input)):
            
            # Case I: Upper diagonal antenna
            if row_ind > 3:

                # Upper Left
                if col_ind > 3:
                    obsr_list = []
                    for link_ind in range(5):
                        
                        obsr_list.append(board_input[row_ind - link_ind][col_ind - link_ind])

                    if determine_winner(line_input = obsr_list):
                        
                        return determine_winner(line_input = obsr_list)
                            
                # Upper right
                if (len(board_input) - 1 - col_ind) > 3:
                    obsr_list = []
                    for link_ind in range(5):
                        
                        obsr_list.append(board_input[row_ind - link_ind][col_ind + link_ind])
                        
                    if determine_winner(line_input = obsr_list):

                        return determine_winner(line_input = obsr_list)
                            
            # Case II: Lower diagonal antenna
            if (len(board_input) - 1 - row_ind) > 3:
                
                # Lower Left
                if col_ind > 3:
                    obsr_list = []
                    for link_ind in range(5):
                        
                        obsr_list.append(board_input[row_ind + link_ind][col_ind - link_ind])
                        
                    if determine_winner(line_input = obsr_list):

                        return determine_winner(line_input = obsr_list)
                            
                # Lower Right
                if (len(board_input) - 1 - col_ind) > 3:
                    obsr_list = []
                    for link_ind in range(5):
                        
                        obsr_list.append(board_input[row_ind + link_ind][col_ind + link_ind])

                    if determine_winner(line_input = obsr_list):

                        return determine_winner(line_input = obsr_list)
                            
    # ----------------------------------------
    # The following lines are obsolete
    # ----------------------------------------
    # Handles diagonal
    #diagonal_entry = [board[i][i] for i in range(len(board))]
    #
    #if len(set(diagonal_entry)) == 1: 
    #    
    #    if row[0] == 'O':
    #        return 'A'
    #
    #    elif row[0] == 'X':
    #        return 'B'
    #
    # Handles anti-diagonal
    #
    #anti_diag_entry = [board[i][len(board) - 1 - i] for i in range(len(board))]
    #
    #if len(set(anti_diag_entry)) == 1:
    #
    #    if anti_diag_entry[0] == 'O':
    #        return 'A'
    #
    #    elif anti_diag_entry[0] == 'X':
    #        return 'B'
    # ----------------------------------------
    
def determine_winner(mode = "oblique", *, line_input: list = []) -> (bool, str):
    """
    This function is only meant to be used given the "line_input"
    passed is an actual list.
    """
    if mode == "oblique":
        if (line_input) and (len(set(line_input)) == 1):

            if line_input[0] == 'O':
                return 'A'

            elif line_input[0] == 'X':
                return 'B'
            
        return False
            
    elif mode == "count":
        if line_input:
            player1_count = player2_count = pointer = 0; following_entry = line_input[1]
            
            while (pointer < len(line_input)) and (player1_count < 5) and (player2_count < 5):

                if line_input[pointer] == 'O':

                    if following_entry == 'O':
                        player1_count += 1 if (player1_count != 0) else 2
                        print(player1_count)
                    else:
                        player1_count = 0

                elif line_input[pointer] == 'X':

                    if following_entry == 'X':
                        player2_count += 1 if (player2_count != 0) else 2

                    else:
                        player2_count = 0

                pointer += 1
                following_entry = line_input[pointer + 1] if (pointer + 1) < len(line_input) else None
                
            if player1_count > 4:
                return 'A'
                
            elif player2_count > 4:
                return 'B'
                
            return False
                    
def draw_ascii_chessboard(board_input: list = []) -> None:
    "Void Function"
    print("_" * (len(board_input) * 2 + 1))

    for row in board_input:

        for entry in row:
            print("|", end = '')
            print(" ", end = '') if entry == None else print(entry, end = '')

        print("|")
        print("-" * (len(board_input) * 2 + 1))
main()
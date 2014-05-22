"""
----------------------------------------
Project Name      : Gomoku Simulation
Project Start Time: May 12th, 2014
Project Type      : Simulation/Game
Language Used     : Python 3.4.0
License           : GNU GPL 3
Interface         : Text-based/No GUI
Author(s)         : Jiahui Xie
Version           : 0.4
Final             : No
----------------------------------------
"""
def main() -> None:
    """
    Top Level Starter
    Handles the start or the exit of the program.
    ----------------------------------------
    Version Change Notice
    ----------------------------------------
    0.4    Conditional clause added to read auto-save file.
    ----------------------------------------
    """
    import os, pickle
    
    print("-" * 40)
    print("Welcome to the Gomoku Simulation")
    print("-" * 40)
    start_choice = input("Press 1 and enter to start the game, 2 to exit > ")

    # Error Checking Block
    while True:
        if ((start_choice.isdigit()) and (start_choice in '12') and (len(start_choice) == 1)): 
            break
        start_choice = input("Invalid Input! You must enter either 1 or 2 > ")
        
    if start_choice in '1':

        # Chessboard-loader
        if os.getcwd()[-3:] == "sav":
            pass
        else:
            os.chdir("sav")
            
        try:
            with open("gomoku_autosave", "rb") as saved_status_data:
                chessboard_saved_input, player_info = pickle.load(saved_status_data)
            saved_status_data.close()
            
            # Null Save Checker
            null_save = True
            for line in chessboard_saved_input:
                if len(set(line)) != 1:
                    null_save = False
                    break
            
            if (null_save):
                gomoku_pvp_main(chessboard_size = 30) 
            else:
                gomoku_pvp_main(player_stat = player_info, saved_chessboard = chessboard_saved_input)
        except IOError:
            gomoku_pvp_main(chessboard_size = 30)
            
        # print(chessboard_saved_input)
        
    elif start_choice in '2':
        print("Program exited!")

def gomoku_pvp_main(player_stat: int = None, saved_chessboard: list = [], *, chessboard_size: int = 0) -> None:
    """
    Main Game Loop
    This function is in charge of the switch loop between the two
    and report the winning player when one player wins.
    Two players are denoted by O and X, respectively.
    ----------------------------------------
    Version Change Notice
    ----------------------------------------
    0.4    try/except block added to achieve auto-save functionality
    0.3    variable row_number & col_number is no longer 0 based index
    ----------------------------------------
    """
    if (not saved_chessboard) and (not player_stat) and (chessboard_size):
        chessboard = [[None] * chessboard_size for i in range(chessboard_size)]
        player_cycle = 0; info_hint = 1
    
    elif (not chessboard_size) and (saved_chessboard):
        chessboard = saved_chessboard
        player_cycle = player_stat; info_hint = 2
    print("info_hint" in locals())
    print("player_cycle" in locals())
    print("chessboard" in locals())
    while True:

        if info_hint:
            print("-" * 40)
            print("Please be aware that both players have to enter the row and\n + \
                  column numbers that they would like to place their pieces!")
            print("Player A is denoted by O, Player B is denoted by X")
            
            if info_hint == 2:
                print("Recent Saved Game detected, continue from the saved game!")
                info_hint -= 1
                
            print("-" * 40)
            info_hint -= 1
            draw_ascii_chessboard(chessboard)
            
        try:
            # First player A's turn: O
            if player_cycle == 0:
                print("-" * 40)
                print("Player A's turn!")

                # Please be aware that row/col number from 0.3 have become 1-len(chessboard) based,
                # no longer 0 based index as 0.2 and before
                row_number = input("Please enter the row number > ")
                col_number = input("Please enter the column number > ")

                while True:
                    if (row_number.isdigit() and (0 < int(row_number) <= len(chessboard))
                        and col_number.isdigit() and (0 < int(col_number) <= len(chessboard))):
                        break
                    print("You entered invalid row/column number, please try again!")
                    row_number = input("Please enter the row number > ")
                    col_number = input("Please enter the column number > ")

                coordinate = (int(row_number) - 1, int(col_number) - 1)
                chessboard = update_chessboard(board_input = chessboard, position = coordinate, player = player_cycle)
                player_cycle += 1
                draw_ascii_chessboard(chessboard)
                current_board_status = winning_check(chessboard)

                if current_board_status:
                    break
                continue

            # Second player B's turn: X
            elif player_cycle == 1:
                print("-" * 40)
                print("Player B's turn!")

                # Please be aware that row/col number from 0.3 have become 1-len(chessboard) based,
                # no longer 0 based index as 0.2 and before
                row_number = input("Please enter the row number > ")
                col_number = input("Please enter the column number > ")

                while True:
                    if (row_number.isdigit() and (0 < int(row_number) <= len(chessboard))
                        and col_number.isdigit() and (0 < int(col_number) <= len(chessboard))):
                        break
                    print("You entered invalid row/column number, please try again!")
                    row_number = input("Please enter the row number > ")
                    col_number = input("Please enter the column number > ")

                coordinate = (int(row_number) - 1, int(col_number) - 1)

                chessboard = update_chessboard(board_input = chessboard, position = coordinate, player = player_cycle)
                player_cycle -= 1
                draw_ascii_chessboard(chessboard)
                current_board_status = winning_check(chessboard)

                if current_board_status:
                    break
                continue
    
        # 0.4 New Feature
        # Auto save the current chessboard status and the player's turn when forced to exit
        except (SystemExit, KeyboardInterrupt, EOFError):
            import os, pickle
            if os.getcwd()[-3:] == "sav":
                pass
            else:
                os.chdir("sav")
            with open("gomoku_autosave", 'wb') as gomoku_status_save:
                pickle.dump((chessboard, player_cycle), gomoku_status_save)
            
            os.chdir("..")
            gomoku_status_save.close()
            break

    print("-" * 40)
    if ("current_board_status" in locals()) and (current_board_status):
        print("Player %s Win!\nGame ends here!" % current_board_status)
        # print(chessboard)
        print("-" * 40)
    else:
        print("Game auto saved!")
    
def update_chessboard(*, board_input: list = [], position: tuple = (), player: int = 0) -> list:
    """
    Place the corresponding 'O' or 'X' inside the board_input
    ----------------------------------------
    Version Change Notice
    ----------------------------------------
    0.3    exception handling added:
           can detect collision and force
           the player to re-place their piece
    ----------------------------------------
    """

    
    if board_input[position[0]][position[1]] == None:
        board_input[position[0]][position[1]] = 'O' if player == 0 else 'X'
        return board_input

    elif board_input[position[0]][position[1]] in 'OX':


        if board_input[position[0]][position[1]] == 'O':
            if player == 0:
                print("You cannot place another piece onto the previous one!\nPlease re-position it!")
            elif player == 1:
                print("You cannot place your piece onto the other player's!\nPlease re-position it!")            

        if board_input[position[0]][position[1]] == 'X':
            if player == 1:
                print("You cannot place another piece onto the previous one!\nPlease re-position it!")
            elif player == 0:
                print("You cannot place your piece onto the other player's!\nPlease re-position it!")            

        # Re-position the wrongly placed piece
        row_number = input("Please enter the row number > ")
        col_number = input("Please enter the column number > ")

        while True:
            if (row_number.isdigit() and (0 < int(row_number) <= len(board_input))
                and col_number.isdigit() and (0 < int(col_number) <= len(board_input))
                and board_input[int(row_number) - 1][int(col_number) - 1] == None): # index - 1 to support 1-based indexing
                break

            if (row_number.isdigit() and col_number.isdigit()):
                if board_input[int(row_number) - 1][int(col_number) - 1] == 'O':
                    if player == 0:
                        print("You cannot place another piece onto the previous one!\nPlease re-position it!")
                    elif player == 1:
                        print("You cannot place your piece onto the other player's!\nPlease re-position it!")            

                if board_input[int(row_number) - 1][int(col_number) - 1] == 'X':
                    if player == 1:
                        print("You cannot place another piece onto the previous one!\nPlease re-position it!")
                    elif player == 0:
                        print("You cannot place your piece onto the other player's!\nPlease re-position it!")            

            print("You entered invalid row/column number, please try again!")
            row_number = input("Please enter the row number > ")
            col_number = input("Please enter the column number > ")

        board_input[int(row_number) - 1][int(col_number) - 1] = 'O' if player == 0 else 'X'
        return board_input
    # ----------------------------------------
    # The following lines are obsolete
    # ----------------------------------------
    #update = lambda inp, pos, plyr: inp[pos[0]][pos[1]] = plyr
    #update(board_input, position, 'O') if player == 0 else update(board_input, position, 'X')
    # ----------------------------------------
            
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
                        # print(player1_count)
                    else:
                        player1_count = 0

                elif line_input[pointer] == 'X':

                    if following_entry == 'X':
                        player2_count += 1 if (player2_count != 0) else 2
                        # print(player2_count)
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
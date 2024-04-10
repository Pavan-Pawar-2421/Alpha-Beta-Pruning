import tkinter as tk
import time

# Define the game board - Initial State
# board = [
#     ['X', ' ', 'O'],
#     ['O', 'X', ' '],
#     [' ', ' ', ' ']
# ]

# board = [
#     ['X', ' ', 'X'],
#     [' ', ' ', 'O'],
#     ['O', 'X', 'O']
# ]

board = [
    ['O', 'O', 'X'],
    [' ', 'X', ' '],
    ['O', 'X', ' ']
]

# Define the player symbols
PLAYER_X = 'X'
PLAYER_O = 'O'

# Define the GUI window
window = tk.Tk()
window.title("Alpha-Beta Pruning Demonstration")

# Define the canvas to display the game board
canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Define the function to draw the game board
def draw_board(pruned_moves=None, pruned_max=False, pruned_min=False):
    canvas.delete("all")

    # Calculate the position to center the game board
    board_size = 300  
    board_x = (canvas_width - board_size) // 2
    board_y = (canvas_height - board_size) // 2

    for i in range(3):
        for j in range(3):
            x1 = board_x + j * 100
            y1 = board_y + i * 100
            x2 = x1 + 100
            y2 = y1 + 100
            fill_color = "white"
            symbol = board[i][j]

            # if pruned_moves and (i, j) in pruned_moves:
            #     canvas.configure(bg="yellow")
            #     canvas.create_text((x1 + x2) / 2, 20, text="State Pruned!!", font=("Arial",20), fill="red") 
                
            if pruned_moves and (i, j) in pruned_moves:
                canvas.configure(bg="yellow")
                text = "State Pruned: "
                if pruned_max and pruned_min:
                    text += "Min/Max"
                elif pruned_max:
                    text += "Max"
                elif pruned_min:
                    text += "Min"
                text_x = canvas_width // 2
                text_y = 20
                canvas.create_text(text_x, text_y, text=text, font=("Arial", 16), fill="red") 
            if pruned_max and pruned_min:
                fill_color = "red"  
            elif pruned_max:
                fill_color = "orange"
            elif pruned_min:
                fill_color = "green"
                
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)
            text_color = "black"
            
            if symbol == PLAYER_X or symbol == PLAYER_O:
                if pruned_moves and (i, j) in pruned_moves:
                    text_color = "red"  
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=symbol, font=("Arial", 32), fill=text_color)
    window.update()
    canvas.config(bg="white")

# Define the function to check if the game is over
def game_over(board):
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != ' ':
            return board[0][j]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    # Check if the game is a tie
    if ' ' not in [cell for row in board for cell in row]:
        return 'Tie'
    return None

# Define the minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    result = game_over(board)
    if result is not None:
        if result == 'Tie':
            return 0
        elif result == PLAYER_X:
            return 1
        else:
            return -1

    if depth == 3:  # Stop exploring the tree at depth 7
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        pruned_moves = []
        print(f"Depth: {depth}, Max Player")
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = PLAYER_X
                    print(f"Trying move ({i}, {j})")
                    print_board(board)
                    draw_board(pruned_moves=pruned_moves)  # Update the GUI
                    time.sleep(1)  # Slow down the frame update
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    print(f"Evaluation: {eval}")
                    board[i][j] = ' '
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (i, j)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        print("Pruned at Max")
                        pruned_moves.append((i, j))
                        draw_board(pruned_moves=pruned_moves, pruned_max=True)  
                        time.sleep(2)  
                        draw_board()  
                        return max_eval
        print(f"Best move for Max Player: {best_move}")
        return max_eval
    else:
        min_eval = float('inf')
        best_move = None
        pruned_moves = []
        print(f"Depth: {depth}, Min Player")
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = PLAYER_O
                    print(f"Trying move ({i}, {j})")
                    print_board(board)
                    draw_board(pruned_moves=pruned_moves)  # Update the GUI
                    time.sleep(2)  # Slow down the frame update
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    print(f"Evaluation: {eval}")
                    board[i][j] = ' '
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (i, j)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        print("Pruned at Min")
                        pruned_moves.append((i, j))
                        draw_board(pruned_moves=pruned_moves, pruned_min=True)  
                        time.sleep(2)  
                        draw_board()  
                        return min_eval
        print(f"Best move for Min Player: {best_move}")
        return min_eval

# Define the function to print the board
def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

# Call the minimax function to generate the game tree
print("Generating game tree...")
print(minimax(board, 0, float('-inf'), float('inf'), True))
print("*")


# Final State (printing)
print("Final State:")
print_board(board)

draw_board()
window.mainloop()
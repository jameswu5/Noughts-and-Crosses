# Nought and crosses by James Wu
# Adapted from the skeleton code
# Features: Player vs Player, Player vs Perfect AI, best move from one game state, interactive interface, easy inputs, some validation

class GameState:
    WINNING_TRIPLES = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    cache = {}

    def __init__(self, board): 
        self.board = board

    def next_to_move(self):
        count = 0
        for i in range(len(self.board)):
            if self.board[i] != '.':
                count += 1
        if count % 2 == 0:
            return 'O'
        else:
            return 'X'
    
    def last_moved(self):
        count = 0
        for i in range(len(self.board)):
            if self.board[i] != '.':
                count += 1
        if count % 2 == 0:
            return 'X'
        else:
            return 'O'
        
    def check_occupied(self,cell):
        if self.board[cell] == '.':
            return False
        else:
            return True

    def replace(self, index, letter):
        string = list(self.board)
        string[index] = letter
        new_string = "".join(string)
        return new_string

    def make_move(self, cell):
        letter = self.next_to_move()
        return GameState(self.replace(cell, letter))

    def is_game_won(self):
        for i in range(len(GameState.WINNING_TRIPLES)):
            if self.board[GameState.WINNING_TRIPLES[i][0]] == self.board[GameState.WINNING_TRIPLES[i][1]] and self.board[GameState.WINNING_TRIPLES[i][0]] == self.board[GameState.WINNING_TRIPLES[i][2]]:
                if self.board[GameState.WINNING_TRIPLES[i][0]] != '.':
                    return True
        return False

    def is_grid_full(self):
        if '.' not in self.board:
            return True
        return False

    def calculate_value(self):
        if self.is_game_won():
            return (0, None)
        elif self.is_grid_full():
            return (1, None)
        else:            
            if self.board in GameState.cache:
                return GameState.cache.get(self.board)
            
            for i in range(9):
                if self.board[i] == '.':
                    
                    new_state = self.make_move(i)
                    value = new_state.calculate_value()
                    GameState.cache[new_state.board] = value

                    if value[0] == 0:
                        return (2, i)
            
            for j in range(9):
                if self.board[j] == ".":
                    new_state = self.make_move(j)
                    value = new_state.calculate_value()
                    GameState.cache[new_state.board] = value

                    if value[0] == 1:
                        return (1, j)

            return (0, None)

    def display(self):
        print()
        for i in range(3):
            print(str(self.board[i]), end = " ")
        print()
        for i in range(3, 6):
            print(str(self.board[i]), end = " ")
        print()
        for i in range(6, 9):
            print(str(self.board[i]), end = " ")
        print()

def test():
    starting_board = GameState(input("Enter the game state for the starting board \n"))
    starting_board.display()
    print(starting_board.calculate_value())

def convert_index(index):
    positions = ['top left', 'top middle', 'top right', 'left middle', 'dead centre', 'right middle', 'bottom left', 'bottom middle', 'bottom right']
    return positions[index]

def convert_text(text):
    positions = ['top left', 'top middle', 'top right', 'left middle', 'dead centre', 'right middle', 'bottom left', 'bottom middle', 'bottom right']
    for i in range(len(positions)):
        if text == positions[i]:
            return i
    return None

def enter_move(board):
    while True:
        flag = True
        move = input("Which position would you like to play? ")
        try:
            move = int(move)
        except:
            move = convert_text(move.lower())
            if move is None:
                flag = False
        if flag:
            if board.check_occupied(move):
                move = int(input("You can't overwrite, try again! "))
            else:
                break
    return move

def game(first_go):
    turn = first_go
    game_board = GameState('.........')
    game_board.display()

    while True:
        print()
        if turn == 'player':
            print("These are the options:")
            print(", ".join(['top left', 'top middle', 'top right', 'left middle', 'dead centre', 'right middle', 'bottom left', 'bottom middle', 'bottom right']))
            print()
            move = enter_move(game_board)
            game_board = game_board.make_move(move)
            game_board.display()

            if game_board.is_game_won():
                print("You win!\n")
                break
            elif game_board.is_grid_full():
                print("It's a draw!\n")
                break

            turn = 'AI'

        else:
            best_move = game_board.calculate_value()
            their_move = best_move[1]

            print("The AI plays", convert_index(their_move))
            game_board = game_board.make_move(their_move)
            game_board.display()

            if game_board.is_game_won():
                print("The AI wins.\n")
                break
            elif game_board.is_grid_full():
                print("It's a draw!\n")
                break
            
            turn = 'player'

def friendly(player1, player2):
    
    if player1 == "":
        player1 = 'Player 1'
    if player2 == "":
        player2 = 'Player 2'
    
    turn = True

    game_board = GameState('.........')
    game_board.display()

    while True:
        print()
        print("These are the options:")
        print(", ".join(['top left', 'top middle', 'top right', 'left middle', 'dead centre', 'right middle', 'bottom left', 'bottom middle', 'bottom right']))
        print()
        if turn:
            print(player1, "(O) to move!")
        else:
            print(player2, "(X) to move!")
        
        move = enter_move(game_board)
        game_board = game_board.make_move(move)
        game_board.display()

        if game_board.is_game_won():
            player_won = game_board.last_moved()
            if player_won == 'O':
                print(player1, "wins!\n")
            else:
                print(player2, "wins!\n")
            break
        elif game_board.is_grid_full():
            print("It's a draw!\n")
            break

        if turn:
            turn = False
        else:
            turn = True

def main():
    print("Welcome to noughts and crosses!")
    option = input("Who would you like to play the AI or another player? ").lower()
    if option == 'ai':
        move_first = input("Would you like to move first? Yes or no: ").lower()
        if move_first == "yes":
            game('player')
        elif move_first == 'no':
            game('AI')
    elif option == 'player':
        player1 = input("Enter Player 1's name: ")
        player2 = input("Enter Player 2's name: ")
        friendly(player1, player2)


if __name__ == "__main__":
    main()
import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False
        self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        client, addr = server.accept()
        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.you = "O"
        self.opponent = "X"
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        try:
            while not self.game_over:
                if self.turn == self.you:
                    move = input("Enter a move (row, column): ")
                    if self.check_valid_move(move.split(',')):
                        client.send(move.encode('utf-8'))
                        self.apply_move(move.split(','), self.you)
                        self.turn = self.opponent
                    else:
                        print("Invalid move! Please enter row and column as numbers (0-2) and ensure the space is empty.")
                else:
                    data = client.recv(1024)
                    if not data:
                        client.close()
                        break
                    else:
                        self.apply_move(data.decode('utf-8').split(','), self.opponent)
                        self.turn = self.you  # Change the turn back to 'you'
            print("Game over!")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            client.close()

    def apply_move(self, move, player):
        if self.game_over:
            return
        row, col = int(move[0]), int(move[1])
        if self.board[row][col] == "":
            self.counter += 1
            self.board[row][col] = player
            self.print_board()
            if self.check_if_won():
                if self.winner == self.you:
                    print("You win!")
                elif self.winner == self.opponent:
                    print("You lose!")
                self.game_over = True
            elif self.counter == 9:
                print("It is a tie!")
                self.game_over = True
        else:
            print("Invalid move! The space is already taken.")

    def check_valid_move(self, move):
        # Check if move has exactly 2 elements
        if len(move) != 2:
            return False
        # Check if both elements are strings representing valid integers
        try:
            row = int(move[0])
            col = int(move[1])
            # Check if row and col are within bounds (0-2)
            if not (0 <= row < 3 and 0 <= col < 3):
                return False
            # Check if the board position is empty
            if self.board[row][col] != "":
                return False
            return True
        except ValueError:
            # Return False if move[0] or move[1] cannot be converted to integers
            return False

    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                self.winner = self.board[row][0]
                return True

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                self.winner = self.board[0][col]
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.winner = self.board[0][0]
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.winner = self.board[0][2]
            return True

        return False

    def print_board(self):
        for row in range(3):
            for col in range(3):
                print(f" {self.board[row][col]}", end="")
                if col < 2:
                    print(" |", end="")
            print()
            if row < 2:
                print("-----------")

# Example usage
game = TicTacToe()
game.connect_to_game("localhost", 9999)
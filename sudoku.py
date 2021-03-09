from random import shuffle
from copy import deepcopy


class Sudoku:
    def __init__(self):
        pass

    def print_board(self, board):
        """Print board for user to view result."""
        for row in range(len(board)):
            if row % 3 == 0 and row != 0:
                print('---------------------')
            for col in range(len(board)):
                if col % 3 == 0 and col != 0:
                    print('|', end=" ")
                if col == 8:
                    print(board[row][col])
                else:
                    print(str(board[row][col]), end=" ")

    def find_empty_pos(self, board):
        """
        Scans entire board for zeros and returns first location having a zero.
        If no zeros on board, returns None.
        """
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == 0:
                    return (row,col)
        return None

    def is_valid(self, board, num, position):
        """Checks if the given number is a valid option to insert."""

        r,c = position

        # Checks row
        for col in range(len(board)):
            # returns false if num exists in given row and
            # if column it exists in is different than the given column
            if board[r][col] == num and c != col:
                return False

        # Checks col
        for row in range(len(board)):
            # returns false if num exists in given column and
            # if row it exists in is different than the given row
            if board[row][c] == num and r != row:
                return False

        # Checks box
        # Checking which 9 digit square we are in according to coordinates
        x_loc = r // 3
        y_loc = c // 3

        # Loop through the square and return false if num exists in the square
        # and position doesn't equal the given position
        for row in range(x_loc*3, x_loc*3 + 3):
            for col in range(y_loc*3, y_loc*3 + 3):
                if board[row][col] == num and (row,col) != position:
                    return False
        return True


class Sudoku_Solver(Sudoku):
    def __init__(self, board=None):
        self.board = board

    def solve_board(self, board):
        """Backtrack until sudoku board has been solved."""
        empty_space = self.find_empty_pos(board)

        if not empty_space:
            return True
        else:
            row, col = empty_space

        for i in range(1, 10):
            if self.is_valid(board, i, (row, col)):
                board[row][col] = i

                if self.solve_board(board):
                    return True

                self.board[row][col] = 0

        return False


class Sudoku_Board_Generator(Sudoku_Solver):
    def __init__(self):
        self.counter = 0
        self.board = [[0 for row in range(0,9)] for col in range(0,9)]
        self.board = self.generate_board(self.board)

    def generate_board(self, board):
        """Generates a new game board."""
        self.solve_board(self.board)
        starter_board = self.remove_nums_from_board()
        return starter_board

    def fetch_filled_squares(self, board):
        """
        Fetch all non zero squares and return a shuffled
        list of those squares.
        """
        filled_squares = []
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if board[row][col] != 0:
                    filled_squares.append((row,col))
        shuffle(filled_squares)
        return filled_squares

    def remove_nums_from_board(self):
        """
        Remove numbers from the generated game board
        and verify only one unique solution is available.
        """
        filled_squares = self.fetch_filled_squares(self.board)
        filled_squares_count = len(filled_squares)

        while filled_squares_count != 17:

            row, col = filled_squares.pop()
            filled_squares_count -= 1

            # Store the value of the removed square in case replacement needed.
            removed_square = self.board[row][col]
            self.board[row][col] = 0

            # make a copy of board and check if more than one solution
            # exists on copied current board
            board_copy = deepcopy(self.board)
            self.counter = 0
            self.solution_counter(board_copy)

            # if more than one solution exists, revert value of removed square
            # and increment filled squares count by 1
            if self.counter != 1:
                self.board[row][col] = removed_square
                filled_squares_count += 1

        print('Starting Board: ')
        print('\n')
        self.print_board(self.board)
        return self.board

    def solution_counter(self, board):
        """Counts how many different solutions existing board has."""
        for row in range(len(board)):
            for col in range(len(board)):
                #loops through board until zero found
                if board[row][col] == 0:
                    #trys to insert 1-9 in position and checks if insertion is valid
                    for i in range(1, 10):
                        if self.is_valid(board, i, (row,col)):
                            #if insertion is valid, insert value at position
                            board[row][col] = i
                            #if no other empty cells exist, increment counter by 1
                            # and break out of enclosing loop
                            if not self.find_empty_pos(board):
                                self.counter += 1
                                break
                            else:
                                if self.solution_counter(board):
                                    return True
                    break
        self.board[row][col] = 0
        return False

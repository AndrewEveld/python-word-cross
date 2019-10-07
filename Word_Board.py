from typing import *


class WordBoard:

    def __init__(self, size: int):
        self.board: List[List[str]] = []
        self.size: int = size
        self.english_words: List[str] = []
        self.unconfirmed_board: List[List[str]] = []
        self.board.append([])
        self.unconfirmed_board.append([])
        for i in range(1, size + 1):
            self.board.append([])
            self.unconfirmed_board.append([])
            self.board[i].append('0')
            self.unconfirmed_board[i].append('0')
            for j in range(1, size + 1):
                self.board[i].append('0')
                self.unconfirmed_board[i].append('0')
        f = open('english2.txt', 'r')
        for word in f:
            self.english_words.append(word.upper().strip())

    # Take a word, the row and column, and the orientation (vertical or horizontal) as parameters.
    # Returns True if the word is a word and fits in the board and agrees with the other words in the board.
    def add_word(self, word: str, row: int, column: int, orientation: str) -> bool:
        if self.__is_english(word):
            if self.__will_word_fit(word, row, column, orientation):
                if orientation == "VERTICAL":
                    for i in range(row, row + len(word)):
                        self.unconfirmed_board[i][column] = word[i - row]
                else:
                    for i in range(column, column + len(word)):
                        self.unconfirmed_board[row][i] = word[i - column]

                # Check if the added word agrees with the current words on the board.
                # (only from up to down and left to right).
                if self.__check_board_valid():
                    self.__update_board()
                    return True
                else:
                    print('This word does not agree with other words currently on the board!')
                    self.__reset_unconfirmed_board()
                    return False
            else:
                print('This word will not fit on the board!')
                return False
        else:
            print('This word is not English!')

    def __is_english(self, word: str) -> bool:
        if word in self.english_words:
            return True
        return False

    # Takes the current board and list of english words as parameters.
    # Returns boolean base on if the board is valid based on the rules of the game.
    def __check_board_valid(self) -> bool:
        horizontal_words_string: str = ""
        vertical_words_string: str = ""
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                horizontal_words_string += self.unconfirmed_board[i][j]
                vertical_words_string += self.unconfirmed_board[j][i]
            horizontal_words_string += "0"
            vertical_words_string += "0"
        current_words_list: List[str] = horizontal_words_string.split("0")
        current_words_list.extend(vertical_words_string.split("0"))
        for word in current_words_list:
            if len(word) > 1:
                if word not in self.english_words:
                    return False
        return True

    # Takes board dictionary, string word, orientation, and placement as parameters.
    # Returns boolean True if the word fits in desired location and False if not.
    def __will_word_fit(self, word: str, row: int, column: int, orientation: str) -> bool:
        if orientation == 'HORIZONTAL':
            if len(word) - 1 + column > self.size:
                return False
            for i in range(len(word)):
                if self.board[row][column + i] != '0':
                    return False
            return True
        elif orientation == 'VERTICAL':
            if row + len(word) - 1 > self.size:
                return False
            for i in range(len(word)):
                if self.board[row + i][column] != '0':
                    return False
            return True

    # Syncs the unconfirmed board to the board.
    def __reset_unconfirmed_board(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                self.unconfirmed_board[i][j] = self.board[i][j]

    # Syncs the board to the unconfirmed board.
    def __update_board(self):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                self.board[i][j] = self.unconfirmed_board[i][j]

    def print_board(self):
        to_print: str = ''
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                to_print += self.board[i][j] + ' '
            to_print += '\n'
        print(to_print)

    # Takes a board dictionary as parameter.
    # Returns the int number of letters on the board.
    def tally_points(self) -> int:
        score: int = 0
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.board[i][j] != '0':
                    score += 1
        return score

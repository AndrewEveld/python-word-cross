##############################
# CSC 150 Fall 2018
# Andrew Eveld
# Project 2
##############################

from typing import *
from random import randint


def choose_difficulty():
    print('Choose difficulty:')
    print('easy: 2 letter words or higher')
    print('medium: 3 letter words or higher')
    print('hard: 4 letter words or higher')
    choice: str = input('Difficulty: ').lower()
    while choice != 'hard' and choice != 'medium' and choice != 'easy':
        print('Invalid difficulty')
        choice: str = input('Enter hard, medium, or easy: ').lower()
    return choice


def min_word(difficulty: str) -> int:
    if difficulty == 'hard':
        word: int = 4
    elif difficulty == 'medium':
        word: int = 3
    else:
        word: int = 2
    return word


def word_search(word, english_words: List[str]):
    word = word.lower()
    first = 0
    last = len(english_words) - 1
    found = False
    while first <= last and not found:
        middle = (first + last)//2
        if english_words[middle] == word:
            found = True
        else:
            if word < english_words[middle]:
                last = middle - 1
            else:
                first = middle + 1
    return found


def create_board() -> Dict[str, str]:
    board: Dict[str, str] = {}
    for i in range(7):
        for r in range(7):
            location: str = chr(65 + i) + str(r + 1)
            board[location] = '0'
    return board


def print_board(board: Dict[str, str]):
    print('   1 2 3 4 5 6 7')
    for i in range(7):
        row: str = chr(65 + i) + ': '
        for r in range(7):
            row += board[chr(65 + i) + str(r + 1)] + ' '
        print(row)


def point_system(word: str, word_key: List[str], character_points: Dict[str, int], difficulty: int, english_words: List[str]):
    if word_search(word, english_words) and len(word) >= difficulty:
        for key in word_key:
            character_points[key] += 1
    else:
        for key in word_key:
            character_points[key] -= 1
    return character_points


# Function that takes the updated board, difficulty, and orientation (0 for vertical, 1 for horizontal
# Outputs a dictionary with row + column as key and an int as value.
# If a key's value is >= 0 then the letter is valid, else it is invalid and the move will be reversed elsewhere.
def validate_letters(board: Dict[str, str], difficulty: int, orientation: int, english_words: List[str]) -> Dict[str, int]:
    to_return: Dict[str, int] = create_board()
    for key in to_return:
        to_return[key] = int(to_return[key])
    row: int = 0
    column: int = 0
    for i in range(7):
        if orientation == 0:
            column = i
        else:
            row = i
        word1: str = ''
        word1_keys: List[str] = []
        between: int = 0
        word2: str = ''
        word2_keys: List[str] = []
        for r in range(7):
            if orientation == 0:
                row = r
            else:
                column = r
            if board[chr(65 + row) + str(column + 1)] == '0' and word1 != '':
                between += 1
            elif board[chr(65 + row) + str(column + 1)] != '0' and between == 0:
                word1 += board[chr(65 + row) + str(column + 1)]
                word1_keys.append(chr(65 + row) + str(column + 1))
            elif board[chr(65 + row) + str(column + 1)] != '0' and between != 0:
                word2 += board[chr(65 + row) + str(column + 1)]
                word2_keys.append(chr(65 + row) + str(column + 1))
        to_return = point_system(word1, word1_keys, to_return, difficulty, english_words)
        to_return = point_system(word2, word2_keys, to_return, difficulty, english_words)
    return to_return


def check_board_valid(board: Dict[str, str], difficulty: int, english_words: List[str]):
    char_points_1: Dict[str, int] = validate_letters(board, difficulty, 0, english_words)
    char_points_2: Dict[str, int] = validate_letters(board, difficulty, 1, english_words)
    for key in char_points_1:
        char_points_1[key] += char_points_2[key]
    for key in char_points_1:
        if char_points_1[key] < 2:
            return False
    return True


def fill_letters(current_letters: List[str]) -> List[str]:
    while len(current_letters) < 10:
        current_letters.append(chr(65 + randint(0, 25)))
    return current_letters


def get_word(choices: List[str]) -> str:
    print('What word would you like to place?')
    print(choices)
    choice: str = input('Word choice: ').upper()
    if choice == 'QUIT GAME':
        return choice
    while not check_typed_word(choice, choices):
        print('word contains invalid letters!')
        choice = input('Word choice: ').upper()
    return choice


def check_typed_word(word: str, choices: List[str]) -> bool:
    check_choices: List[str] = []
    for letter in choices:
        check_choices.append(letter)
    done: bool = False
    while not done:
        for letters in word:
            if letters not in check_choices:
                return False
            else:
                check_choices.remove(letters)
        done = True
    return done


def letter_placement() -> List[str]:
    row: str = input('Which row do you wish to place the first letter of your word in? ').upper()
    column: str = input('Which column do you wish to place the first letter of your word in? ')
    placement_list: List[str] = []
    while len(row) > 1:
        print('Invalid row: A through G accepted only.')
        row = input('Row: ').upper()
    while ord(row) < 65 or ord(row) > 71:
        print('Invalid row: A through G accepted only.')
        row = input('Row: ').upper()
    while not column.isdigit() or int(column) < 1 or int(column) > 7:
        print('Invalid column: 1 through 7 accepted only.')
        column = input('Column: ')
    placement_list.append(row)
    placement_list.append(column)
    return placement_list


def update_test_board(board: Dict[str, str]) -> Dict[str, str]:
    test_board: Dict[str, str] = {}
    for key in board:
        test_board[key] = board[key]
    return test_board


def update_test_letters(letters: List[str]) -> List[str]:
    test_letters: List[str] = []
    for letter in letters:
        test_letters.append(letter)
    return test_letters


def tally_points(board: Dict[str, str]) -> int:
    score: int = 0
    for key in board:
        if board[key] != '0':
            score += 1
    return score


def subtract_letters(letter_list: List[str], letters: str):
    for letter in letters:
        letter_list.remove(letter)
    return letter_list


def place_word(board: Dict[str, str], word: str, placement: List[str], orientation: str) -> Dict[str, str]:
    if orientation == 'HORIZONTAL':
        for i in range(len(word)):
            board[placement[0] + str(int(placement[1]) + i)] = word[i]
    else:
        for i in range(len(word)):
            board[chr(ord(placement[0]) + i) + placement[1]] = word[i]
    return board


def will_word_fit(board: Dict[str, str], word: str, orientation: str, placement: List[str]) -> bool:
    if orientation == 'HORIZONTAL':
        if len(word) - 1 + int(placement[1]) > 7:
            return False
        for i in range(len(word)):
            if board[placement[0] + str(int(placement[1]) + i)] != '0':
                return False
        return True
    elif orientation == 'VERTICAL':
        if ord(placement[0]) + len(word) - 1 > 71:
            return False
        for i in range(len(word)):
            if board[chr(ord(placement[0]) + i) + placement[1]] != '0':
                return False
        return True


def word_orientation() -> str:
    print('Place the word vertically or horizontally?')
    print('Vertical will start at the beginning letter and go down.')
    print('Horizontal will start at the beginning letter and go right.')
    orientation: str = input('Orientation:(vertical/horizontal) ').upper()
    done: bool = False
    while not done:
        if orientation != 'HORIZONTAL' and orientation != 'VERTICAL':
            print('Invalid input.')
            orientation = input('Horizontal or vertical? ').upper()
        else:
            done = True
    return orientation


def y_n(answer: str) -> str:
    while answer != 'YES' and answer != 'NO':
        answer = input('Please answer "yes" or "no": ').upper()
    return answer


def main():
    f = open('english2.txt', "r")
    english_words = []
    for line in f:
        english_words.append(line.lower().strip())
    print('You are playing Python Bonanza!')
    print('You will be given 7 letters')
    print('You must make words out of these letters on a blank 7 x 7 board.')
    print('Each time you are done making a word, your letters will be renewed.')
    print('You are free to make more than one word per turn as long as they are')
    print('long enough and valid words.')
    print('Words you place do not have to be words as long as they connect with')
    print('other words to make words on your board.')
    print('Words are not required to be connected to be counted in your final score.')
    print('You receive one point for every letter you successfully place.')
    difficulty: int = min_word(choose_difficulty())
    board: Dict[str, str] = create_board()
    letters: List[str] = ['E', 'A', 'R', 'I', 'O', 'T', 'N', 'S', 'L', 'C']
    test_letters = update_test_letters(letters)
    test_board: Dict[str, str] = update_test_board(board)
    done: bool = False
    while not done:
        print_board(test_board)
        word_choice: str = get_word(test_letters)
        if word_choice == 'QUIT GAME':
            done = True
        else:
            orientation: str = word_orientation()
            placement: List[str] = letter_placement()
            if will_word_fit(test_board, word_choice, orientation, placement):
                place_word(test_board, word_choice, placement, orientation)
                test_letters = subtract_letters(test_letters, word_choice)
                print_board(test_board)
            else:
                print('Word will not fit!')
                test_letters = update_test_letters(letters)
                test_board = update_test_board(board)
                print_board(test_board)
        if check_board_valid(test_board, difficulty, english_words):
            test_letters = fill_letters(test_letters)
            letters = update_test_letters(test_letters)
            board = update_test_board(test_board)
            another = y_n(input('Another Word?(yes/no) ').upper())
            if another == 'NO':
                done = True
        else:
            print('Invalid word or word too short! Try again!')
            test_board = update_test_board(board)
            test_letters = update_test_letters(letters)
    print('Your final score is ' + str(tally_points(board)) + ' points!')


main()






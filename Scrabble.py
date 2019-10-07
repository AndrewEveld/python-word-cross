##############################
# CSC 150 Fall 2018
# Andrew Eveld
# Project 2
##############################

from typing import *
from random import randint
from Word_Board import WordBoard


# Prompt user for a difficulty and return their choice


def choose_size() -> int:
    print('Choose the size of the board:')
    print('The size must be an integer greater than 1.')
    print('For an integer n, the game board will be n * n')
    choice: str = input('Size: ')
    while not choice.isdigit() or int(choice) < 2:
        print('Invalid difficulty')
        choice: str = input('Size must be an integer larger than 1:').lower()
    return int(choice)


# Replaces letter used from the last turn with random letters.
# Takes list of strings as parameter.
# Returns list with new random letters.
def fill_letters(current_letters: List[str]) -> List[str]:
    while len(current_letters) < 10:
        current_letters.append(chr(65 + randint(0, 25)))
    return current_letters


# Takes a list of letters as parameter.
# Prompts user for a word created from the letters.
# Returns word user made.
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


# Takes a word and list of letters as parameters.
# Returns boolean True if word can be made using the letters in the string and False if not. 
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


# Prompts user for the location of the starting key of their word. 
# Returns list that has the row (A-G) and index 0 and column (1-7) as index 1.
def letter_placement(board_size: int) -> List[int]:
    row: str = input('Which row do you wish to place the first letter of your word in? ')
    column: str = input('Which column do you wish to place the first letter of your word in? ')
    placement_list: List[int] = []
    while not row.isdigit() or int(row) < 1 or int(row) > board_size:
        print('Invalid row: 1 through ' + str(board_size) + ' accepted only')
        row = input('Row: ').upper()
    while not column.isdigit() or int(column) < 1 or int(column) > board_size:
        print('Invalid column: 1 through ' + str(board_size) + ' accepted only.')
        column = input('Column: ')
    placement_list.append(int(row))
    placement_list.append(int(column))
    return placement_list


# Takes list of letters as parameter.
# Returns duplicate of the list.
def update_test_letters(letters: List[str]) -> List[str]:
    test_letters: List[str] = []
    for letter in letters:
        test_letters.append(letter)
    return test_letters


# Takes the list of letters and the word chosen by user as parameters.
# Returns the letters from the list that were not used. 
def subtract_letters(letter_list: List[str], letters: str):
    for letter in letters:
        letter_list.remove(letter)
    return letter_list


# Prompts the user the desired orientation of their selected word.
# Returns string 'VERTICAL' or 'HORIZONTAL'.
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


# Takes the previous answer as parameter.
# Returns 'YES' or 'NO' once user types either one. 
def y_n(answer: str) -> str:
    while answer != 'YES' and answer != 'NO':
        answer = input('Please answer "yes" or "no": ').upper()
    return answer


def main():
    f = open("english2.txt", "r")
    english_words = []

    for line in f:
        english_words.append(line.upper().strip())

    print('You are playing Python Word Cross!')
    print('You will be given 7 letters')
    print('You must make words out of these letters on a blank board.')
    print('Each time you are done making a word, your letters will be renewed.')
    print('You are free to make more than one word per turn as long as they are')
    print('long enough and valid words.')
    print('Words you place do not have to be words as long as they connect with')
    print('other words to make words on your board.')
    print('Words are not required to be connected to be counted in your final score.')
    print('You receive one point for every letter you successfully place.')

    board_size: int = choose_size()
    board: WordBoard = WordBoard(board_size)
    letters: List[str] = ['E', 'A', 'R', 'I', 'O', 'T', 'N', 'S', 'L', 'C']
    test_letters = update_test_letters(letters)

    done: bool = False
    while not done:
        board.print_board()
        word_choice: str = get_word(test_letters)
        if word_choice == 'QUIT GAME':
            done = True
        else:
            orientation: str = word_orientation()
            placement: List[int] = letter_placement(board_size)
            if board.add_word(word_choice, placement[0], placement[1], orientation):
                test_letters = subtract_letters(test_letters, word_choice)
                board.print_board()
                test_letters = fill_letters(test_letters)
                letters = update_test_letters(test_letters)
                another = y_n(input('Another Word?(yes/no) ').upper())
                if another == 'NO':
                    done = True
            else:
                test_letters = update_test_letters(letters)
    print('Your final score is ' + str(board.tally_points()) + ' points!')


main()




